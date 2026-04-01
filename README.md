# 🧳 LuggageIQ — Amazon India Competitive Intelligence Dashboard
## 🚀 Live Dashboard
👉 [Click here to view the dashboard](https://luggageiq-dashboard-drapavd6dzopnhgbkayqig.streamlit.app/)
A competitive intelligence dashboard for luggage brands on Amazon India, built for the Moonshot AI Agent Internship Assignment.

## 📊 Dashboard Features

- **Overview Tab** — Price vs Sentiment bubble map, market positioning donut, discount bar chart, aspect-level radar chart
- **Brand Compare Tab** — Side-by-side benchmarking table, price distribution box plots, multi-metric grouped bars
- **Product Drilldown Tab** — Per-product sentiment breakdown, aspect quality scores, sample reviews
- **Sentiment Deep Dive Tab** — Sentiment scores, stacked review counts, aspect heatmap, value-for-money analysis
- **Agent Insights Tab** — 6 AI-generated non-obvious conclusions + decision recommendations

## 🚀 Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate mock data
python data/generate_data.py

# 3. Launch dashboard
streamlit run app.py
```

## 📁 Project Structure

```
luggage-dashboard/
├── app.py                  ← Main Streamlit dashboard
├── requirements.txt
├── README.md
└── data/
    ├── generate_data.py    ← Mock data generator
    ├── products.csv        ← 79 products across 6 brands
    ├── reviews.csv         ← 6,700+ customer reviews
    └── brand_summary.csv   ← Aggregated brand metrics
```

## 🏷️ Brands Covered

| Brand | Position | Avg Price |
|---|---|---|
| American Tourister | Premium | ₹6,215 |
| Nasher Miles | Mid-Premium | ₹4,200 |
| Safari | Mid-Premium | ₹3,830 |
| Skybags | Value | ₹2,527 |
| VIP | Budget | ₹2,138 |
| Aristocrat | Budget | ₹1,513 |

## 📝 Methodology

- **Data**: Realistic mock data simulating Amazon India listings and reviews
- **Sentiment**: Rule-based classification using star ratings + brand-specific strength/weakness profiles
- **Aspect Scores**: Per-review scores for wheels, handle, zipper, material, size, durability
- **VFM Index**: Sentiment Score ÷ Avg Price × 1000
