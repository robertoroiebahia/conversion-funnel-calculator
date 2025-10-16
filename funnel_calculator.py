import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Conversion Funnel Loss Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    h1 {
        color: white !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
    }
    
    .subtitle {
        color: rgba(255,255,255,0.95);
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
    }
    
    .stNumberInput input {
        border-radius: 8px !important;
        border: 2px solid #e2e8f0 !important;
    }
    
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent) !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>📊 Conversion Funnel Loss Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>See exactly where revenue is leaking and what each improvement is worth</p>", unsafe_allow_html=True)

st.markdown("---")

# Input Section
st.markdown("## ⚙️ Configure Your Funnel")

col1, col2 = st.columns(2)

with col1:
    aov = st.number_input("Average Order Value ($)", min_value=0.01, value=95.00, step=1.00)

with col2:
    num_stages = st.number_input("Number of Funnel Stages", min_value=3, max_value=10, value=5, step=1)

st.markdown("---")

# Dynamic stage inputs
st.markdown("## 📈 Funnel Stages")

stages = []
stage_names = ["Homepage/Landing", "Product Page View", "Add to Cart", "Checkout Begin", "Purchase"]

for i in range(num_stages):
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            default_name = stage_names[i] if i < len(stage_names) else f"Stage {i+1}"
            stage_name = st.text_input(
                f"Stage {i+1} Name", 
                value=default_name,
                key=f"stage_name_{i}"
            )
        
        with col2:
            if i == 0:
                users = st.number_input(
                    "Users at this stage",
                    min_value=1,
                    value=100000,
                    step=1000,
                    key=f"users_{i}"
                )
            else:
                users = st.number_input(
                    "Users at this stage",
                    min_value=0,
                    max_value=stages[i-1]['users'],
                    value=min(stages[i-1]['users'] // 2, stages[i-1]['users']),
                    step=100,
                    key=f"users_{i}"
                )
        
        # Calculate conversion rate from previous stage
        if i > 0:
            conv_rate = (users / stages[i-1]['users'] * 100) if stages[i-1]['users'] > 0 else 0
        else:
            conv_rate = 100
        
        stages.append({
            'name': stage_name,
            'users': users,
            'conversion_rate': conv_rate
        })
        
        if i < num_stages - 1:
            st.markdown("")

st.markdown("---")

# Calculate losses
def calculate_funnel_metrics(stages, aov):
    results = []
    
    for i in range(len(stages) - 1):
        current_stage = stages[i]
        next_stage = stages[i + 1]
        
        drop_off_users = current_stage['users'] - next_stage['users']
        drop_off_rate = (drop_off_users / current_stage['users'] * 100) if current_stage['users'] > 0 else 0
        
        # Assume drop-offs would have same conversion rate as those who made it through
        final_conversion_rate = stages[-1]['users'] / stages[0]['users'] if stages[0]['users'] > 0 else 0
        estimated_lost_purchases = drop_off_users * final_conversion_rate
        revenue_lost = estimated_lost_purchases * aov
        
        # Value of 1% improvement
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

# Display Results
st.markdown("## 💰 Revenue Loss Analysis")

metrics = calculate_funnel_metrics(stages, aov)

# Summary metrics
total_revenue_lost = sum(m['revenue_lost'] for m in metrics)
total_potential_customers = stages[0]['users'] - stages[-1]['users']
overall_conversion = (stages[-1]['users'] / stages[0]['users'] * 100) if stages[0]['users'] > 0 else 0

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("Overall Conversion Rate", f"{overall_conversion:.2f}%")

with metric_col2:
    st.metric("Total Drop-offs", f"{total_potential_customers:,}")

with metric_col3:
    st.metric("Estimated Revenue Lost", f"${total_revenue_lost:,.0f}")

with metric_col4:
    potential_revenue = stages[0]['users'] * aov * overall_conversion / 100
    st.metric("Current Revenue", f"${potential_revenue:,.0f}")

st.markdown("---")

# Funnel Visualization
st.markdown("## 🔍 Funnel Visualization")

fig = go.Figure()

# Create funnel chart
fig.add_trace(go.Funnel(
    name='Users',
    y=[stage['name'] for stage in stages],
    x=[stage['users'] for stage in stages],
    textposition="inside",
    textinfo="value+percent initial",
    marker={
        "color": ["#667eea", "#7c8ff0", "#92a0f5", "#a8b1f9", "#bec2fc"][:num_stages],
        "line": {"width": 2, "color": "white"}
    },
    connector={"line": {"color": "#cbd5e1", "dash": "dot", "width": 3}}
))

fig.update_layout(
    title={
        'text': "Conversion Funnel",
        'font': {'size': 20, 'color': '#1e293b', 'family': 'Inter'}
    },
    paper_bgcolor='white',
    plot_bgcolor='white',
    height=400,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Detailed Loss Table
st.markdown("## 📊 Stage-by-Stage Revenue Impact")

df_metrics = pd.DataFrame([
    {
        'Transition': f"{m['from_stage']} → {m['to_stage']}",
        'Drop-off Users': f"{m['drop_off_users']:,}",
        'Drop-off Rate': f"{m['drop_off_rate']:.1f}%",
        'Revenue Lost': f"${m['revenue_lost']:,.0f}",
        'Value of 1% Improvement': f"${m['one_percent_value']:,.0f}"
    }
    for m in metrics
])

st.dataframe(df_metrics, use_container_width=True, hide_index=True)

st.markdown("---")

# What-If Calculator
st.markdown("## 🎯 What-If Scenario Calculator")

st.markdown("See what happens if you improve a specific funnel stage:")

scenario_col1, scenario_col2, scenario_col3 = st.columns(3)

with scenario_col1:
    stage_options = [f"{m['from_stage']} → {m['to_stage']}" for m in metrics]
    selected_stage_idx = st.selectbox("Select Stage to Improve", range(len(stage_options)), format_func=lambda x: stage_options[x])

with scenario_col2:
    improvement_pct = st.slider("Improvement (%)", min_value=1, max_value=50, value=10, step=1)

with scenario_col3:
    time_period = st.selectbox("Time Period", ["Monthly", "Quarterly", "Annually"])

# Calculate scenario
selected_metric = metrics[selected_stage_idx]
current_stage = stages[selected_stage_idx]

improved_users = current_stage['users'] * (improvement_pct / 100)
final_conversion_rate = stages[-1]['users'] / stages[0]['users'] if stages[0]['users'] > 0 else 0
additional_purchases = improved_users * final_conversion_rate
additional_revenue = additional_purchases * aov

# Time period multiplier
multiplier = {"Monthly": 1, "Quarterly": 3, "Annually": 12}[time_period]
projected_revenue = additional_revenue * multiplier

st.markdown("")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.metric("Additional Users", f"+{improved_users:,.0f}")

with result_col2:
    st.metric("Additional Purchases", f"+{additional_purchases:,.0f}")

with result_col3:
    st.metric(f"{time_period} Revenue Lift", f"${projected_revenue:,.0f}")

with result_col4:
    roi_potential = (projected_revenue / additional_revenue - 1) * 100 if time_period != "Monthly" else 0
    st.metric("Time Period Multiplier", f"{multiplier}x")

# Success message with the scenario
st.success(f"""
**Scenario Summary:**  
If you improve the **{selected_metric['from_stage']} → {selected_metric['to_stage']}** conversion rate by **{improvement_pct}%**, you would gain:
- **{additional_purchases:,.0f}** more purchases per month
- **${additional_revenue:,.0f}** in additional monthly revenue
- **${projected_revenue:,.0f}** in total {time_period.lower()} revenue

This represents a **{improvement_pct}%** improvement on a stage that currently converts at **{100 - selected_metric['drop_off_rate']:.1f}%**.
""")

st.markdown("---")

# Pro Tips
st.info("""
**💡 How to Use This Data:**

1. **Focus on the biggest leaks** — Stages with the highest revenue lost or highest drop-off rates
2. **Quick wins vs. big bets** — Balance high-impact stages with ease of implementation
3. **Start with qualitative research** — Use heatmaps, session recordings, and user interviews to understand WHY users drop off
4. **A/B test improvements** — Don't just ship changes; validate with proper testing
5. **Monitor over time** — Track funnel changes monthly to catch issues early

**🎯 Where to Focus:**
- Drop-off rates >50% indicate major friction
- High-volume stages (earlier in funnel) have biggest absolute impact
- High-percentage improvements on low-converting stages often easier to achieve
""")

st.markdown("---")

st.markdown("""
<div style='text-align: center; color: white; padding: 1rem;'>
    <p>Built by <a href='https://www.linkedin.com/in/roberto-bahia/' style='color: white; text-decoration: underline;'>Roberto Bahia</a> | 
    <a href='https://github.com/robertoroiebahia' style='color: white; text-decoration: underline;'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)
