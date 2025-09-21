import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config with custom styling
st.set_page_config(
    page_title="Solar Energy Estimator", 
    page_icon="☀️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #ff7b00, #ffcd3c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    .input-section {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .results-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #ff7b00, #ffcd3c);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 30px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 123, 0, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<h1 class="main-header">☀️ Solar Energy Potential Estimator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover your solar power potential, savings, and return on investment with advanced analytics</p>', unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["🏠 Basic Analysis", "📊 Advanced Metrics", "💡 Tips & Info"])

with tab1:
    # Input section with better styling
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 🔧 System Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        area = st.number_input(
            "🏠 Rooftop Area (m²)", 
            min_value=10, 
            max_value=1000, 
            value=100,
            help="Available rooftop space for solar panels"
        )
        
    with col2:
        irradiance = st.slider(
            "☀️ Solar Irradiance (kWh/m²/day)", 
            min_value=3.0, 
            max_value=7.0, 
            value=5.5, 
            step=0.1,
            help="Daily solar energy received per square meter"
        )
        
    with col3:
        tariff = st.number_input(
            "⚡ Electricity Tariff (₹/kWh)", 
            min_value=3.0, 
            max_value=15.0, 
            value=6.5, 
            step=0.1,
            help="Current electricity rate you pay"
        )
    
    # Advanced options in expander
    with st.expander("⚙️ Advanced Settings"):
        col1, col2 = st.columns(2)
        with col1:
            panel_efficiency = st.slider("Panel Efficiency (%)", 15, 25, 20, 1)
            system_losses = st.slider("System Losses (%)", 10, 25, 15, 1)
        with col2:
            installation_cost = st.number_input("Installation Cost (₹/kW)", 40000, 80000, 65000, 1000)
            maintenance_cost = st.number_input("Annual Maintenance (₹)", 2000, 8000, 4000, 500)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate button
    if st.button("🔍 Calculate Solar Potential", type="primary"):
        # Enhanced calculations
        performance_ratio = (100 - system_losses) / 100
        annual_output = area * irradiance * 365 * performance_ratio * (panel_efficiency/20)
        annual_savings = annual_output * tariff
        total_system_cost = (annual_output / 1000) * installation_cost
        net_annual_savings = annual_savings - maintenance_cost
        payback = total_system_cost / net_annual_savings if net_annual_savings > 0 else 0
        co2_reduction = annual_output * 0.82  # kg CO2 per kWh
        
        # Results section
        st.markdown('<div class="results-section">', unsafe_allow_html=True)
        st.markdown("### 📈 Your Solar Analysis Results")
        
        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="⚡ Annual Output",
                value=f"{annual_output:,.0f} kWh",
                delta=f"{annual_output/365:.1f} kWh/day"
            )
            
        with col2:
            st.metric(
                label="💰 Annual Savings",
                value=f"₹{annual_savings:,.0f}",
                delta=f"₹{annual_savings/12:,.0f}/month"
            )
            
        with col3:
            st.metric(
                label="⏳ Payback Period",
                value=f"{payback:.1f} years",
                delta="ROI Timeline"
            )
            
        with col4:
            st.metric(
                label="🌱 CO₂ Reduction",
                value=f"{co2_reduction:,.0f} kg/year",
                delta="Environmental Impact"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Visual gauges
        col1, col2 = st.columns(2)
        
        with col1:
            # Solar potential gauge
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = min(100, (annual_output/area) * 10),
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Solar Potential Score"},
                delta = {'reference': 50},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "orange"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with col2:
            # ROI Timeline
            years = list(range(1, int(payback) + 5))
            cumulative_savings = [(year * net_annual_savings - total_system_cost) for year in years]
            
            fig_roi = go.Figure()
            fig_roi.add_trace(go.Scatter(
                x=years,
                y=cumulative_savings,
                mode='lines+markers',
                name='Cumulative Savings',
                line=dict(color='green', width=3),
                fill='tozeroy'
            ))
            fig_roi.add_hline(y=0, line_dash="dash", line_color="red")
            fig_roi.update_layout(
                title="Return on Investment Timeline",
                xaxis_title="Years",
                yaxis_title="Cumulative Savings (₹)",
                height=300
            )
            st.plotly_chart(fig_roi, use_container_width=True)

with tab2:
    st.markdown("### 📊 Detailed Financial Analysis")
    
    if 'annual_output' in locals():
        # Monthly breakdown
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        seasonal_variation = [0.8, 0.9, 1.1, 1.2, 1.3, 1.2, 1.1, 1.1, 1.0, 0.9, 0.8, 0.7]
        monthly_output = [annual_output/12 * var for var in seasonal_variation]
        monthly_savings = [output * tariff for output in monthly_output]
        
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Bar(
            x=months,
            y=monthly_output,
            name='Energy Output (kWh)',
            marker_color='orange'
        ))
        fig_monthly.update_layout(
            title="Monthly Energy Production Estimate",
            xaxis_title="Month",
            yaxis_title="Energy Output (kWh)",
            height=400
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
        
        # Financial breakdown table
        st.markdown("### 💹 Financial Summary")
        financial_data = {
            'Parameter': [
                'System Size (kW)',
                'Total Installation Cost (₹)',
                'Annual Energy Output (kWh)',
                'Annual Savings (₹)',
                'Annual Maintenance (₹)',
                'Net Annual Benefit (₹)',
                'Payback Period (years)',
                '25-Year Total Savings (₹)'
            ],
            'Value': [
                f"{annual_output/1000:.1f}",
                f"₹{total_system_cost:,.0f}",
                f"{annual_output:,.0f}",
                f"₹{annual_savings:,.0f}",
                f"₹{maintenance_cost:,.0f}",
                f"₹{net_annual_savings:,.0f}",
                f"{payback:.1f}",
                f"₹{(net_annual_savings * 25 - total_system_cost):,.0f}"
            ]
        }
        st.table(financial_data)

with tab3:
    st.markdown("### 💡 Solar Energy Tips & Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🏠 Optimal Conditions
        - **Roof Direction**: South-facing roofs are ideal
        - **Tilt Angle**: 15-30° for maximum efficiency
        - **Shading**: Minimize shadows from trees/buildings
        - **Roof Age**: Ensure roof can support panels for 25+ years
        """)
        
        st.markdown("""
        #### 💰 Financial Benefits
        - **Government Subsidies**: Up to 40% subsidy available
        - **Net Metering**: Sell excess power back to grid
        - **Tax Benefits**: Depreciation advantages for businesses
        - **Property Value**: Increases property value by 3-4%
        """)
    
    with col2:
        st.markdown("""
        #### 🌱 Environmental Impact
        - **Carbon Footprint**: Typical system saves 1-2 tons CO₂/year
        - **Energy Independence**: Reduce dependence on fossil fuels
        - **Clean Energy**: Zero emissions during operation
        - **Sustainability**: 25-30 year lifespan
        """)
        
        st.markdown("""
        #### ⚡ Technical Considerations
        - **Panel Types**: Monocrystalline, Polycrystalline, Thin-film
        - **Inverters**: String vs. Power optimizers vs. Microinverters
        - **Monitoring**: Track system performance remotely
        - **Maintenance**: Minimal - mostly cleaning and inspections
        """)
    
    # Interactive irradiance map info
    st.markdown("### 🗺️ India Solar Irradiance Guide")
    irradiance_data = {
        'Region': ['Rajasthan', 'Gujarat', 'Karnataka', 'Andhra Pradesh', 'Tamil Nadu', 'Maharashtra', 'Punjab', 'Haryana'],
        'Average Irradiance (kWh/m²/day)': [6.2, 5.8, 5.5, 5.4, 5.2, 5.0, 4.8, 4.6],
        'Potential': ['Excellent', 'Excellent', 'Very Good', 'Very Good', 'Good', 'Good', 'Good', 'Moderate']
    }
    st.table(irradiance_data)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌟 Start your solar journey today and contribute to a sustainable future! 🌟</p>
    <p><small>Calculations are estimates. Consult with solar professionals for detailed assessments.</small></p>
</div>
""", unsafe_allow_html=True)