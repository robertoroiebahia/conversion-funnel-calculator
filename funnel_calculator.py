import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Conversion Funnel Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Clean, Professional Style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: #f8fafc;
    }
    
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
    }
    
    /* Headers */
    h1 {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em;
    }
    
    h2 {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin-top: 2.5rem !important;
        margin-bottom: 1rem !important;
        letter-spacing: -0.01em;
    }
    
    h3 {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 1.125rem !important;
        margin-top: 1.5rem !important;
    }
    
    .subtitle {
        color: #64748b;
        font-size: 1.125rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
    }
    
    /* Input Fields */
    .stNumberInput input, .stTextInput input {
        border-radius: 6px !important;
        border: 1px solid #e2e8f0 !important;
        font-size: 0.9375rem !important;
        padding: 0.625rem !important;
        background: white !important;
    }
    
    .stNumberInput input:focus, .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stNumberInput label, .stTextInput label {
        font-weight: 500 !important;
        color: #334155 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.375rem !important;
    }
    
    /* Select boxes */
    .stSelectbox label {
        font-weight: 500 !important;
        color: #334155 !important;
        font-size: 0.875rem !important;
    }
    
    /* Slider */
    .stSlider label {
        font-weight: 500 !important;
        color: #334155 !important;
        font-size: 0.875rem !important;
    }
    
    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }
    
    /* Info/Success boxes */
    .stAlert {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        background: white !important;
        padding: 1.25rem !important;
    }
    
    .stSuccess {
        background: #f0fdf4 !important;
        border-color: #86efac !important;
    }
    
    .stInfo {
        background: #eff6ff !important;
        border-color: #93c5fd !important;
    }
    
    /* Dividers */
    hr {
        margin: 2.5rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: #e2e8f0 !important;
    }
    
    /* Containers */
    [data-testid="column"] {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Remove default streamlit branding colors */
    .stApp {
        background: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>Conversion Funnel Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Identify revenue leaks and prioritize optimization opportunities</p>", unsafe_allow_html=True)

st.markdown("---")

# Configuration Section
st.markdown("## Configuration")

config_container = st.container()
with config_container:
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        aov = st.number_input(
            "Average Order Value ($)", 
            min_value=0.01, 
            value=95.00, 
            step=1.00,
            help="The average revenue per transaction"
        )
    
    with col2:
        num_stages = st.number_input(
            "Funnel Stages", 
            min_value=3, 
            max_value=10, 
            value=5, 
            step=1,
            help="Number of stages in your conversion funnel"
        )
    
    with col3:
        st.markdown("")

st.markdown("---")

# Funnel Stage Inputs
st.markdown("## Funnel Data")

stages = []
stage_names = ["Homepage/Landing", "Product Page View", "Add to Cart", "Checkout Begin", "Purchase"]

for i in range(num_stages):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        default_name = stage_names[i] if i < len(stage_names) else f"Stage {i+1}"
        stage_name = st.text_input(
            f"Stage {i+1}",
            value=default_name,
            key=f"stage_name_{i}",
            label_visibility="collapsed"
        )
    
    with col2:
        if i == 0:
            users = st.number_input(
                "Users",
                min_value=1,
                value=100000,
                step=1000,
                key=f"users_{i}",
                label_visibility="collapsed"
            )
        else:
            max_users = stages[i-1]['users']
            default_users = int(max_users * 0.7) if i == 1 else int(max_users * 0.5)
            users = st.number_input(
                "Users",
                min_value=0,
                max_value=max_users,
                value=min(default_users, max_users),
                step=100,
                key=f"users_{i}",
                label_visibility="collapsed"
            )
    
    if i > 0:
        conv_rate = (users / stages[i-1]['users'] * 100) if stages[i-1]['users'] > 0 else 0
    else:
        conv_rate = 100
    
    stages.append({
        'name': stage_name,
        'users': users,
        'conversion_rate': conv_rate
    })

st.markdown("---")

# Calculate metrics
def calculate_funnel_metrics(stages, aov):
    results = []
    
    for i in range(len(stages) - 1):
        current_stage = stages[i]
        next_stage = stages[i + 1]
        
        drop_off_users = current_stage['users'] - next_stage['users']
        drop_off_rate = (drop_off_users / current_stage['users'] * 100) if current_stage['users'] > 0 else 0
        
        final_conversion_rate = stages[-1]['users'] / stages[0]['users'] if stages[0]['users'] > 0 else 0
        estimated_lost_purchases = drop_off_users * final_conversion_rate
        revenue_lost = estimated_lost_purchases * aov
        
        one_percent_users = current_stage['users'] * 0.01
        one_percent_purchases = one_percent_users * final_conversion_rate
        one_percent_value = one_percent_purchases * aov
        
        results.append({
            'from_stage': current_stage['name'],
            'to_stage': next_stage['name'],
            'drop_off_users': drop_off_users,
            'drop_off_rate': drop_off_rate,
            'revenue_lost': revenue_lost,
            'one_percent_value': one_percent_value
        })
    
    return results

# Analysis Section
st.markdown("## Performance Summary")

metrics = calculate_funnel_metrics(stages, aov)

total_revenue_lost = sum(m['revenue_lost'] for m in metrics)
total_potential_customers = stages[0]['users'] - stages[-1]['users']
overall_conversion = (stages[-1]['users'] / stages[0]['users'] * 100) if stages[0]['users'] > 0 else 0
current_revenue = stages[-1]['users'] * aov

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("Conversion Rate", f"{overall_conversion:.2f}%")

with metric_col2:
    st.metric("Current Revenue", f"${current_revenue:,.0f}")

with metric_col3:
    st.metric("Total Drop-offs", f"{total_potential_customers:,}")

with metric_col4:
    st.metric("Revenue at Risk", f"${total_revenue_lost:,.0f}")

st.markdown("---")

# Funnel Visualization
st.markdown("## Funnel Visualization")

fig = go.Figure()

fig.add_trace(go.Funnel(
    name='Conversion Funnel',
    y=[stage['name'] for stage in stages],
    x=[stage['users'] for stage in stages],
    textposition="inside",
    textinfo="value+percent initial",
    marker={
        "color": ["#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe", "#dbeafe"][:num_stages],
        "line": {"width": 0}
    },
    connector={"line": {"color": "#cbd5e1", "width": 2}}
))

fig.update_layout(
    paper_bgcolor='white',
    plot_bgcolor='white',
    height=400,
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(family='Inter', size=13, color='#334155')
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Revenue Impact Analysis
st.markdown("## Revenue Impact by Stage")

df_metrics = pd.DataFrame([
    {
        'Stage Transition': f"{m['from_stage']} → {m['to_stage']}",
        'Users Lost': f"{m['drop_off_users']:,}",
        'Drop-off Rate': f"{m['drop_off_rate']:.1f}%",
        'Revenue Lost': f"${m['revenue_lost']:,.0f}",
        'Value of 1% Improvement': f"${m['one_percent_value']:,.0f}"
    }
    for m in metrics
])

st.dataframe(df_metrics, use_container_width=True, hide_index=True)

st.markdown("---")

# Scenario Planning
st.markdown("## Scenario Planning")

st.markdown("Model the revenue impact of improving a specific funnel stage.")

scenario_col1, scenario_col2, scenario_col3 = st.columns(3)

with scenario_col1:
    stage_options = [f"{m['from_stage']} → {m['to_stage']}" for m in metrics]
    selected_stage_idx = st.selectbox(
        "Stage to Improve",
        range(len(stage_options)),
        format_func=lambda x: stage_options[x]
    )

with scenario_col2:
    improvement_pct = st.slider(
        "Improvement (%)",
        min_value=1,
        max_value=50,
        value=10,
        step=1
    )

with scenario_col3:
    time_period = st.selectbox(
        "Time Period",
        ["Monthly", "Quarterly", "Annually"]
    )

# Calculate scenario
selected_metric = metrics[selected_stage_idx]
current_stage = stages[selected_stage_idx]

improved_users = current_stage['users'] * (improvement_pct / 100)
final_conversion_rate = stages[-1]['users'] / stages[0]['users'] if stages[0]['users'] > 0 else 0
additional_purchases = improved_users * final_conversion_rate
additional_revenue = additional_purchases * aov

multiplier = {"Monthly": 1, "Quarterly": 3, "Annually": 12}[time_period]
projected_revenue = additional_revenue * multiplier

st.markdown("")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.metric("Additional Conversions", f"+{improved_users:,.0f}")

with result_col2:
    st.metric("Additional Purchases", f"+{additional_purchases:,.0f}")

with result_col3:
    st.metric(f"{time_period} Revenue", f"${projected_revenue:,.0f}")

with result_col4:
    revenue_lift_pct = (projected_revenue / current_revenue * 100) if current_revenue > 0 else 0
    st.metric("Revenue Lift", f"+{revenue_lift_pct:.1f}%")

st.markdown("")

# Summary box
st.success(f"""
**Impact Summary**

Improving **{selected_metric['from_stage']} → {selected_metric['to_stage']}** by **{improvement_pct}%** would generate:

- **{additional_purchases:,.0f}** additional monthly purchases  
- **${additional_revenue:,.0f}** in additional monthly revenue  
- **${projected_revenue:,.0f}** in total {time_period.lower()} revenue  

Current conversion rate at this stage: **{100 - selected_metric['drop_off_rate']:.1f}%**
""")

st.markdown("---")

# Recommendations
st.markdown("## Optimization Priorities")

st.info("""
**Focus Areas (Ranked by Revenue Impact):**

1. **Highest Revenue Loss** — Address stages with the largest dollar impact first
2. **Highest Drop-off Rates** — Stages with >50% drop-off indicate major friction points
3. **Early Funnel Issues** — Improving top-of-funnel stages affects all downstream conversion
4. **Quick Wins** — Balance high-impact changes with ease of implementation

**Next Steps:**

- Conduct qualitative research (heatmaps, session recordings, user interviews) to identify why users drop off  
- Prioritize A/B tests based on potential revenue impact and implementation effort  
- Monitor funnel performance monthly to catch issues early  
- Focus on one stage at a time to isolate the impact of changes
""")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 2rem 0 1rem 0; font-size: 0.875rem;'>
    Built by <a href='https://www.linkedin.com/in/roberto-bahia/' style='color: #3b82f6; text-decoration: none;'>Roberto Bahia</a> | 
    <a href='https://github.com/robertoroiebahia' style='color: #3b82f6; text-decoration: none;'>GitHub</a>
</div>
""", unsafe_allow_html=True)
