# Conversion Funnel Loss Calculator

Calculate exactly where revenue is leaking in your conversion funnel and what each improvement is worth. Built for CRO professionals, growth teams, and e-commerce businesses.

**[🚀 Live Demo](#)** *(Coming soon - will deploy to Streamlit Cloud)*

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.18+-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

- **Visual Funnel Analysis** — See exactly where users drop off with interactive charts
- **Revenue Impact Calculator** — Translate drop-offs into lost revenue
- **What-If Scenarios** — Model the revenue impact of improving specific stages
- **Flexible Configuration** — Support for 3-10 funnel stages with custom naming
- **No Integration Required** — Manual input means it works with any analytics platform

---

## Why This Tool?

Most analytics platforms show you conversion rates, but they don't answer the critical questions:

1. **Where is the biggest revenue leak?**
2. **What's the dollar value of improving each stage?**
3. **Which improvements should we prioritize?**

This calculator does all three, helping you focus optimization efforts where they'll have the biggest business impact.

---

## Quick Start

### Local Installation
```bash
# Clone the repository
git clone https://github.com/robertoroiebahia/conversion-funnel-calculator.git
cd conversion-funnel-calculator

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run funnel_calculator.py
```

### Cloud Deployment

This app is ready to deploy to Streamlit Cloud:

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from your forked repo

---

## How to Use

### 1. Configure Your Funnel

- Set your **Average Order Value**
- Choose the **number of stages** (3-10)

### 2. Input Your Data

For each funnel stage:
- Customize the stage name (e.g., "Homepage", "Product Page", "Add to Cart")
- Enter the number of users at that stage

The calculator automatically:
- Calculates conversion rates between stages
- Identifies drop-off percentages
- Estimates revenue loss

### 3. Analyze Results

Review:
- **Overall metrics** — Conversion rate, total drop-offs, estimated revenue lost
- **Funnel visualization** — Interactive chart showing user flow
- **Revenue impact table** — Stage-by-stage breakdown with dollar values
- **What-if scenarios** — Model improvements and see projected revenue impact

---

## Example Use Case

**Scenario:** E-commerce jewelry site with $95 AOV

**Funnel:**
- Homepage: 100,000 users
- Product Pages: 75,000 users (25% drop-off)
- Add to Cart: 8,000 users (89% drop-off) 🔴
- Checkout: 4,000 users (50% drop-off)
- Purchase: 2,300 users (42.5% drop-off)

**Insight:** The PDP → ATC stage has an 89% drop-off rate, costing an estimated $6.3M in lost revenue.

**What-if:** A 10% improvement in ATC rate would generate +$34,675 monthly (+$416K annually).

**Action:** Prioritize product page optimization (trust signals, pricing clarity, social proof).

---

## Screenshots

### Funnel Visualization
*Interactive funnel chart showing drop-offs at each stage*

### Revenue Loss Analysis
*Table showing exact dollar impact of each funnel stage*

### What-If Calculator
*Model improvements and see projected revenue lift*

---

## Technical Details

**Built with:**
- [Streamlit](https://streamlit.io/) — Web app framework
- [Plotly](https://plotly.com/) — Interactive visualizations
- [Pandas](https://pandas.pydata.org/) — Data manipulation

**Key calculations:**
- **Drop-off rate** = (Users at stage N - Users at stage N+1) / Users at stage N
- **Revenue lost** = Drop-off users × Final conversion rate × AOV
- **Value of 1% improvement** = Stage users × 0.01 × Final conversion rate × AOV

---

## Roadmap

- [ ] Export results as PDF report
- [ ] Compare two time periods (YoY or MoM)
- [ ] GA4 integration for auto-fill
- [ ] Multi-currency support
- [ ] Save/load funnel configurations
- [ ] Cohort analysis by device/channel

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## About

Built by [Roberto Bahia](https://www.linkedin.com/in/roberto-bahia/) — CRO strategist specializing in conversion optimization and A/B testing for DTC e-commerce brands.

**Other tools:**
- [A/B Test Statistical Significance Calculator](https://github.com/robertoroiebahia/arpu_n_aov_stat_sig_calculator)

**Connect:**
- [LinkedIn](https://www.linkedin.com/in/roberto-bahia/)
- [GitHub](https://github.com/robertoroiebahia)

---

## Acknowledgments

- Inspired by real-world CRO consulting work
- Built to solve a gap in existing analytics tools
- Thanks to the Streamlit community for the amazing framework

---

**Questions or feedback?** [Open an issue](https://github.com/robertoroiebahia/conversion-funnel-calculator/issues) or connect on LinkedIn.
