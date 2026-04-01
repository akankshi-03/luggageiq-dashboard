import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LuggageIQ — Amazon India Intelligence",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.main { background: #0d0f14; }
[data-testid="stSidebar"] { background: #12151c !important; border-right: 1px solid #1e2330; }

.block-container { padding: 2rem 2.5rem 3rem; }

/* Hero header */
.hero {
    background: linear-gradient(135deg, #0d0f14 0%, #141824 50%, #0d0f14 100%);
    border: 1px solid #1e2330;
    border-radius: 16px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #e8edf5;
    margin: 0 0 0.3rem;
    letter-spacing: -0.5px;
}
.hero p { color: #6b7a99; font-size: 0.95rem; margin: 0; }
.hero .tag {
    display: inline-block;
    background: rgba(99,179,237,0.15);
    color: #63b3ed;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid rgba(99,179,237,0.25);
    margin-bottom: 0.7rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* KPI cards */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.8rem; }
.kpi-card {
    background: #12151c;
    border: 1px solid #1e2330;
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: #2e3a52; }
.kpi-label { font-size: 0.72rem; color: #6b7a99; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 500; margin-bottom: 0.4rem; }
.kpi-value { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 700; color: #e8edf5; line-height: 1; }
.kpi-sub { font-size: 0.78rem; color: #4a5568; margin-top: 0.3rem; }
.kpi-accent { color: #63b3ed; }
.kpi-green { color: #68d391; }
.kpi-orange { color: #f6ad55; }
.kpi-red { color: #fc8181; }

/* Section titles */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #c8d4e8;
    margin: 0 0 1rem;
    letter-spacing: -0.2px;
}
.section-sub { font-size: 0.82rem; color: #6b7a99; margin-top: -0.7rem; margin-bottom: 1rem; }

/* Brand badge */
.brand-chip {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
}
.pos-premium { background: rgba(99,179,237,0.15); color: #63b3ed; border: 1px solid rgba(99,179,237,0.3); }
.pos-mid { background: rgba(104,211,145,0.15); color: #68d391; border: 1px solid rgba(104,211,145,0.3); }
.pos-value { background: rgba(246,173,85,0.15); color: #f6ad55; border: 1px solid rgba(246,173,85,0.3); }
.pos-budget { background: rgba(252,129,129,0.15); color: #fc8181; border: 1px solid rgba(252,129,129,0.3); }

/* Insight cards */
.insight-card {
    background: #12151c;
    border: 1px solid #1e2330;
    border-left: 3px solid #63b3ed;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
.insight-card .i-title { font-size: 0.82rem; font-weight: 600; color: #c8d4e8; margin-bottom: 0.25rem; }
.insight-card .i-body { font-size: 0.8rem; color: #6b7a99; line-height: 1.5; }
.insight-warn { border-left-color: #f6ad55; }
.insight-good { border-left-color: #68d391; }
.insight-danger { border-left-color: #fc8181; }

/* Divider */
.divider { border: none; border-top: 1px solid #1e2330; margin: 1.5rem 0; }

/* Sidebar labels */
.sidebar-label { font-size: 0.75rem; color: #6b7a99; text-transform: uppercase; letter-spacing: 0.7px; font-weight: 500; margin-bottom: 0.4rem; }

/* Winner badge */
.winner-badge {
    background: linear-gradient(135deg, #f6ad55, #ed8936);
    color: #1a1a2e;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 20px;
    margin-left: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

stPlotlyChart { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os, sys
    if not os.path.exists("data/products.csv"):
        st.info("⏳ Data files nahi mili, generate ho rahi hain...")
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        os.makedirs("data", exist_ok=True)
        import importlib.util, pathlib
        spec = importlib.util.spec_from_file_location(
            "generate_data",
            pathlib.Path(__file__).parent / "data" / "generate_data.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.generate_products().to_csv("data/products.csv", index=False)
        prods = pd.read_csv("data/products.csv")
        revs  = mod.generate_reviews(prods)
        revs.to_csv("data/reviews.csv", index=False)
        mod.compute_brand_summary(prods, revs).to_csv("data/brand_summary.csv", index=False)
    products = pd.read_csv("data/products.csv")
    reviews  = pd.read_csv("data/reviews.csv")
    summary  = pd.read_csv("data/brand_summary.csv")
    return products, reviews, summary

products_df, reviews_df, summary_df = load_data()

BRAND_COLORS = {
    "Safari":             "#63b3ed",
    "Skybags":            "#f6ad55",
    "American Tourister": "#68d391",
    "VIP":                "#fc8181",
    "Aristocrat":         "#b794f4",
    "Nasher Miles":       "#76e4f7",
}
ALL_BRANDS = list(BRAND_COLORS.keys())

POS_BADGE = {
    "premium":     "pos-premium",
    "mid-premium": "pos-mid",
    "value":       "pos-value",
    "budget":      "pos-budget",
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#e8edf5;margin-bottom:1.5rem;">🧳 LuggageIQ</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Select Brands</div>', unsafe_allow_html=True)
    selected_brands = st.multiselect("", ALL_BRANDS, default=ALL_BRANDS, label_visibility="collapsed")
    if not selected_brands:
        selected_brands = ALL_BRANDS

    st.markdown("<hr style='border-color:#1e2330;margin:1rem 0'>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Price Range (₹)</div>', unsafe_allow_html=True)
    price_min, price_max = int(products_df["sell_price"].min()), int(products_df["sell_price"].max())
    price_range = st.slider("", price_min, price_max, (price_min, price_max), step=100, label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">Min Rating</div>', unsafe_allow_html=True)
    min_rating = st.slider("", 1.0, 5.0, 1.0, 0.1, label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">Luggage Type</div>', unsafe_allow_html=True)
    all_types = ["All"] + sorted(products_df["type"].unique().tolist())
    selected_type = st.selectbox("", all_types, label_visibility="collapsed")

    st.markdown('<div class="sidebar-label">Sentiment Filter</div>', unsafe_allow_html=True)
    sentiment_filter = st.selectbox("", ["All", "Positive", "Neutral", "Negative"], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#1e2330;margin:1rem 0'>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.72rem;color:#4a5568;">Amazon India · Mock Data · 2024</div>', unsafe_allow_html=True)

# ── Filter data ───────────────────────────────────────────────────────────────
filt_products = products_df[
    (products_df["brand"].isin(selected_brands)) &
    (products_df["sell_price"] >= price_range[0]) &
    (products_df["sell_price"] <= price_range[1]) &
    (products_df["rating"] >= min_rating)
]
if selected_type != "All":
    filt_products = filt_products[filt_products["type"] == selected_type]

filt_reviews = reviews_df[reviews_df["brand"].isin(selected_brands)]
if sentiment_filter != "All":
    filt_reviews = filt_reviews[filt_reviews["sentiment"] == sentiment_filter.lower()]

filt_summary = summary_df[summary_df["brand"].isin(selected_brands)]

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="tag">Competitive Intelligence · Amazon India</div>
  <h1>🧳 LuggageIQ Dashboard</h1>
  <p>Real-time brand analysis across pricing, sentiment & market positioning for luggage brands</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
top_brand = filt_summary.loc[filt_summary["sentiment_score"].idxmax(), "brand"] if len(filt_summary) else "—"
avg_discount = filt_products["discount_pct"].mean() if len(filt_products) else 0
avg_sentiment = filt_summary["sentiment_score"].mean() if len(filt_summary) else 0

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">Brands Tracked</div>
    <div class="kpi-value kpi-accent">{len(selected_brands)}</div>
    <div class="kpi-sub">of 6 total brands</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Products Analyzed</div>
    <div class="kpi-value">{len(filt_products)}</div>
    <div class="kpi-sub">across all categories</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Reviews Processed</div>
    <div class="kpi-value kpi-green">{len(filt_reviews):,}</div>
    <div class="kpi-sub">customer opinions</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Avg Sentiment Score</div>
    <div class="kpi-value kpi-orange">{avg_sentiment:.1f}%</div>
    <div class="kpi-sub">positive review ratio</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", "🏷️ Brand Compare", "🔍 Product Drilldown",
    "💬 Sentiment Deep Dive", "🤖 Agent Insights"
])

# ════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        st.markdown('<div class="section-title">Price vs Sentiment — Bubble Map</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Bubble size = total reviews · X = avg price · Y = sentiment score</div>', unsafe_allow_html=True)

        fig_bubble = go.Figure()
        for _, row in filt_summary.iterrows():
            fig_bubble.add_trace(go.Scatter(
                x=[row["avg_sell_price"]],
                y=[row["sentiment_score"]],
                mode="markers+text",
                text=[row["brand"]],
                textposition="top center",
                textfont=dict(size=11, color="#c8d4e8", family="DM Sans"),
                marker=dict(
                    size=max(row["total_reviews"] / 50, 20),
                    color=BRAND_COLORS.get(row["brand"], "#888"),
                    opacity=0.85,
                    line=dict(width=2, color="#0d0f14"),
                ),
                name=row["brand"],
                hovertemplate=(
                    f"<b>{row['brand']}</b><br>"
                    f"Avg Price: ₹{row['avg_sell_price']:,.0f}<br>"
                    f"Sentiment: {row['sentiment_score']}%<br>"
                    f"Reviews: {row['total_reviews']:,}<br>"
                    f"Rating: ⭐ {row['avg_rating']}<extra></extra>"
                ),
            ))
        fig_bubble.update_layout(
            showlegend=False,
            paper_bgcolor="#12151c", plot_bgcolor="#0d0f14",
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            xaxis=dict(title=dict(text="Avg Selling Price (₹)", font=dict(color="#6b7a99")), color="#6b7a99", gridcolor="#1e2330"),
            yaxis=dict(title=dict(text="Sentiment Score (%)", font=dict(color="#6b7a99")), color="#6b7a99", gridcolor="#1e2330"),
            font=dict(family="DM Sans", color="#6b7a99"),
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Market Positioning</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Premium vs Budget segmentation</div>', unsafe_allow_html=True)

        pos_counts = filt_summary["market_position"].value_counts()
        fig_donut = go.Figure(go.Pie(
            labels=pos_counts.index,
            values=pos_counts.values,
            hole=0.6,
            marker=dict(colors=["#63b3ed", "#68d391", "#f6ad55", "#fc8181"]),
            textfont=dict(color="#c8d4e8", size=12),
        ))
        fig_donut.update_layout(
            paper_bgcolor="#12151c", plot_bgcolor="#12151c",
            margin=dict(l=10, r=10, t=10, b=10),
            height=200,
            showlegend=True,
            legend=dict(font=dict(color="#6b7a99"), bgcolor="rgba(0,0,0,0)"),
            font=dict(family="DM Sans"),
            annotations=[dict(text="Brands", x=0.5, y=0.5, font_size=13, showarrow=False, font_color="#6b7a99")]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

        st.markdown('<div class="section-title" style="margin-top:0.5rem">Discount vs Price Band</div>', unsafe_allow_html=True)
        fig_bar = px.bar(
            filt_summary.sort_values("avg_discount_pct", ascending=True),
            x="avg_discount_pct", y="brand",
            orientation="h",
            color="brand",
            color_discrete_map=BRAND_COLORS,
            text="avg_discount_pct",
        )
        fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside", textfont_color="#c8d4e8")
        fig_bar.update_layout(
            paper_bgcolor="#12151c", plot_bgcolor="#0d0f14",
            margin=dict(l=10, r=10, t=10, b=10),
            height=200,
            showlegend=False,
            xaxis=dict(title="Avg Discount %", color="#6b7a99", gridcolor="#1e2330"),
            yaxis=dict(title="", color="#c8d4e8"),
            font=dict(family="DM Sans", color="#6b7a99"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Aspect radar
    st.markdown('<div class="section-title">Aspect-Level Quality Scores</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Wheels · Handle · Zipper · Material · Size · Durability — averaged across all reviews per brand</div>', unsafe_allow_html=True)

    aspects = ["avg_wheels_score", "avg_handle_score", "avg_zipper_score",
               "avg_material_score", "avg_size_score", "avg_durability_score"]
    aspect_labels = ["Wheels", "Handle", "Zipper", "Material", "Size", "Durability"]

    fig_radar = go.Figure()
    for _, row in filt_summary.iterrows():
        vals = [row[a] for a in aspects]
        vals_closed = vals + [vals[0]]
        labels_closed = aspect_labels + [aspect_labels[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_closed, theta=labels_closed,
            fill="toself", name=row["brand"],
            line=dict(color=BRAND_COLORS.get(row["brand"], "#888"), width=2),
            fillcolor=BRAND_COLORS.get(row["brand"], "#888"),
            opacity=0.18,
        ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="#0d0f14",
            radialaxis=dict(visible=True, range=[0, 5], color="#6b7a99", gridcolor="#1e2330"),
            angularaxis=dict(color="#c8d4e8", gridcolor="#1e2330"),
        ),
        paper_bgcolor="#12151c",
        margin=dict(l=30, r=30, t=30, b=30),
        height=400,
        legend=dict(font=dict(color="#c8d4e8"), bgcolor="rgba(0,0,0,0)"),
        font=dict(family="DM Sans"),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 2 — BRAND COMPARE
# ════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Brand Comparison Table</div>', unsafe_allow_html=True)

    display_cols = {
        "brand": "Brand", "market_position": "Position",
        "avg_sell_price": "Avg Price (₹)", "avg_discount_pct": "Avg Discount %",
        "avg_rating": "Avg Rating ⭐", "total_reviews": "Reviews",
        "sentiment_score": "Sentiment %", "top_pros": "Top Pros", "top_cons": "Top Cons"
    }
    compare_df = filt_summary[list(display_cols.keys())].rename(columns=display_cols).copy()
    compare_df["Avg Price (₹)"] = compare_df["Avg Price (₹)"].apply(lambda x: f"₹{x:,.0f}")
    compare_df["Avg Discount %"] = compare_df["Avg Discount %"].apply(lambda x: f"{x:.1f}%")
    compare_df["Sentiment %"] = compare_df["Sentiment %"].apply(lambda x: f"{x:.1f}%")
    compare_df = compare_df.sort_values("Sentiment %", ascending=False)
    st.dataframe(compare_df, use_container_width=True, height=280)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Price Distribution by Brand</div>', unsafe_allow_html=True)
        fig_box = px.box(
            filt_products, x="brand", y="sell_price", color="brand",
            color_discrete_map=BRAND_COLORS,
        )
        fig_box.update_layout(
            paper_bgcolor="#12151c", plot_bgcolor="#0d0f14",
            margin=dict(l=10, r=10, t=10, b=10), height=320,
            showlegend=False,
            xaxis=dict(title="", color="#c8d4e8", gridcolor="#1e2330"),
            yaxis=dict(title="Selling Price (₹)", color="#6b7a99", gridcolor="#1e2330"),
            font=dict(family="DM Sans", color="#6b7a99"),
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Rating vs Review Count</div>', unsafe_allow_html=True)
        fig_scatter = px.scatter(
            filt_products, x="rating", y="review_count", color="brand",
            color_discrete_map=BRAND_COLORS, size="discount_pct",
            hover_data=["product_name", "sell_price"],
        )
        fig_scatter.update_layout(
            paper_bgcolor="#12151c", plot_bgcolor="#0d0f14",
            margin=dict(l=10, r=10, t=10, b=10), height=320,
            legend=dict(font=dict(color="#c8d4e8"), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(title="Rating ⭐", color="#6b7a99", gridcolor="#1e2330"),
            yaxis=dict(title="Review Count", color="#6b7a99", gridcolor="#1e2330"),
            font=dict(family="DM Sans", color="#6b7a99"),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Brand Benchmark — Multi-Metric</div>', unsafe_allow_html=True)
    metrics = ["avg_rating", "sentiment_score", "avg_discount_pct"]
    metric_labels = {"avg_rating": "Avg Rating (×20)", "sentiment_score": "Sentiment %", "avg_discount_pct": "Discount %"}

    fig_group = go.Figure()
    for metric in metrics:
        scale = 20 if metric == "avg_rating" else 1
        fig_group.add_trace(go.Bar(
            name=metric_labels[metric],
            x=filt_summary["brand"],
            y=filt_summary[metric] * scale,
            marker_color={"avg_rating": "#63b3ed", "sentiment_score": "#68d391", "avg_discount_pct": "#f6ad55"}[metric],
            opacity=0.85,
        ))
    fig_group.update_layout(
        barmode="group",
        paper_bgcolor="#12151c", plot_bgcolor="#0d0f14",
        margin=dict(l=10, r=10, t=10, b=10), height=320,
        legend=dict(font=dict(color="#c8d4e8"), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(color="#c8d4e8", gridcolor="#1e2330"),
        yaxis=dict(color="#6b7a99", gridcolor="#1e2330"),
        font=dict(family="DM Sans", color="#6b7a99"),
    )
    st.plotly_chart(fig_group, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 3 — PRODUCT DRILLDOWN
# ════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Product Drilldown</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        brand_pick = st.selectbox("Select Brand", selected_brands)
    with col_f2:
        brand_products = filt_products[filt_products["brand"] == brand_pick]
        product_pick = st.selectbox("Select Product", brand_products["product_name"].tolist())

    if product_pick:
        prod_row = brand_products[brand_products["product_name"] == product_pick].iloc[0]
        prod_id  = prod_row["product_id"]
        prod_reviews = reviews_df[reviews_df["product_id"] == prod_id]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Selling Price", f"₹{prod_row['sell_price']:,}")
        col2.metric("List Price",    f"₹{prod_row['list_price']:,}", f"-{prod_row['discount_pct']}%")
        col3.metric("Rating",        f"⭐ {prod_row['rating']}")
        col4.metric("Reviews",       f"{prod_row['review_count']:,}")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown('<div class="section-title">Sentiment Breakdown</div>', unsafe_allow_html=True)
            sent_counts = prod_reviews["sentiment"].value_counts()
            fig_sent = go.Figure(go.Pie(
                labels=sent_counts.index, values=sent_counts.values,
                hole=0.55,
                marker=dict(colors=["#68d391", "#f6ad55", "#fc8181"]),
            ))
            fig_sent.update_layout(
                paper_bgcolor="#12151c", margin=dict(l=0,r=0,t=0,b=0),
                height=200, legend=dict(font=dict(color="#c8d4e8"), bgcolor="rgba(0,0,0,0)"),
                font=dict(family="DM Sans"),
            )
            st.plotly_chart(fig_sent, use_container_width=True)

        with col_b:
            st.markdown('<div class="section-title">Aspect Quality Scores</div>', unsafe_allow_html=True)
            aspect_cols  = ["wheels_score","handle_score","zipper_score","material_score","size_score","durability_score"]
            aspect_names = ["Wheels","Handle","Zipper","Material","Size","Durability"]
            aspect_means = [prod_reviews[c].mean() for c in aspect_cols]
            fig_asp = go.Figure(go.Bar(
                x=aspect_names, y=aspect_means,
                marker_color=["#63b3ed" if v >= 3.5 else "#fc8181" for v in aspect_means],
                text=[f"{v:.1f}" for v in aspect_means], textposition="outside",
                textfont_color="#c8d4e8",
            ))
            fig_asp.update_layout(
                paper_bgcolor="#12151c", plot_bgcolor="#0d0f14",
                margin=dict(l=10,r=10,t=10,b=10), height=200,
                yaxis=dict(range=[0,5], color="#6b7a99", gridcolor="#1e2330"),
                xaxis=dict(color="#c8d4e8"),
                font=dict(family="DM Sans", color="#6b7a99"),
            )
            st.plotly_chart(fig_asp, use_container_width=True)

        st.markdown('<div class="section-title">Sample Reviews</div>', unsafe_allow_html=True)
        sample_reviews = prod_reviews.sample(min(6, len(prod_reviews)), random_state=1)
        for _, rev in sample_reviews.iterrows():
            color = {"positive": "#68d391", "negative": "#fc8181", "neutral": "#f6ad55"}.get(rev["sentiment"], "#888")
            stars = "⭐" * rev["star_rating"]
            st.markdown(f"""
            <div class="insight-card" style="border-left-color:{color}">
              <div class="i-title">{stars} &nbsp; <span style="color:{color};font-size:0.75rem">{rev['sentiment'].upper()}</span> · {rev['review_date']}</div>
              <div class="i-body">{rev['review_text']}</div>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 4 — SENTIMENT DEEP DIVE
# ════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Sentiment Score by Brand</div>', unsafe_allow_html=True)

    fig_sent_bar = px.bar(
        filt_summary.sort_values("sentiment_score", ascending=True),
        x="sentiment_score", y="brand", orientation="h",
        color="brand", color_discrete_map=BRAND_COLORS,
        text="sentiment_score",
    )
    fig_sent_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside", textfont_color="#c8d4e8")
    fig_sent_bar.update_layout(
        paper_bgcolor="#12151c", plot_bgcolor="#0d0f14",
        margin=dict(l=10,r=10,t=10,b=10), height=280,
        showlegend=False,
        xaxis=dict(title="Sentiment Score (%)", color="#6b7a99", gridcolor="#1e2330"),
        yaxis=dict(title="", color="#c8d4e8"),
        font=dict(family="DM Sans", color="#6b7a99"),
    )
    st.plotly_chart(fig_sent_bar, use_container_width=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Positive vs Negative Reviews</div>', unsafe_allow_html=True)
        fig_stacked = go.Figure()
        for sentiment, color in [("positive_reviews","#68d391"),("negative_reviews","#fc8181"),("neutral_reviews","#f6ad55")]:
            fig_stacked.add_trace(go.Bar(
                name=sentiment.replace("_reviews","").title(),
                x=filt_summary["brand"], y=filt_summary[sentiment],
                marker_color=color, opacity=0.85,
            ))
        fig_stacked.update_layout(
            barmode="stack",
            paper_bgcolor="#12151c", plot_bgcolor="#0d0f14",
            margin=dict(l=10,r=10,t=10,b=10), height=300,
            legend=dict(font=dict(color="#c8d4e8"), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(color="#c8d4e8", gridcolor="#1e2330"),
            yaxis=dict(title="Review Count", color="#6b7a99", gridcolor="#1e2330"),
            font=dict(family="DM Sans", color="#6b7a99"),
        )
        st.plotly_chart(fig_stacked, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Aspect Heatmap</div>', unsafe_allow_html=True)
        aspect_cols  = ["avg_wheels_score","avg_handle_score","avg_zipper_score",
                        "avg_material_score","avg_size_score","avg_durability_score"]
        aspect_names = ["Wheels","Handle","Zipper","Material","Size","Durability"]
        heatmap_data = filt_summary.set_index("brand")[aspect_cols]
        heatmap_data.columns = aspect_names
        fig_heat = go.Figure(go.Heatmap(
            z=heatmap_data.values, x=aspect_names, y=heatmap_data.index,
            colorscale=[[0,"#fc8181"],[0.5,"#f6ad55"],[1,"#68d391"]],
            zmin=1, zmax=5, text=np.round(heatmap_data.values,1),
            texttemplate="%{text}", textfont=dict(color="#0d0f14", size=12),
        ))
        fig_heat.update_layout(
            paper_bgcolor="#12151c",
            margin=dict(l=10,r=10,t=10,b=10), height=300,
            xaxis=dict(color="#c8d4e8"),
            yaxis=dict(color="#c8d4e8"),
            font=dict(family="DM Sans"),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    # Value for money
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Value-for-Money Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Sentiment Score ÷ Avg Price × 1000 — higher = better value relative to cost</div>', unsafe_allow_html=True)

    vfm = filt_summary.copy()
    vfm["value_for_money"] = (vfm["sentiment_score"] / vfm["avg_sell_price"] * 1000).round(2)
    fig_vfm = px.bar(
        vfm.sort_values("value_for_money", ascending=False),
        x="brand", y="value_for_money", color="brand",
        color_discrete_map=BRAND_COLORS, text="value_for_money",
    )
    fig_vfm.update_traces(texttemplate="%{text:.2f}", textposition="outside", textfont_color="#c8d4e8")
    fig_vfm.update_layout(
        paper_bgcolor="#12151c", plot_bgcolor="#0d0f14",
        margin=dict(l=10,r=10,t=10,b=10), height=280,
        showlegend=False,
        yaxis=dict(title="VFM Score", color="#6b7a99", gridcolor="#1e2330"),
        xaxis=dict(color="#c8d4e8"),
        font=dict(family="DM Sans", color="#6b7a99"),
    )
    st.plotly_chart(fig_vfm, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 5 — AGENT INSIGHTS
# ════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">🤖 Agent Insights — Non-Obvious Conclusions</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">AI-generated strategic conclusions from the data. Updated based on active filters.</div>', unsafe_allow_html=True)

    if len(filt_summary) >= 2:
        top_sentiment  = filt_summary.loc[filt_summary["sentiment_score"].idxmax()]
        low_sentiment  = filt_summary.loc[filt_summary["sentiment_score"].idxmin()]
        top_discount   = filt_summary.loc[filt_summary["avg_discount_pct"].idxmax()]
        low_discount   = filt_summary.loc[filt_summary["avg_discount_pct"].idxmin()]
        top_price      = filt_summary.loc[filt_summary["avg_sell_price"].idxmax()]
        vfm_df = filt_summary.copy()
        vfm_df["vfm"] = vfm_df["sentiment_score"] / vfm_df["avg_sell_price"] * 1000
        best_vfm = vfm_df.loc[vfm_df["vfm"].idxmax()]

        insights = [
            ("insight-good",  f"🏆 {top_sentiment['brand']} is the Sentiment Leader",
             f"{top_sentiment['brand']} achieves the highest sentiment score of {top_sentiment['sentiment_score']:.1f}% "
             f"while maintaining an avg price of ₹{top_sentiment['avg_sell_price']:,.0f}. "
             f"This suggests strong product-market fit with customers recommending it organically."),

            ("insight-warn",  f"⚡ {top_discount['brand']} Relies Heavily on Discounts",
             f"{top_discount['brand']} offers an average discount of {top_discount['avg_discount_pct']:.1f}% — "
             f"highest among all brands. Yet its sentiment score is {top_discount['sentiment_score']:.1f}%. "
             f"High discounting with moderate sentiment suggests price is driving sales, not loyalty."),

            ("insight-good",  f"💎 {best_vfm['brand']} Wins on Value-for-Money",
             f"{best_vfm['brand']} scores {best_vfm['vfm']:.2f} on our VFM index (sentiment/price ratio). "
             f"Customers get more satisfaction per rupee spent here than any other brand in the set."),

            ("insight-danger", f"⚠️ {low_sentiment['brand']} Has the Lowest Sentiment Despite Discounts",
             f"{low_sentiment['brand']} has only {low_sentiment['sentiment_score']:.1f}% positive sentiment. "
             f"With avg discounts of {low_sentiment['avg_discount_pct']:.1f}%, the brand is struggling to convert "
             f"price advantage into customer delight — a warning sign for long-term brand equity."),

            ("insight-warn",  f"🔍 Zipper & Handle Anomaly Detected",
             f"Across brands, zipper and handle scores are consistently the lowest-rated aspects, "
             f"even for brands with 4+ star ratings. This reveals a gap: customers rate overall experience "
             f"higher than specific component quality — suggesting emotional bias in review ratings."),

            ("insight-good",  f"📈 {low_discount['brand']} Sustains Premium Pricing with Confidence",
             f"{low_discount['brand']} offers only {low_discount['avg_discount_pct']:.1f}% average discount — "
             f"the lowest in the market — yet maintains a sentiment score of {low_discount['sentiment_score']:.1f}%. "
             f"This signals strong brand pull: customers buy at near-MRP, reducing margin pressure."),
        ]

        for cls, title, body in insights:
            st.markdown(f"""
            <div class="insight-card {cls}">
              <div class="i-title">{title}</div>
              <div class="i-body">{body}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Decision Recommendations</div>', unsafe_allow_html=True)
        recs = [
            ("🎯 For a Budget Buyer",
             f"Choose {best_vfm['brand']} — best sentiment-to-price ratio in the market."),
            ("💼 For a Frequent Traveler",
             f"Choose {top_sentiment['brand']} — highest positive feedback, worth the premium."),
            ("📦 For a Brand Manager",
             f"Monitor {low_sentiment['brand']} — declining sentiment despite discounting is a red flag."),
            ("🔧 For Product Teams",
             "Improve zipper and handle quality across all brands — the #1 recurring complaint category."),
        ]
        c1, c2 = st.columns(2)
        for i, (title, body) in enumerate(recs):
            col = c1 if i % 2 == 0 else c2
            col.markdown(f"""
            <div class="insight-card">
              <div class="i-title">{title}</div>
              <div class="i-body">{body}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Select at least 2 brands to generate AI insights.")
