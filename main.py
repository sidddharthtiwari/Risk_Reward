import streamlit as st
import pandas as pd

def calculate_risk_reward(avg_price, max_against_price, target_price, tick_size, 
                         no_of_lots, tick_value, tc_per_lot, total_lots_entry_exit, 
                         rebate_per_lot):
    """
    Calculate risk and reward based on the provided formulas
    """
    
    # Risk calculation
    # (|Avg price - Max Against Price|/tick size) * no of lots * tick value + 
    # (TC per lot * total lots for entry/exit * 2 * no of lots) - 
    # (Rebate per lot * total lots for entry/exit * 2 * no of lots)
    
    price_movement_risk = abs(avg_price - max_against_price) / tick_size
    risk_from_price = price_movement_risk * no_of_lots * tick_value
    
    transaction_cost = tc_per_lot * total_lots_entry_exit * 2 * no_of_lots
    rebate_benefit = rebate_per_lot * total_lots_entry_exit * 2 * no_of_lots
    
    total_risk = risk_from_price + transaction_cost - rebate_benefit
    
    # Reward calculation  
    # |Avg price - Target price|/tick size * no of lots * tick value +
    # (TC per lot * total lots for entry/exit * 2 * no of lots) - 
    # (Rebate per lot * total lots for entry/exit * 2 * no of lots)
    
    price_movement_reward = abs(avg_price - target_price) / tick_size
    reward_from_price = price_movement_reward * no_of_lots * tick_value
    
    # Transaction costs and rebates are same for both risk and reward
    total_reward = reward_from_price - transaction_cost + rebate_benefit
    
    return total_risk, total_reward

def format_currency(value):
    """Format value as currency with appropriate decimal places"""
    if abs(value) >= 1:
        return f"${value:,.2f}"
    elif abs(value) >= 0.01:
        return f"${value:.4f}"
    elif abs(value) >= 0.0001:
        return f"${value:.6f}"
    else:
        return f"${value:.8f}"

def main():
    st.set_page_config(
        page_title="Risk-Reward Analysis",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Risk-Reward Analysis Tool")
    st.markdown("---")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("💰 Price Parameters")
        avg_price_str = st.text_input(
            "Average Price ($)", 
            value="",
            help="The average entry price of your position (e.g., 0.008, 150.25, 0.00001234)"
        )
        
        max_against_price_str = st.text_input(
            "Max Against Price - Stop Loss ($)", 
            value="",
            help="Maximum price movement against your position (e.g., 0.006, 148.50)"
        )
        
        target_price_str = st.text_input(
            "Target Price ($)", 
            value="",
            help="Your profit target price (e.g., 0.012, 155.75)"
        )
        
        tick_size_str = st.text_input(
            "Tick Size ($)", 
            value="",
            help="Minimum price movement unit (e.g., 0.001, 0.01, 0.00001)"
        )
    
    with col2:
        st.header("📈 Position Parameters")
        no_of_lots_str = st.text_input(
            "Number of Lots", 
            value="",
            help="Total number of lots in your position (e.g., 1, 10, 0.5)"
        )
        
        tick_value_str = st.text_input(
            "Tick Value ($)", 
            value="",
            help="Monetary value of one tick movement in dollars (e.g., 1, 25, 0.01)"
        )
        
        total_lots_entry_exit_str = st.text_input(
            "Total Lots for Entry/Exit", 
            value="",
            help="Number of lots used for entry and exit calculations"
        )
        
        st.header("💸 Cost Parameters")
        tc_per_lot_str = st.text_input(
            "Transaction Cost per Lot ($)", 
            value="0",
            help="Transaction cost charged per lot in dollars (optional - defaults to 0)"
        )
        
        rebate_per_lot_str = st.text_input(
            "Rebate per Lot ($)", 
            value="0",
            help="Rebate received per lot in dollars (optional - defaults to 0)"
        )
    
    st.markdown("---")
    
    # Calculate button
    if st.button("🔍 Calculate Risk-Reward", type="primary"):
        try:
            # Convert string inputs to float
            required_fields = [
                (avg_price_str, "Average Price"),
                (max_against_price_str, "Max Against Price"),
                (target_price_str, "Target Price"),
                (tick_size_str, "Tick Size"),
                (no_of_lots_str, "Number of Lots"),
                (tick_value_str, "Tick Value"),
                (total_lots_entry_exit_str, "Total Lots for Entry/Exit")
            ]
            
            # Check for empty required fields
            missing_fields = [name for value, name in required_fields if not value.strip()]
            
            if missing_fields:
                st.error(f"Please fill in the following required fields: {', '.join(missing_fields)}")
                return
            
            # Convert to float
            avg_price = float(avg_price_str)
            max_against_price = float(max_against_price_str)
            target_price = float(target_price_str)
            tick_size = float(tick_size_str)
            no_of_lots = float(no_of_lots_str)
            tick_value = float(tick_value_str)
            total_lots_entry_exit = float(total_lots_entry_exit_str)
            tc_per_lot = float(tc_per_lot_str) if tc_per_lot_str.strip() else 0.0
            rebate_per_lot = float(rebate_per_lot_str) if rebate_per_lot_str.strip() else 0.0
            
            # Additional validation
            if tick_size == 0:
                st.error("Tick size cannot be zero")
                return
                
        except ValueError as e:
            st.error("Please enter valid numbers in all fields. Check for any invalid characters.")
            return
        
        # Calculate risk and reward
        risk, reward = calculate_risk_reward(
            avg_price, max_against_price, target_price, tick_size,
            no_of_lots, tick_value, tc_per_lot, total_lots_entry_exit, rebate_per_lot
        )
        
        # Display results
        st.markdown("## 📊 Results")
        
        # Create three columns for results
        res_col1, res_col2, res_col3 = st.columns(3)
        
        with res_col1:
            st.metric(
                label="💀 Total Risk",
                value=format_currency(risk),
                delta=None
            )
        
        with res_col2:
            st.metric(
                label="💰 Total Reward", 
                value=format_currency(reward),
                delta=None
            )
        
        with res_col3:
            if risk != 0:
                ratio = abs(reward / risk)
                st.metric(
                    label="⚖️ Risk:Reward Ratio",
                    value=f"1:{ratio:.3f}",
                    delta=f"{'Good' if ratio >= 2 else 'Poor'}" if ratio >= 1 else "Bad"
                )
            else:
                st.metric(
                    label="⚖️ Risk:Reward Ratio",
                    value="N/A",
                    delta="Risk is zero"
                )
        
        # Detailed breakdown
        st.markdown("### 📋 Detailed Breakdown")
        
        # Calculate individual components
        price_movement_risk_value = abs(avg_price - max_against_price) / tick_size * no_of_lots * tick_value
        price_movement_reward_value = abs(avg_price - target_price) / tick_size * no_of_lots * tick_value
        transaction_cost_value = tc_per_lot * total_lots_entry_exit * 2 * no_of_lots
        rebate_value = rebate_per_lot * total_lots_entry_exit * 2 * no_of_lots
        
        # Create breakdown data
        breakdown_data = {
            'Component': [
                'Price Movement (Risk)',
                'Price Movement (Reward)', 
                'Transaction Costs',
                'Rebate Benefits',
                'Net Risk',
                'Net Reward'
            ],
            'Risk Calculation': [
                format_currency(price_movement_risk_value),
                "-",
                format_currency(transaction_cost_value),
                format_currency(-rebate_value),
                format_currency(risk),
                "-"
            ],
            'Reward Calculation': [
                "-",
                format_currency(price_movement_reward_value),
                format_currency(-transaction_cost_value),
                format_currency(rebate_value),
                "-",
                format_currency(reward)
            ]
        }
        
        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True)
        
        # Analysis insights
        st.markdown("### 💡 Analysis Insights")
        
        if risk != 0:
            ratio = abs(reward / risk)
            if ratio >= 3:
                st.success(f"✅ Excellent Risk-Reward ratio of 1:{ratio:.3f}! This is a very favorable trade setup.")
            elif ratio >= 2:
                st.success(f"✅ Good Risk-Reward ratio of 1:{ratio:.3f}. This trade has favorable odds.")
            elif ratio >= 1:
                st.warning(f"⚠️ Moderate Risk-Reward ratio of 1:{ratio:.3f}. Consider if the probability of success justifies this ratio.")
            else:
                st.error(f"❌ Poor Risk-Reward ratio of 1:{ratio:.3f}. This trade setup is not favorable.")
        else:
            st.info("ℹ️ Risk is zero - please verify your inputs.")
        
        # Additional insights
        st.markdown("#### 💼 Financial Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Maximum Loss**: {format_currency(risk)}")
            st.info(f"**Potential Profit**: {format_currency(reward)}")
        
        with col2:
            if risk > 0:
                profit_percentage = (reward / risk) * 100
                st.info(f"**Profit Potential**: {profit_percentage:.1f}% of risk")
            
            position_value = avg_price * no_of_lots
            if position_value > 0:
                risk_percentage = (risk / position_value) * 100
                st.info(f"**Risk as % of Position**: {risk_percentage:.2f}%")
    
    # Add information section
    with st.expander("ℹ️ How to Use This Tool"):
        st.markdown("""
        **Step 1:** Enter your position details (all values in USD):
        - **Average Price**: Your entry price in dollars
        - **Max Against Price**: Your stop-loss level in dollars
        - **Target Price**: Your profit target in dollars
        - **Tick Size**: Minimum price movement in dollars (e.g., 0.05 for some futures)
        
        **Step 2:** Configure position parameters:
        - **Number of Lots**: Your position size
        - **Tick Value**: Dollar value per tick (e.g., $25 for some contracts)
        - **Total Lots for Entry/Exit**: Usually same as number of lots
        
        **Step 3:** Add cost parameters (in USD):
        - **Transaction Cost per Lot**: Brokerage and charges per lot
        - **Rebate per Lot**: Any rebates you receive per lot
        
        **Step 4:** Click Calculate to get your Risk-Reward analysis!
        
        **Risk-Reward Interpretation:**
        - **1:3 or higher**: Excellent setup ✅
        - **1:2 to 1:3**: Good setup ✅
        - **1:1 to 1:2**: Moderate setup ⚠️
        - **Below 1:1**: Poor setup ❌
        
        **Example Values:**
        - Crypto: Price $0.008, Tick Size $0.001, Tick Value $1
        - Stocks: Price $150.50, Tick Size $0.01, Tick Value $1
        - Futures: Price $4200, Tick Size $0.25, Tick Value $12.50
        """)

if __name__ == "__main__":
    main()
