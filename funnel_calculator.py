import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Funnel Calculator",
    page_icon="📊",
    layout="centered"
)

# Simple CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1 {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.25rem !important;
    }
    
    h2 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    .stNumberInput input, .stTextInput input {
        font-size: 0.9rem !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Funnel Calculator")
st.caption("See where revenue is leaking and what improvements are worth")

st.divider()

# Quick Config
col1, col2 = st.columns(2)
with col1:
    aov = st.number_input("Avg Order Value ($)", value=95.0, step=5.0)
with col2:
    num_stages = st.number_input("# of Stages", min_value=3, max_value=8, value=5)

st.divider()

# Funnel Stages - Simple Input
st.subheader("Funnel Stages")

stages = []
defaults = [
    ("Landing Page", 100000),
    ("Product Page", 75000),
    ("Add to Cart", 8000),
    ("Checkout", 4000),
    ("Purchase", 2300)
]

for i in range(num_stages):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(
            f"Stage {i+1}",
            value=defaults[i][0] if i < len(defaults) else f"Stage {i+1}",
            key=f"name_{i}",
            label_visibility="collapsed"
        )
    with col2:
        if i == 0:
            users = st.number_input(
                "Users",
                value=defaults[i][1] if i < len(defaults) else 10000,
                step=1000,
                key=f"users_{i}",
                label_visibility="collapsed"
            )
        else:
            max_val = stages[-1]['users']
            default_val = defaults[i][1] if i < len(defaults) else int(max_val * 0.5)
            users = st.number_input(
                "Users",
                max_value=max_val,
                value=min(default_val, max_val),
                step=100,
                key=f"users_{i}",
                label_visibility="collapsed"
            )
    
    conv_rate = (users / stages[-1]['users'] * 100) if i > 0 and stages else 100
    stages.append({'name': name, 'users': users, 'rate': conv_rate})

st.divider()

# Quick Metrics
overall_cr = (stages[-1]['users'] / stages[0]['users'] * 100)
current_rev = stages[-1]['users'] * aov

col1, col2, col3 = st.columns(3)
col1.metric("Conversion", f"{overall_cr:.1f}%")
col2.metric("Revenue", f"${current_rev:,.0f}")
col3.metric("Drop-offs", f"{stages[0]['users'] - stages[-1]['users']:,}")

st.divider()

# Funnel Chart
fig = go.Figure(go.Funnel(
    y=[s['name'] for s in stages],
    x=[s['users'] for s in stages],
    textinfo="value+percent initial",
    marker={"color": ["#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe", "#dbeafe"][:num_stages]}
))

fig.update_layout(
    height=300,
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# Revenue Analysis Table
st.subheader("Revenue Impact")

final_cr = stages[-1]['users'] / stages[0]['users']
data = []

for i in range(len(stages) - 1):
    drop = stages[i]['users'] - stages[i+1]['users']
    drop_pct = (drop / stages[i]['users'] * 100)
    lost_rev = drop * final_cr * aov
    
    data.append({
        'Stage': f"{stages[i]['name']} → {stages[i+1]['name']}",
        'Drop-off': f"{drop:,} ({drop_pct:.0f}%)",
        'Revenue Lost': f"${lost_rev:,.0f}"
    })

st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

st.divider()

# What-If (Compact)
st.subheader("What-If")

col1, col2 = st.columns(2)
with col1:
    stage_idx = st.selectbox("Stage", range(len(stages)-1), format_func=lambda x: f"{stages[x]['name']} → {stages[x+1]['name']}")
with col2:
    improvement = st.slider("Improve by", 1, 50, 10, 5)

# Calculate
improved = stages[stage_idx]['users'] * (improvement / 100) * final_cr * aov
annual = improved * 12

col1, col2 = st.columns(2)
col1.metric("Monthly Impact", f"${improved:,.0f}")
col2.metric("Annual Impact", f"${annual:,.0f}")

st.caption(f"A {improvement}% improvement at {stages[stage_idx]['name']} → {stages[stage_idx+1]['name']} would generate ${improved:,.0f}/mo")

st.divider()

st.caption("Built by [Roberto Bahia](https://linkedin.com/in/roberto-bahia)")
