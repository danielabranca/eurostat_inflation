from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "processed" / "hicp_merged.csv"
HPI_PATH = Path(__file__).parent / "data" / "processed" / "inflation_hpi.csv"

st.set_page_config(page_title="Eurostat HICP Dashboard", page_icon="📈", layout="wide")

# Analytical grouping (project choice, not an official Eurostat classification)
GROUP_MAP = {
    **dict.fromkeys(
        ["Bread", "Beef and veal", "Pork", "Poultry", "Fresh or chilled fish",
         "Milk, cheese and eggs", "Eggs", "Butter", "Vegetables", "Potatoes"],
        "Food essentials"),
    **dict.fromkeys(
        ["Olive oil", "Chocolate", "Coffee", "Wine from grapes", "Cigarettes"],
        "Food & indulgence"),
    **dict.fromkeys(["Electricity", "Gas", "Diesel", "Petrol", "Energy"], "Energy"),
    "Housing, water, electricity, gas and other fuels": "Housing",
    "Books": "Culture & information",
    "Clothing": "Clothing",
    "Restaurants, cafés and the like": "Discretionary consumption & services",
    "Hairdressing salons and personal grooming establishments":
        "Discretionary consumption & services",
    "Veterinary and other services for pets": "Pet care",
}
HEADLINE = "All-items HICP"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df["country"] = df["country"].where(
        ~df["country"].str.startswith("Euro area"), "Euro area")
    df["category_group"] = df["category"].map(GROUP_MAP)
    return df


@st.cache_data
def load_hpi() -> pd.DataFrame:
    h = pd.read_csv(HPI_PATH)
    h["country"] = h["country"].where(
        ~h["country"].str.startswith("Euro area"), "Euro area")
    h["date"] = pd.PeriodIndex(h["quarter"], freq="Q").to_timestamp()
    return h


def show(fig):
    st.plotly_chart(fig, width="stretch")


if not DATA_PATH.exists():
    st.error(f"Data file not found: `{DATA_PATH}`")
    st.stop()

df = load_data()
countries = sorted(df["country"].unique())

# ---------- Sidebar ----------
st.sidebar.header("Filters")
focus = st.sidebar.selectbox(
    "Focus country", countries,
    index=countries.index("Portugal") if "Portugal" in countries else 0)
compare = st.sidebar.multiselect(
    "Countries to compare (headline tab)", countries,
    default=[c for c in ["Portugal", "Euro area"] if c in countries])

st.title("📈 Consumer Price Inflation in Europe")
st.caption(
    f"Source: Eurostat HICP · {df['date'].min():%b %Y} – {df['date'].max():%b %Y} · "
    "Year-on-year (homologous) inflation rates")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Headline inflation", "Category heatmaps", "Product explorer",
     "Weights vs inflation", "House prices"])

# ---------- 1. Headline ----------
with tab1:
    head = df[df["category"] == HEADLINE]
    f = head[head["country"] == focus].sort_values("date")
    peak = f.loc[f["homologous_inflation"].idxmax()]
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{focus}: latest ({f['date'].iloc[-1]:%b %Y})",
              f"{f['homologous_inflation'].iloc[-1]:.1f}%")
    c2.metric(f"{focus}: peak ({peak['date']:%b %Y})",
              f"{peak['homologous_inflation']:.1f}%")
    c3.metric(f"{focus}: first ({f['date'].iloc[0]:%b %Y})",
              f"{f['homologous_inflation'].iloc[0]:.1f}%")

    fig = px.line(
        head[head["country"].isin(compare)], x="date", y="homologous_inflation",
        color="country",
        labels={"date": "Date", "homologous_inflation": "Year-on-year inflation (%)",
                "country": "Country"},
        title="Overall consumer price inflation (All-items HICP)")
    fig.add_hline(y=0, line_width=1, line_color="black")
    fig.update_layout(hovermode="x unified")
    show(fig)
    st.info("A falling inflation rate means prices are rising more slowly — "
            "not that the price level has fallen.")

# ---------- 2. Heatmaps ----------
with tab2:
    group = st.selectbox("Category group", sorted(df["category_group"].dropna().unique()))
    annual = (df[(df["country"] == focus) & (df["category_group"] == group)]
              .groupby(["category", "year"])["homologous_inflation"].mean()
              .reset_index()
              .pivot(index="category", columns="year", values="homologous_inflation"))
    fig = px.imshow(
        annual, text_auto=".1f", aspect="auto",
        color_continuous_scale="RdYlBu_r", color_continuous_midpoint=0,
        labels={"x": "Year", "y": "Category", "color": "Avg. inflation (%)"},
        title=f"Average annual inflation: {group} in {focus}")
    fig.update_xaxes(type="category")
    show(fig)

# ---------- 3. Product explorer ----------
with tab3:
    cats = sorted(df["category"].unique())
    defaults = [c for c in ["Olive oil", "Eggs", "Coffee", "Chocolate", HEADLINE] if c in cats]
    chosen = st.multiselect("Categories", cats, default=defaults)
    sub = df[(df["country"] == focus) & (df["category"].isin(chosen))]
    fig = px.line(
        sub, x="date", y="homologous_inflation", color="category",
        labels={"date": "Date", "homologous_inflation": "Year-on-year inflation (%)",
                "category": "Category"},
        title=f"Monthly year-on-year inflation in {focus}")
    fig.add_hline(y=0, line_width=1, line_color="black")
    fig.update_layout(hovermode="x unified")
    show(fig)

# ---------- 4. Weights vs inflation ----------
with tab4:
    years = sorted(df["year"].unique())
    year = st.select_slider("Year", options=years, value=years[-1])
    grouped = df[(df["country"] == focus) & df["category_group"].notna()]
    yr = (grouped[grouped["year"] == year]
          .groupby(["category", "category_group"])
          .agg(inflation=("homologous_inflation", "mean"),
               weight=("item_weight", "first"))
          .reset_index())
    left, right = st.columns(2)
    with left:
        fig = px.scatter(
            yr, x="weight", y="inflation", color="category_group",
            hover_name="category",
            labels={"weight": "Item weight (‰)", "inflation": "Avg. annual inflation (%)",
                    "category_group": "Group"},
            title=f"Weight vs inflation, {focus}, {year}")
        fig.add_hline(y=0, line_width=1, line_color="black")
        show(fig)
    with right:
        top = yr.nlargest(15, "weight").sort_values("weight")
        fig = px.bar(top, x="weight", y="category", orientation="h",
                     labels={"weight": "Item weight (‰)", "category": ""},
                     title=f"Largest HICP weights, {focus}, {year}")
        show(fig)
    st.caption("Weights are in parts per thousand. Some categories are aggregates of "
               "others (e.g. Energy and Electricity), so weights should not be summed.")

# ---------- 5. House prices vs inflation ----------
with tab5:
    if not HPI_PATH.exists():
        st.warning(f"Data file not found: `{HPI_PATH}`")
    else:
        hpi = load_hpi()
        h = hpi[hpi["country"] == focus]
        if h.empty:
            st.info(f"No house price data for {focus}.")
        else:
            fig = go.Figure()
            fig.add_bar(x=h["date"], y=h["house_price_growth_quarterly"],
                        name="House price growth (quarterly, %)", marker_color="#5B8E7D")
            fig.add_scatter(x=h["date"], y=h["mean_monthly_yoy_inflation"],
                            name="Mean y-o-y inflation (%)", mode="lines+markers",
                            line=dict(color="#1f4e79", width=2))
            fig.add_hline(y=0, line_width=1, line_color="black")
            fig.update_layout(title=f"House prices and inflation in {focus}",
                              xaxis_title="Quarter", yaxis_title="%",
                              hovermode="x unified")
            show(fig)

            sc = hpi[hpi["country"].isin(compare)]
            fig = px.scatter(
                sc, x="mean_monthly_yoy_inflation", y="house_price_growth_quarterly",
                color="country", hover_data=["quarter"],
                labels={"mean_monthly_yoy_inflation": "Mean y-o-y inflation (%)",
                        "house_price_growth_quarterly": "House price growth, quarterly (%)",
                        "country": "Country"},
                title="House price growth vs inflation (selected countries)")
            fig.add_hline(y=0, line_width=1, line_color="black")
            show(fig)
            st.caption("House price growth is quarter-on-quarter; inflation is the quarterly "
                       "mean of monthly year-on-year rates, so the two are not directly "
                       "comparable in magnitude.")
