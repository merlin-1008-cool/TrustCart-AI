from pathlib import Path
import hashlib

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="TrustCart AI | Shop Smarter",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent

PRODUCTS_FILE = ROOT / "data" / "raw" / "products.csv"
RETAILERS_FILE = ROOT / "data" / "retailers.csv"
HISTORY_FILE = ROOT / "data" / "raw" / "price_history.csv"
DEALS_FILE = ROOT / "data" / "processed" / "deal_analysis.csv"
TRUST_FILE = ROOT / "data" / "raw" / "retailer_trust.csv"


# =========================================================
# LAVENDER THEME + TOP NAVIGATION STYLING
# =========================================================

st.markdown(
    """
    <style>
    /* Main page background — original colours preserved */
    .stApp {
        background-color: #F7F4FC;
        color: #292438;
    }

    /* Hide the old left sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Hide the sidebar expand control */
    [data-testid="collapsedControl"] {
        display: none;
    }

    /* Main page spacing */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* Headings */
    h1, h2, h3 {
        color: #38265C;
    }

    /* Hero banner */
    .hero {
        background: linear-gradient(120deg, #7655B5, #A58ADD);
        padding: 35px;
        border-radius: 22px;
        color: white;
        margin-bottom: 22px;
    }

    .hero h1 {
        color: white;
        font-size: 40px;
    }

    .hero p {
        color: white;
        font-size: 17px;
    }

    /* Demo information notice */
    .notice {
        background: #F0E8FC;
        border-left: 4px solid #7655B5;
        padding: 14px 18px;
        border-radius: 8px;
        margin: 15px 0 22px 0;
    }

    /* Alert boxes */
    .alert-red {
        background: #FDECEC;
        border-left: 5px solid #C62828;
        padding: 14px;
        border-radius: 8px;
        margin: 10px 0;
    }

    .alert-green {
        background: #EAF7EE;
        border-left: 5px solid #25834A;
        padding: 14px;
        border-radius: 8px;
        margin: 10px 0;
    }

    .alert-yellow {
        background: #FFF6DF;
        border-left: 5px solid #D69E00;
        padding: 14px;
        border-radius: 8px;
        margin: 10px 0;
    }

    /* Category cards */
    .category-card {
        background: white;
        border: 1px solid #E5DCF3;
        border-radius: 16px;
        padding: 18px;
        min-height: 120px;
        margin-bottom: 10px;
    }

    .category-icon {
        font-size: 30px;
    }

    .category-name {
        font-size: 17px;
        font-weight: 700;
        color: #38265C;
    }

    .category-description {
        color: #716980;
        font-size: 13px;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #E5DCF3;
        padding: 15px;
        border-radius: 14px;
    }

    /* Purple buttons */
    div.stButton > button {
        background-color: #7655B5;
        color: white;
        border: none;
        border-radius: 9px;
        font-weight: 600;
        padding: 10px 18px;
        transition: background-color 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #62439E;
        color: white;
        border: none;
    }

    /* Horizontal top navigation */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 10px;
        padding: 12px;
        background-color: #FFFFFF;
        border: 1px solid #DDD0F2;
        border-radius: 12px;
        align-items: center;
    }

    /* Navigation labels */
    div[data-testid="stRadio"] > div[role="radiogroup"] label {
        background-color: #F7F4FC;
        border: 1px solid #DDD0F2;
        border-radius: 9px;
        padding: 8px 14px;
        margin: 0;
        cursor: pointer;
    }

    /* Navigation label text */
    div[data-testid="stRadio"] > div[role="radiogroup"] label p {
        color: #38265C;
        font-weight: 600;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #80778F;
        font-size: 12px;
        padding-top: 25px;
        border-top: 1px solid #E5DCF3;
        margin-top: 35px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_csv(file_path):
    path = Path(file_path)

    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


products = load_csv(PRODUCTS_FILE)
retailers = load_csv(RETAILERS_FILE)
history = load_csv(HISTORY_FILE)
deals = load_csv(DEALS_FILE)
trust = load_csv(TRUST_FILE)


if products.empty:
    st.error("Product data missing: data/raw/products.csv")
    st.stop()

if history.empty:
    st.error("Price history missing: data/raw/price_history.csv")
    st.stop()

if deals.empty:
    st.error("Deal analysis missing: data/processed/deal_analysis.csv")
    st.stop()


history["date"] = pd.to_datetime(
    history["date"],
    errors="coerce",
)

history["price_inr"] = pd.to_numeric(
    history["price_inr"],
    errors="coerce",
)


# =========================================================
# CONSTANTS AND HELPER FUNCTIONS
# =========================================================

PAGES = [
    "Home",
    "Price Comparison",
    "Price History",
    "Deal Intelligence",
    "Seller Trust",
    "Target Price Monitor",
    "Premium Subscription",
]
CATEGORY_INFO = {
    "Smartphones": ("📱", "Phones for everyday life"),
    "Laptops": ("💻", "Work, study and creativity"),
    "Headphones & Earbuds": ("🎧", "Audio for every moment"),
    "Smartwatches": ("⌚", "Smart wearable technology"),
    "Tablets": ("📲", "Entertainment and productivity"),
    "Smart TVs": ("📺", "Upgrade your viewing experience"),
    "Speakers": ("🔊", "Sound for every space"),
}

categories = sorted(
    products["category"].dropna().unique().tolist()
)


def money(value):
    if pd.isna(value):
        return "N/A"

    return f"₹{float(value):,.0f}"


def show_demo_notice():
    st.markdown(
        """
        <div class="notice">
            <strong>SIMULATED DEMONSTRATION DATA</strong><br>
            Prices, ratings, complaints, seller verification,
            return policies and warranty indicators are illustrative.
            They are not verified live retailer information.
        </div>
        """,
        unsafe_allow_html=True,
    )


def set_product(product_name):
    match = products[
        products["product_name"] == product_name
    ]

    if match.empty:
        return

    row = match.iloc[0]

    st.session_state["selected_product_name"] = row[
        "product_name"
    ]

    st.session_state["selected_product_id"] = str(
        row["product_id"]
    )

    st.session_state["selected_category"] = row[
        "category"
    ]


def get_selected_product():
    selected_name = st.session_state.get(
        "selected_product_name"
    )

    if selected_name not in products["product_name"].values:
        set_product(products.iloc[0]["product_name"])

    return products[
        products["product_name"]
        == st.session_state["selected_product_name"]
    ].iloc[0]


def latest_listings(product_id):
    rows = history[
        history["product_id"].astype(str)
        == str(product_id)
    ].copy()

    rows = rows.dropna(
        subset=["date", "price_inr"]
    )

    if rows.empty:
        return rows

    return (
        rows.sort_values("date")
        .groupby(
            ["retailer_id", "retailer_name"],
            as_index=False,
        )
        .tail(1)
        .sort_values("price_inr")
        .reset_index(drop=True)
    )


# =========================================================
# KEEP THE SELECTED PRODUCT ACROSS ALL PAGES
# =========================================================

if "selected_product_name" not in st.session_state:
    set_product(products.iloc[0]["product_name"])


if "navigation_target" in st.session_state:
    st.session_state["main_navigation"] = (
        st.session_state.pop("navigation_target")
    )


if "main_navigation" not in st.session_state:
    st.session_state["main_navigation"] = "Home"


selected_product = get_selected_product()


# =========================================================
# SIDEBAR
# =========================================================
# =========================================================
# TOP NAVIGATION
# =========================================================

st.markdown(
    """
    <div style="margin-bottom: 8px;">
        <h2 style="margin-bottom: 0;">🛍️ TrustCart AI</h2>
        <p style="color: #716980; margin-top: 3px;">
            Shop smarter. Compare better.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.radio(
    "EXPLORE",
    PAGES,
    horizontal=True,
    key="main_navigation",
    label_visibility="collapsed",
)

st.divider()



# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <h1>Shop smarter with TrustCart AI.</h1>
            <p>
                Compare prices, inspect historical trends,
                and review shopping risk indicators.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    show_demo_notice()

    st.markdown("### Choose the product you want to buy")

    saved_category = st.session_state.get(
        "selected_category",
        categories[0],
    )

    if saved_category not in categories:
        saved_category = categories[0]

    category_index = categories.index(saved_category)

    selected_category = st.selectbox(
        "Choose a category",
        categories,
        index=category_index,
        key="home_category_picker",
    )

    category_products = products[
        products["category"] == selected_category
    ]

    product_names = category_products[
        "product_name"
    ].tolist()

    existing_product = st.session_state.get(
        "selected_product_name"
    )

    if existing_product in product_names:
        product_index = product_names.index(existing_product)
    else:
        product_index = 0

    selected_name = st.selectbox(
        "Choose a product",
        product_names,
        index=product_index,
        key="home_product_picker",
    )

    if st.button(
            "Select This Product",
            use_container_width=True,
    ):
        set_product(selected_name)

        st.session_state["navigation_target"] = (
            "Price Comparison"
        )

        st.rerun()

    st.divider()

    st.markdown("### Explore gadget categories")

    category_items = list(CATEGORY_INFO.items())

    for start in range(0, len(category_items), 3):

        columns = st.columns(3)

        for column, item in zip(
            columns,
            category_items[start:start + 3],
        ):

            category, details = item

            icon, description = details

            count = int(
                (products["category"] == category).sum()
            )

            column.markdown(
                f"""
                <div class="category-card">
                    <div class="category-icon">{icon}</div>
                    <div class="category-name">{category}</div>
                    <div class="category-description">
                        {description}<br>
                        {count} demo products
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if column.button(
                f"Explore {category}",
                key=f"explore_{category}",
                use_container_width=True,
            ):

                available_products = products[
                    products["category"] == category
                ]["product_name"].tolist()

                if available_products:
                    set_product(available_products[0])

                st.session_state["navigation_target"] = (
                    "Price Comparison"
                )

                st.rerun()


# Refresh selected product after any Home-page change.
selected_product = get_selected_product()

product_id = str(selected_product["product_id"])
product_name = selected_product["product_name"]
product_category = selected_product["category"]


product_history = history[
    history["product_id"].astype(str) == product_id
].copy()


product_deals = deals[
    deals["product_id"].astype(str) == product_id
].copy() if "product_id" in deals.columns else pd.DataFrame()


# =========================================================
# PRICE COMPARISON
# =========================================================

if page == "Price Comparison":

    st.markdown(
        f"## 🔎 Price Comparison: {product_name}"
    )

    show_demo_notice()

    listings = latest_listings(product_id)

    if listings.empty:

        st.warning(
            "No simulated prices available for this product."
        )

    else:

        lowest = listings.iloc[0]
        highest = listings.iloc[-1]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Lowest simulated price",
            money(lowest["price_inr"]),
        )

        col1.caption(
            f"Retailer: {lowest['retailer_name']}"
        )

        col2.metric(
            "Highest simulated price",
            money(highest["price_inr"]),
        )

        col2.caption(
            f"Retailer: {highest['retailer_name']}"
        )

        col3.metric(
            "Price difference",
            money(
                highest["price_inr"]
                - lowest["price_inr"]
            ),
        )

        col4.metric(
            "Retailer listings",
            len(listings),
        )

        st.markdown("### Compare retailer prices")

        chart = px.bar(
            listings,
            x="retailer_name",
            y="price_inr",
            color="price_inr",
            text="price_inr",
            labels={
                "retailer_name": "Retailer",
                "price_inr": "Simulated price (₹)",
            },
            template="plotly_white",
        )

        chart.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside",
        )

        chart.update_layout(
            showlegend=False,
            xaxis_title=None,
            yaxis_title="Simulated price (₹)",
        )

        st.plotly_chart(
            chart,
            use_container_width=True,
        )

        st.dataframe(
            listings[
                [
                    "retailer_name",
                    "date",
                    "price_inr",
                ]
            ].rename(
                columns={
                    "retailer_name": "Retailer",
                    "date": "Latest observation",
                    "price_inr": "Simulated price (₹)",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# PRICE HISTORY
# =========================================================

elif page == "Price History":

    st.markdown(
        f"## 📈 Price History: {product_name}"
    )

    st.write(
        "Select a retailer to view its price history "
        "for your chosen product."
    )

    show_demo_notice()

    if product_history.empty:

        st.warning(
            "No price history available for this product."
        )

    else:

        retailer_names = sorted(
            product_history["retailer_name"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_retailer = st.selectbox(
            "Select retailer",
            ["All retailers"] + retailer_names,
            key="history_retailer",
        )

        if selected_retailer == "All retailers":
            filtered_history = product_history
        else:
            filtered_history = product_history[
                product_history["retailer_name"]
                == selected_retailer
            ]

        if selected_retailer != "All retailers":

            st.markdown(
                f"### {selected_retailer} — six-month price history"
            )

        chart = px.line(
            filtered_history.sort_values("date"),
            x="date",
            y="price_inr",
            color=(
                "retailer_name"
                if selected_retailer == "All retailers"
                else None
            ),
            markers=True,
            labels={
                "date": "Date",
                "price_inr": "Simulated price (₹)",
                "retailer_name": "Retailer",
            },
            template="plotly_white",
        )

        chart.update_layout(
            hovermode="x unified",
            xaxis_title=None,
            yaxis_title="Simulated price (₹)",
        )

        st.plotly_chart(
            chart,
            use_container_width=True,
        )

        if selected_retailer != "All retailers":

            summary = filtered_history[
                "price_inr"
            ].agg(["min", "mean", "max"])

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Historical lowest",
                money(summary["min"]),
            )

            col2.metric(
                "Historical average",
                money(summary["mean"]),
            )

            col3.metric(
                "Historical highest",
                money(summary["max"]),
            )


# =========================================================
# DEAL INTELLIGENCE
# =========================================================

elif page == "Deal Intelligence":

    st.markdown(
        f"## 🏷️ Deal Intelligence: {product_name}"
    )

    st.write(
        "Understand whether to buy now, compare retailers, "
        "or monitor the price before purchasing."
    )

    show_demo_notice()

    if product_deals.empty:

        st.warning(
            "No deal analysis is available for this product."
        )

    else:

        # -------------------------------------------------
        # PREPARE DEAL DATA
        # -------------------------------------------------

        deal_data = product_deals.copy()

        numeric_columns = [
            "latest_price_inr",
            "historical_min_inr",
            "historical_average_inr",
            "market_min_inr",
            "market_average_inr",
            "pct_vs_historical_avg",
        ]

        for column in numeric_columns:
            if column in deal_data.columns:
                deal_data[column] = pd.to_numeric(
                    deal_data[column],
                    errors="coerce",
                )

        if "retailer_name" not in deal_data.columns:

            st.warning(
                "Retailer names are unavailable in the deal dataset."
            )

        elif "latest_price_inr" not in deal_data.columns:

            st.warning(
                "Current prices are unavailable in the deal dataset."
            )

        else:

            deal_data = deal_data.dropna(
                subset=["retailer_name", "latest_price_inr"]
            )

            deal_data = deal_data[
                deal_data["latest_price_inr"] > 0
            ].copy()

            if deal_data.empty:

                st.warning(
                    "No valid retailer prices are available."
                )

            else:

                deal_data = deal_data.sort_values(
                    "latest_price_inr"
                ).reset_index(drop=True)

                # -----------------------------------------
                # SELECTED RETAILER
                # -----------------------------------------

                retailer_names = deal_data[
                    "retailer_name"
                ].astype(str).tolist()

                selected_retailer = st.selectbox(
                    "Select the retailer you are considering",
                    retailer_names,
                    key="deal_retailer",
                )

                selected_rows = deal_data[
                    deal_data["retailer_name"].astype(str)
                    == selected_retailer
                ]

                selected_row = selected_rows.iloc[0]

                current_price = float(
                    selected_row["latest_price_inr"]
                )

                historical_low = selected_row.get(
                    "historical_min_inr",
                    float("nan"),
                )

                historical_average = selected_row.get(
                    "historical_average_inr",
                    float("nan"),
                )

                market_low = selected_row.get(
                    "market_min_inr",
                    float("nan"),
                )

                # -----------------------------------------
                # PRICE METRICS
                # -----------------------------------------

                st.markdown("### 📊 Your selected retailer")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Current price",
                    money(current_price),
                )

                col2.metric(
                    "Six-month lowest recorded",
                    money(historical_low),
                )

                col3.metric(
                    "Six-month average",
                    money(historical_average),
                )

                # -----------------------------------------
                # SELECTED RETAILER RECOMMENDATION
                # -----------------------------------------

                st.markdown(
                    "### 🛍️ Recommendation for "
                    f"{selected_retailer}"
                )

                if (
                    pd.notna(historical_low)
                    and float(historical_low) > 0
                    and current_price
                    <= float(historical_low) + 0.01
                ):

                    st.markdown(
                        """
                        <div class="alert-green">
                            <strong>🟢 LOWEST RECORDED PRICE</strong><br>
                            This price matches the lowest price recorded
                            in the available historical data. If you need
                            the product, it may be a good buying opportunity.
                            Check the seller, warranty and return policy
                            before purchasing.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                elif (
                    pd.notna(historical_average)
                    and float(historical_average) > 0
                    and current_price
                    <= float(historical_average) * 0.95
                ):

                    st.markdown(
                        """
                        <div class="alert-green">
                            <strong>🟢 ATTRACTIVE HISTORICAL PRICE</strong><br>
                            The current price is at least 5% below this
                            retailer's historical average. Consider buying
                            if the seller and purchase conditions are suitable.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                elif (
                    pd.notna(historical_average)
                    and float(historical_average) > 0
                    and current_price
                    >= float(historical_average) * 1.05
                ):

                    difference = (
                        current_price - float(historical_average)
                    )

                    st.markdown(
                        f"""
                        <div class="alert-yellow">
                            <strong>🟡 PRICE IS ABOVE THE HISTORICAL AVERAGE</strong><br>
                            The current price is {money(difference)} higher
                            than this retailer's historical average. If your
                            purchase is not urgent, compare other retailers
                            or monitor this product before deciding.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                else:

                    st.markdown(
                        """
                        <div class="alert-yellow">
                            <strong>🟡 COMPARE BEFORE BUYING</strong><br>
                            The current price is close to the historical
                            average, or the available history is insufficient
                            to identify a clear price advantage. Compare
                            retailers before deciding.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.caption(
                    "Historical comparisons use the values in the deal "
                    "dataset. A six-month-low claim is reliable only when "
                    "that dataset contains complete and correctly dated "
                    "observations for the intended six-month period."
                )

                # -----------------------------------------
                # BEST AVAILABLE RETAILER
                # -----------------------------------------

                st.divider()

                st.markdown(
                    "### 🏆 Best available price across retailers"
                )

                cheapest_row = deal_data.iloc[0]

                cheapest_retailer = str(
                    cheapest_row["retailer_name"]
                )

                cheapest_price = float(
                    cheapest_row["latest_price_inr"]
                )

                savings = current_price - cheapest_price

                if savings > 0.01:

                    st.markdown(
                        f"""
                        <div class="alert-green">
                            <strong>🏆 A LOWER LISTED PRICE IS AVAILABLE</strong><br>
                            {cheapest_retailer} has the lowest listed
                            simulated price at {money(cheapest_price)}.
                            You could save {money(savings)} compared with
                            the selected retailer, {selected_retailer}.
                            Check seller reliability, warranty, delivery
                            charges and return conditions before switching.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                elif abs(savings) <= 0.01:

                    st.markdown(
                        f"""
                        <div class="alert-green">
                            <strong>🟢 LOWEST LISTED PRICE MATCHED</strong><br>
                            {selected_retailer} currently matches the
                            lowest listed simulated price for this product.
                            Check seller and purchase conditions before buying.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                else:

                    st.info(
                        f"{selected_retailer} is currently the lowest "
                        "priced retailer in the available comparison."
                    )

                # -----------------------------------------
                # RETAILER PRICE COMPARISON
                # -----------------------------------------

                st.markdown(
                    "### 💰 Compare prices before purchasing"
                )

                comparison = deal_data[
                    [
                        column
                        for column in [
                            "retailer_name",
                            "latest_price_inr",
                            "historical_min_inr",
                            "historical_average_inr",
                        ]
                        if column in deal_data.columns
                    ]
                ].rename(
                    columns={
                        "retailer_name": "Retailer",
                        "latest_price_inr": "Current price (₹)",
                        "historical_min_inr": "Historical low (₹)",
                        "historical_average_inr":
                            "Historical average (₹)",
                    }
                )

                st.dataframe(
                    comparison,
                    use_container_width=True,
                    hide_index=True,
                )

                # -----------------------------------------
                # TARGET PRICE MONITOR
                # -----------------------------------------

                st.divider()

                st.markdown(
                    "### 🔔 Target price monitor"
                )

                st.write(
                    "Enter the price you would like to pay. "
                    "TrustCart AI will tell you whether the current "
                    "price has reached your target."
                )

                target_price = st.number_input(
                    "Your target price (₹)",
                    min_value=1.0,
                    value=float(
                        max(1, int(current_price * 0.90))
                    ),
                    step=500.0,
                    key=f"target_price_{product_id}_{selected_retailer}",
                )

                if current_price <= target_price:

                    st.success(
                        f"Your target has been reached! The current "
                        f"price is {money(current_price)}, which is "
                        f"at or below your target of {money(target_price)}."
                    )

                else:

                    target_gap = current_price - target_price

                    st.info(
                        f"The current price is {money(target_gap)} "
                        f"above your target. You can monitor the price "
                        "before deciding to buy."
                    )

                st.caption(
                    "This prototype checks the target against the "
                    "currently loaded demonstration data. It does not "
                    "automatically monitor retailer websites or send "
                    "notifications."
                )

                # -----------------------------------------
                # IMPORTANT LIMITATIONS
                # -----------------------------------------

                with st.expander(
                    "How TrustCart AI makes these recommendations"
                ):

                    st.write(
                        "- Historical recommendations compare the "
                        "current listed price with the historical values "
                        "available in the dataset."
                    )

                    st.write(
                        "- The lowest-price recommendation compares "
                        "retailers represented in the loaded data only."
                    )

                    st.write(
                        "- A lower price does not automatically mean "
                        "a better or safer purchase."
                    )

                    st.write(
                        "- Seller verification, warranty, delivery "
                        "charges and return policies should be checked "
                        "separately before purchasing."
                    )

                    st.write(
                        "- All current prices and recommendations are "
                        "based on simulated demonstration data, not "
                        "verified live retailer information."
                    )

elif page == "Target Price Monitor":
    st.title("🎯 Target Price Monitor")
    st.write(
        "Set your target price and compare available prices "
        "across retailers."
    )

    show_demo_notice()

    product = get_selected_product()

    if product is None:
        st.info("Please select a product first.")
    else:
        product_id = product["product_id"]
        product_name = product["product_name"]

        st.subheader(f"Product: {product_name}")

        # Get the latest available price from each retailer.
        listings = latest_listings(product_id)

        if listings.empty:
            st.warning(
                "No price data is available for this product "
                "in the current demonstration dataset."
            )
        else:
            listings = listings.copy()
            listings["price_inr"] = pd.to_numeric(
                listings["price_inr"], errors="coerce"
            )
            listings = listings.dropna(subset=["price_inr"])

            if listings.empty:
                st.warning("No valid prices are available.")
            else:
                lowest_price = float(listings["price_inr"].min())
                default_target = max(
                    1.0, float(round(lowest_price * 0.90))
                )

                target_price = st.number_input(
                    "Your target price (₹)",
                    min_value=1.0,
                    value=default_target,
                    step=500.0,
                    key=f"target_price_all_{product_id}",
                )

                st.info(
                    "🔔 Want to be notified when your target price is reached?\n\n"
                    "Premium membership is planned at ₹200/year and will include "
                    "target-price alerts for up to 5 products.\n\n"
                    "⚠️ Automatic price monitoring and notifications are not active yet. "
                    "Currently, this page checks only the available demo data."
                )

                if st.button(
                        "💎 View Premium Plan — ₹200/year",
                        key=f"premium_from_target_{product_id}",
                        use_container_width=True,
                ):
                    st.session_state["navigation_target"] = "Premium Subscription"
                    st.rerun()

                st.caption(
                    "This demo checks the latest prices available "
                    "in the dataset. It does not continuously monitor "
                    "retailer websites."
                )

                # Find every retailer meeting the target.
                matching = listings[
                    listings["price_inr"] <= target_price
                ].copy()

                # Identify the retailer name column.
                retailer_col = next(
                    (
                        col for col in [
                            "retailer_name",
                            "seller_name",
                            "retailer",
                        ]
                        if col in matching.columns
                    ),
                    None,
                )

                if matching.empty:
                    st.warning(
                        "No retailer in the available dataset currently "
                        "meets your target price."
                    )
                    st.write(
                        "Try increasing your target price to see "
                        "whether any available offers qualify."
                    )
                else:
                    matching["Savings vs Target (₹)"] = (
                        target_price - matching["price_inr"]
                    )

                    matching = matching.sort_values("price_inr")

                    st.success(
                        f"{len(matching)} available offer(s) meet "
                        "or beat your target price."
                    )

                    cheapest = matching.iloc[0]

                    if retailer_col:
                        cheapest_name = cheapest[retailer_col]
                    else:
                        cheapest_name = "Lowest-priced available retailer"

                    st.metric(
                        "🏆 Lowest Matching Price",
                        f"₹{cheapest['price_inr']:,.0f}",
                        f"₹{target_price - cheapest['price_inr']:,.0f} "
                        "below your target",
                    )

                    st.write(f"**Lowest-priced retailer:** {cheapest_name}")

                    # Prepare the comparison table.
                    display = matching.copy()

                    rename_columns = {
                        "price_inr": "Current Price (₹)",
                        "date": "Last Recorded Date",
                    }

                    display = display.rename(
                        columns={
                            old: new
                            for old, new in rename_columns.items()
                            if old in display.columns
                        }
                    )

                    display = display.rename(
                        columns={
                            "Savings vs Target (₹)": "Savings vs Target (₹)"
                        }
                    )

                    preferred_columns = [
                        col for col in [
                            retailer_col,
                            "Current Price (₹)",
                            "Savings vs Target (₹)",
                            "Last Recorded Date",
                        ]
                        if col and col in display.columns
                    ]

                    st.subheader("Retailers Meeting Your Target")
                    st.dataframe(
                        display[preferred_columns],
                        use_container_width=True,
                        hide_index=True,
                    )

                # Show how much of the expected retailer list has prices.
                st.subheader("Retailer Price Coverage")

                try:
                    retailer_names = []

                    if (
                        not retailers.empty
                        and "retailer_name" in retailers.columns
                    ):
                        retailer_names = (
                            retailers["retailer_name"]
                            .dropna()
                            .astype(str)
                            .unique()
                            .tolist()
                        )

                    if not retailer_names and "retailer_name" in listings.columns:
                        retailer_names = (
                            listings["retailer_name"]
                            .dropna()
                            .astype(str)
                            .unique()
                            .tolist()
                        )

                    if retailer_names:
                        available_names = set()

                        if "retailer_name" in listings.columns:
                            available_names = set(
                                listings["retailer_name"]
                                .dropna()
                                .astype(str)
                            )

                        missing_names = [
                            name for name in retailer_names
                            if name not in available_names
                        ]

                        st.write(
                            f"Retailers listed: {len(retailer_names)}"
                        )
                        st.write(
                            f"Retailers with available prices: "
                            f"{len(available_names)}"
                        )

                        if missing_names:
                            st.warning(
                                "No price is available in the current "
                                "dataset for: "
                                + ", ".join(missing_names)
                            )
                    else:
                        st.info(
                            "The retailer list could not be identified "
                            "from the current dataset."
                        )

                except NameError:
                    st.info(
                        "Retailer coverage information is not available."
                    )


# =========================================================
# PREMIUM SUBSCRIPTION
# =========================================================

elif page == "Premium Subscription":

    st.markdown("## 💎 TrustCart AI Premium")

    st.markdown(
        """
        <div class="hero">
            <h1>Shop smarter. Save with confidence.</h1>
            <p>
                Set your target prices and prepare to discover
                better buying opportunities across retailers.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    show_demo_notice()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown(
            """
            <div style="
                background: white;
                border: 2px solid #A58ADD;
                border-radius: 20px;
                padding: 30px;
                text-align: center;
            ">
                <h2>TrustCart AI Premium</h2>
                <p style="color: #716980;">
                    Annual membership
                </p>
                <h1 style="color: #7655B5; font-size: 44px;">
                    ₹200
                </h1>
                <p style="color: #716980;">
                    per year
                </p>
                <hr>
                <p>✅ Compare available retailer prices</p>
                <p>✅ Explore available price history</p>
                <p>✅ Review deal intelligence</p>
                <p>✅ Review seller trust indicators</p>
                <p>✅ Plan target-price monitoring for up to 5 products</p>
                <p>🔔 Future email alerts when monitoring is implemented</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if st.button(
            "Choose Premium Plan",
            use_container_width=True,
            key="choose_premium_plan",
        ):

            st.session_state["premium_interest"] = True

        if st.session_state.get("premium_interest", False):

            st.success(
                "You've selected the Premium plan!"
            )

            st.info(
                "Payment is not enabled yet. No money has been "
                "collected and no subscription has been activated."
            )

    st.divider()

    st.markdown("### Compare membership plans")

    plan_comparison = pd.DataFrame(
        {
            "Feature": [
                "Price comparison",
                "Price history",
                "Deal intelligence",
                "Seller trust indicators",
                "Target-price monitoring",
                "Monitor up to 5 products",
                "Automatic monitoring",
                "Email alerts",
            ],
            "Free": [
                "Available demo data",
                "Available demo data",
                "Available demo data",
                "Available demo data",
                "Demo page access",
                "Not included",
                "Not included",
                "Not included",
            ],
            "Premium — ₹200/year": [
                "Included",
                "Included",
                "Included",
                "Included",
                "Planned",
                "Planned",
                "Planned",
                "Planned",
            ],
        }
    )

    st.dataframe(
        plan_comparison,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "This is a subscription-plan demonstration. Payment processing, "
        "subscription activation, expiry management, automatic monitoring "
        "and email notifications have not been implemented yet."
    )
# =========================================================
# SELLER TRUST
# =========================================================

elif page == "Seller Trust":

    st.markdown(
        f"## 🛡️ Seller Trust: {product_name}"
    )

    st.write(
        "Compare seller and purchase-protection indicators "
        "for your selected product."
    )

    show_demo_notice()

    if trust.empty:

        st.error(
            "Trust dataset not found. Run the trust-data generator "
            "shown in Step 2 below."
        )

    else:

        product_trust = trust[
            trust["product_id"].astype(str) == product_id
        ].copy()

        if product_trust.empty:

            st.warning(
                "No trust records are available for this product."
            )

        else:

            for column in [
                "verified_seller",
                "warranty_available",
                "return_policy",
            ]:

                product_trust[column] = (
                    product_trust[column]
                    .astype(str)
                    .str.lower()
                    .isin(["true", "1", "yes"])
                )

            for column in [
                "rating",
                "reviews_count",
                "complaint_count",
                "price_inr",
            ]:

                product_trust[column] = pd.to_numeric(
                    product_trust[column],
                    errors="coerce",
                )

            product_trust["complaint_count"] = (
                product_trust["complaint_count"].fillna(0)
            )

            total = len(product_trust)

            verified_count = int(
                product_trust["verified_seller"].sum()
            )

            warranty_count = int(
                product_trust["warranty_available"].sum()
            )

            return_count = int(
                product_trust["return_policy"].sum()
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Listings compared",
                total,
            )

            col2.metric(
                "Verified indicators",
                f"{verified_count}/{total}",
            )

            col3.metric(
                "Warranty listed",
                f"{warranty_count}/{total}",
            )

            col4.metric(
                "Return policy listed",
                f"{return_count}/{total}",
            )

            st.markdown("### 🚨 Important alerts")

            complaint_threshold = product_trust[
                "complaint_count"
            ].quantile(0.75)

            high_complaints = product_trust[
                product_trust["complaint_count"]
                >= complaint_threshold
            ]

            if (
                not high_complaints.empty
                and complaint_threshold > 0
            ):

                retailers_text = ", ".join(
                    high_complaints["retailer_name"].astype(str)
                )

                st.markdown(
                    f"""
                    <div class="alert-red">
                        <strong>Higher complaint-count indicator:</strong>
                        {retailers_text}.<br>
                        Review seller information carefully. These are
                        simulated complaint values, not real complaint records.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            missing_warranty = product_trust[
                ~product_trust["warranty_available"]
            ]

            if not missing_warranty.empty:

                retailers_text = ", ".join(
                    missing_warranty["retailer_name"].astype(str)
                )

                st.markdown(
                    f"""
                    <div class="alert-yellow">
                        <strong>Warranty not listed in demo data:</strong>
                        {retailers_text}.<br>
                        Check the actual manufacturer warranty and seller terms.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            missing_returns = product_trust[
                ~product_trust["return_policy"]
            ]

            if not missing_returns.empty:

                retailers_text = ", ".join(
                    missing_returns["retailer_name"].astype(str)
                )

                st.markdown(
                    f"""
                    <div class="alert-yellow">
                        <strong>Return policy not listed in demo data:</strong>
                        {retailers_text}.<br>
                        Confirm the product's return and exchange conditions.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                "### Retailer-by-retailer comparison"
            )

            view = product_trust.copy()

            view["Seller verification"] = (
                view["verified_seller"]
                .map({
                    True: "Yes (simulated)",
                    False: "No (simulated)",
                })
            )

            view["Warranty"] = (
                view["warranty_available"]
                .map({
                    True: "Listed (simulated)",
                    False: "Not listed (simulated)",
                })
            )

            view["Return / exchange"] = (
                view["return_policy"]
                .map({
                    True: "Listed (simulated)",
                    False: "Not listed (simulated)",
                })
            )

            view = view.rename(
                columns={
                    "retailer_name": "Retailer",
                    "price_inr": "Price (₹)",
                    "rating": "Rating / 5",
                    "reviews_count": "Review count",
                    "complaint_count": "Complaint count",
                }
            )

            columns = [
                "Retailer",
                "Price (₹)",
                "Seller verification",
                "Rating / 5",
                "Review count",
                "Complaint count",
                "Return / exchange",
                "Warranty",
            ]

            st.dataframe(
                view[columns].sort_values(
                    "Price (₹)",
                    na_position="last",
                ),
                use_container_width=True,
                hide_index=True,
            )

            st.markdown(
                "### What should you check before buying?"
            )

            st.write(
                "- **Seller verification:** check the actual seller's verified badge.\n"
                "- **Customer ratings:** look at both the rating and review count.\n"
                "- **Complaints:** a high count is a reason to investigate, not proof of fraud.\n"
                "- **Return policy:** confirm return and exchange deadlines.\n"
                "- **Warranty:** confirm the duration and whether it is manufacturer-backed."
            )

            st.caption(
                "All trust values in this prototype are simulated. "
                "They must be replaced with authorized, verifiable information "
                "before being used for real purchasing recommendations."
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        <strong>TrustCart AI</strong><br>
        Shop Smarter. Compare Better. Buy with Confidence.<br>
        Educational prototype · Simulated data · Not a live shopping service
    </div>
    """,
    unsafe_allow_html=True,
)