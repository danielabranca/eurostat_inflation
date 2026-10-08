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

GROUP_DESC = {
    "Food essentials": "staple food products such as bread, meat, fish, eggs, dairy, vegetables and potatoes.",
    "Food & indulgence": "selected products such as olive oil, chocolate, coffee, wine and cigarettes.",
    "Energy": "electricity, gas, petrol, diesel and the broader energy aggregate.",
    "Housing": "housing, water, electricity, gas and other fuels.",
    "Culture & information": "books.",
    "Clothing": "clothing.",
    "Discretionary consumption & services": "restaurants, cafés, hairdressing and personal grooming services.",
    "Pet care": "veterinary and other services for pets.",
}

# Written findings from the analysis notebook (Portugal only, data up to Dec 2025)
HEADLINE_FINDINGS = """
- Inflation in Portugal and the euro area was **low and fairly stable from January 2019 to December 2020**.
- It started to rise in **2021** and accelerated throughout **2022**, reaching its highest point in **October 2022** in Portugal and in every area in the dataset.
- After the peak it fell until about **November 2023**, then stayed steadier, but never returned to the low levels seen at the start of the period.
- In January 2019 the annual rate was about **1.4%** in the euro area and **0.6%** in Portugal. By December 2025 it was about **2.0%** and **2.4%**, so inflationary pressure at the end of the period was higher than at the beginning.
- The data ends in December 2025, so it says nothing about 2026.
"""

GROUP_FINDINGS = {
    "Food essentials": """
- Most categories stayed close to zero in 2019–2021 and then jumped in 2022. **Eggs** had the highest average rate in the group (**31.3%**), followed by poultry (**26.2%**), butter (**19.4%**) and beef and veal (**19.0%**).
- In 2023 **potatoes** were particularly high (**24.2%**), and vegetables (**18.3%**) and eggs (**16.1%**) were also strongly affected.
- By 2024 inflation had fallen for most products. In 2025 it differed by product: eggs (**20.8%**) and beef and veal (**18.2%**) rose again, while potatoes (**-3.5%**) and vegetables (**-0.6%**) were negative.
""",
    "Food & indulgence": """
- **Olive oil** stands out: **14.5% in 2022**, **46.5% in 2023** and **35.6% in 2024**. In 2025 the average was **-24.0%**, meaning prices were on average much lower than a year earlier.
- **Chocolate** rose gradually, reaching **17.3%** in 2025.
- **Coffee** went from about zero in 2019–2021 to **8.4%** in 2022 and 2023, and **9.4%** in 2025.
- **Wine** stayed comparatively stable, close to zero or in the low single digits.
""",
    "Energy": """
- After mostly negative rates in 2020, energy prices rose strongly in 2021 and especially in 2022. **Gas** was highest in 2022 (**38.4%**), followed by diesel (**25.9%**), overall Energy (**23.7%**) and electricity (**22.1%**).
- In 2023, electricity, diesel, petrol and overall Energy were negative on average, while gas stayed positive (**14.0%**).
- In 2024 electricity returned to a high rate (**14.2%**) while gas was negative (**-10.0%**): different energy products can follow very different paths.
""",
}
OVERALL_FINDINGS = ("**Overall:** 2022 stands out as a period of high inflationary pressure, "
                    "particularly for food essentials and energy. Afterwards, categories peaked, "
                    "fell and reversed at different times, with no single trajectory.")


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


def findings(title, body):
    """Show the written findings (prepared for Portugal) only when Portugal is selected."""
    if focus == "Portugal":
        with st.expander(title):
            st.markdown(body)
    else:
        st.caption("📝 The written findings were prepared for Portugal. "
                   "Select Portugal as focus country to read them.")


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

with st.expander("ℹ️ New here? Start with this", expanded=True):
    st.markdown(f"""
**What am I looking at?** Eurostat's **HICP** (Harmonised Index of Consumer Prices) is the measure used to compare
how fast consumer prices rise in different European countries. This dashboard covers
**{df['date'].min():%B %Y} to {df['date'].max():%B %Y}**.

**What does "inflation" mean here?** Every rate is **year-on-year**: how much prices in a given month are higher
(or lower, if negative) than in the *same month a year earlier*.

**Inflation rate ≠ price level.** A falling rate means prices are rising *more slowly* than before, not that they have
become cheaper. Even with a low rate, prices can still be well above where they were in 2019.

**How to use it:** choose a *focus country* in the sidebar and explore the tabs. Hover over charts for exact values.

*The product groups (e.g. "Food essentials") are an analytical choice made for this project and are not an official
Eurostat classification.*
""")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Headline inflation", "Category heatmaps", "Product explorer",
     "Weights vs inflation", "House prices"])

# ---------- 1. Headline ----------
with tab1:
    st.markdown("**Headline inflation** is the overall rise in consumer prices (the *All-items HICP*, "
                "covering the whole basket of goods and services). Compare countries below; the numbers "
                "show the selected focus country.")
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
    findings("📝 Key findings: overall inflation", HEADLINE_FINDINGS)

# ---------- 2. Heatmaps ----------
with tab2:
    st.markdown("Each cell is the **average of the 12 monthly year-on-year rates** in that year. "
                "**Red = prices rising faster** than a year earlier; **blue = prices rising more slowly "
                "or falling**. It shows how intense inflation was, not the cumulative price change.")
    group = st.selectbox("Category group", sorted(df["category_group"].dropna().unique()))
    st.markdown(f"**{group}** includes {GROUP_DESC.get(group, '')}")
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
    if group in GROUP_FINDINGS:
        findings(f"📝 Key findings: {group}", GROUP_FINDINGS[group] + "\n" + OVERALL_FINDINGS)
    st.caption("Only complete years are shown, because a partial year would not be comparable.")

# ---------- 3. Product explorer ----------
with tab3:
    st.markdown("Follow individual products month by month. A line **above zero** means the price is higher "
                "than in the same month a year earlier; **below zero**, lower. Add *All-items HICP* "
                "as a benchmark to see whether a product rose faster or slower than prices overall.")
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
    st.markdown("Inflation alone doesn't tell you how much a product matters to households. The **item weight** "
                "is how important a category is in the average consumer basket. Compare the two: a product "
                "with high inflation but a small weight has little effect on overall inflation, and vice versa.")
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
    st.caption("Weights are in parts per thousand (‰), with the whole basket = 1,000, so a weight of 100 "
               "is about 10% of the basket. Some categories are aggregates of others (e.g. Energy and "
               "Electricity), so weights should not be summed. A category's position here does not by "
               "itself show its contribution to overall inflation.")

# ---------- 5. House prices vs inflation ----------
with tab5:
    st.markdown("Do house prices move with consumer prices? Bars show how much house prices grew "
                "each quarter; the line shows average inflation in the same quarter.")
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
