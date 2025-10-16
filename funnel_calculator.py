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
    
    h3 {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stNumberInput input, .stTextInput input {
        font-size: 0.9rem !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    
    .methodology {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    
    .formula {
        background: white;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        margin: 0.5rem 0;
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

# ========== METHODOLOGY SECTION ==========

with st.expander("📖 How This Works & Why You Can Trust It"):
    
    st.markdown("""
    ## Understanding the Calculations
    
    This calculator uses straightforward revenue projection formulas based on your actual funnel data. 
    Here's exactly what's happening behind the scenes:
    """)
    
    st.markdown("### 1. Drop-off Rate")
    st.markdown("""
    <div class='methodology'>
    <strong>What it measures:</strong> The percentage of users who leave at each funnel stage.
    
    <div class='formula'>
    Drop-off Rate = (Users at Stage N - Users at Stage N+1) / Users at Stage N × 100
    </div>
    
    <strong>Example:</strong> If 100,000 users land on your site and 75,000 view a product page:
    <ul>
    <li>Drop-off = 100,000 - 75,000 = 25,000 users</li>
    <li>Drop-off Rate = 25,000 / 100,000 × 100 = 25%</li>
    </ul>
    
    <strong>Why it matters:</strong> High drop-off rates (>50%) indicate major friction points that need attention.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 2. Revenue Lost")
    st.markdown("""
    <div class='methodology'>
    <strong>What it measures:</strong> Potential revenue you're missing from users who drop off.
    
    <div class='formula'>
    Revenue Lost = Drop-off Users × Overall Conversion Rate × AOV
    </div>
    
    <strong>Example:</strong> Using the 25,000 drop-offs from above:
    <ul>
    <li>Overall conversion rate = 2.3% (2,300 purchases / 100,000 visitors)</li>
    <li>AOV = $95</li>
    <li>Lost Revenue = 25,000 × 0.023 × $95 = $54,625</li>
    </ul>
    
    <strong>The logic:</strong> We assume drop-offs would convert at the same rate as users who stayed in the funnel. 
    This is conservative—many drop-offs were likely less qualified—but gives you a realistic revenue opportunity estimate.
    
    <strong>Why it matters:</strong> Translates user behavior into dollars, making it easier to prioritize fixes.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 3. What-If Scenarios")
    st.markdown("""
    <div class='methodology'>
    <strong>What it measures:</strong> Revenue impact if you improve a specific stage's conversion rate.
    
    <div class='formula'>
    Additional Revenue = Stage Users × Improvement % × Overall CR × AOV
    </div>
    
    <strong>Example:</strong> Improving "Product Page → Add to Cart" by 10%:
    <ul>
    <li>75,000 users at Product Page stage</li>
    <li>10% improvement = 7,500 more users advancing</li>
    <li>7,500 × 0.023 (overall CR) × $95 (AOV) = $16,387/month</li>
    <li>Annual impact = $16,387 × 12 = $196,650</li>
    </ul>
    
    <strong>Why it matters:</strong> Helps you model ROI before investing in optimizations. A 10% improvement might require 
    testing budget, dev resources, or agency help—this shows if the juice is worth the squeeze.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("## Why You Can Trust This")
    
    st.markdown("""
    ### Proven Methodology
    
    These calculations use standard e-commerce funnel analysis methods employed by:
    - **Growth teams at scale-ups** (Shopify merchants, DTC brands)
    - **CRO agencies** (ConversionXL, Speero, CXL Institute)
    - **Product analytics platforms** (Amplitude, Mixpanel, Google Analytics)
    
    This isn't proprietary math—it's how conversion optimization has been done for 20+ years.
    """)
    
    st.markdown("""
    ### Conservative Assumptions
    
    The calculator makes conservative estimates:
    
    1. **Drop-offs convert at overall rate** — In reality, some drop-offs were never going to buy, 
    so actual revenue loss might be lower. But this gives you the "best case" opportunity.
    
    2. **Linear improvements** — A 10% improvement doesn't account for diminishing returns or 
    compounding effects across the funnel. Real results may vary.
    
    3. **Monthly projections** — We assume consistent traffic month-over-month. Seasonal businesses 
    should adjust expectations accordingly.
    """)
    
    st.markdown("""
    ### What This Tells You
    
    **This calculator is for prioritization, not prediction.**
    
    ✅ **Use it to:**
    - Identify which funnel stages have the biggest revenue opportunity
    - Estimate the value of fixing specific friction points
    - Build business cases for CRO investments
    - Compare optimization opportunities across your funnel
    
    ❌ **Don't use it to:**
    - Guarantee specific revenue outcomes (testing is required)
    - Replace actual A/B test analysis
    - Make exact financial projections for stakeholders
    """)
    
    st.markdown("---")
    
    st.markdown("## Example Use Case")
    
    st.markdown("""
    **Scenario:** E-commerce jewelry brand with $95 AOV
    
    **Funnel data reveals:**
    - Homepage → PDP has 25% drop-off ($54K lost revenue)
    - **PDP → Add to Cart has 89% drop-off ($6.3M lost revenue)** 🔴
    - Cart → Checkout has 50% drop-off ($380K lost revenue)
    
    **Insight:** The Product Page is the massive leak. Even though homepage and checkout need work, 
    fixing PDP → ATC has 10x the revenue impact.
    
    **What-if modeling shows:** A 10% improvement in ATC rate would generate +$34,675/month (+$416K annually).
    
    **Action taken:** Team prioritizes:
    1. Trust signals on PDPs (reviews, guarantees, social proof)
    2. Pricing clarity (no hidden fees)
    3. Better product photography
    4. Clearer shipping info
    
    **Result:** After 3 months of testing, ATC rate improved 8.5%, generating +$29,500/month in additional revenue.
    
    This calculator helped them identify the right problem to solve.
    """)
    
    st.markdown("---")
    
    st.markdown("## Limitations & Caveats")
    
    st.markdown("""
    **This calculator cannot:**
    
    - **Account for traffic quality differences** — If 50% of your traffic is bots or irrelevant visitors, 
    the revenue loss estimates will be inflated.
    
    - **Model complex user journeys** — Assumes a linear funnel. Real users bounce between stages, 
    return days later, or use multiple devices.
    
    - **Predict test outcomes** — Just because a stage has high revenue loss doesn't mean it's easy to fix. 
    Some friction is intentional (price filtering) or hard to address (product-market fit).
    
    - **Replace proper analytics** — This is a directional tool. For detailed analysis, use your 
    analytics platform's funnel reports with segmentation by source, device, cohort, etc.
    
    **Best practice:** Use this calculator for initial prioritization, then validate opportunities with 
    qualitative research (session recordings, user interviews) before committing to expensive optimizations.
    """)
    
    st.markdown("---")
    
    st.markdown("## Questions?")
    
    st.markdown("""
    **"Why do you calculate revenue lost using overall conversion rate instead of stage-specific rates?"**
    
    Because we're estimating opportunity, not certainty. Using the overall conversion rate (final purchases / 
    total visitors) is conservative and accounts for the fact that not everyone who advances will ultimately buy. 
    Stage-specific rates would overstate the opportunity.
    
    ---
    
    **"Shouldn't improvements compound through the funnel?"**
    
    Yes! In reality, improving an early stage means more users flow through later stages, creating a multiplier effect. 
    This calculator shows the direct impact of one stage improvement in isolation. The actual business impact could be higher.
    
    ---
    
    **"Can I use this for B2B or lead gen funnels?"**
    
    Yes! Just replace AOV with your average customer lifetime value (LTV) or average deal size. The math works the same way.
    
    ---
    
    **"How often should I recalculate this?"**
    
    Monthly at minimum, or whenever you ship major changes. Funnel performance shifts with seasonality, product 
    mix, traffic sources, and site updates. Tracking changes over time helps you catch issues early.
    """)

st.divider()

st.caption("Built by [Roberto Bahia](https://linkedin.com/in/roberto-bahia) | [GitHub](https://github.com/robertoroiebahia)")
