"""
View Data page — shows the dataset (Clean_Dataset.csv) and the preprocessing
TravelWatchAI applies before model training.
"""
import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Candidate dataset locations — repo root has `datasets/Clean_Dataset.csv`,
# and the notebook may save a processed copy alongside the model weights.
_DATASET_CANDIDATES = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "datasets", "Clean_Dataset.csv"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "Clean_Dataset.csv"),
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Clean_Dataset.csv"),
]


@st.cache_data(show_spinner=False)
def _load_dataset() -> tuple[pd.DataFrame | None, str | None]:
    for path in _DATASET_CANDIDATES:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                if df.columns[0].lower().startswith("unnamed"):
                    df = df.drop(columns=df.columns[0])
                return df, path
            except Exception as e:
                st.error(f"Failed to read {path}: {e}")
                return None, None
    return None, None


def _preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mirror the preprocessing described in the README:
    - drop missing values
    - one-hot encode categorical features
    - normalize numeric features
    - clip outliers via IQR
    """
    work = df.dropna().copy()

    # Numeric vs categorical
    numeric = [c for c in work.columns if pd.api.types.is_numeric_dtype(work[c]) and c != "price"]
    categorical = [c for c in work.columns if not pd.api.types.is_numeric_dtype(work[c])]

    # IQR-based outlier clipping on numeric features (incl. price)
    for col in numeric + (["price"] if "price" in work.columns else []):
        q1, q3 = work[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        work[col] = work[col].clip(lower=lo, upper=hi)

    # One-hot
    if categorical:
        work = pd.get_dummies(work, columns=categorical, drop_first=False)

    # Standardize numeric features (z-score), but leave price as target
    for col in numeric:
        mu, sigma = work[col].mean(), work[col].std()
        if sigma > 0:
            work[col] = (work[col] - mu) / sigma

    return work


def render():
    st.markdown('<h2 style="font-size:24px;font-weight:700;color:#111;margin:0 0 20px 0;">View Data</h2>', unsafe_allow_html=True)

    df, path = _load_dataset()
    if df is None:
        st.warning(
            "Dataset not found. Download `Clean_Dataset.csv` from Kaggle "
            "(https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction) "
            "and place it at `datasets/Clean_Dataset.csv`."
        )
        return

    st.caption(f"Loaded from `{path}` — {len(df):,} rows × {len(df.columns)} columns.")

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab_preview, tab_schema, tab_missing, tab_dist, tab_corr, tab_processed = st.tabs([
        "Preview", "Columns", "Missing Values", "Price Distribution", "Correlation", "Processed Features",
    ])

    # Preview ────────────────────────────────────────────────────────────────
    with tab_preview:
        rows = st.slider("Rows to preview", 5, 200, 20, step=5)
        st.dataframe(df.head(rows), use_container_width=True, height=420)

    # Columns / dtypes ───────────────────────────────────────────────────────
    with tab_schema:
        schema = pd.DataFrame({
            "column": df.columns,
            "dtype": [str(t) for t in df.dtypes],
            "non_null": df.notna().sum().values,
            "unique": [df[c].nunique(dropna=True) for c in df.columns],
            "sample": [", ".join(map(str, df[c].dropna().unique()[:3])) for c in df.columns],
        })
        st.dataframe(schema, use_container_width=True, height=420, hide_index=True)

    # Missing values ─────────────────────────────────────────────────────────
    with tab_missing:
        miss = df.isna().sum()
        miss_df = pd.DataFrame({
            "column": miss.index,
            "missing": miss.values,
            "missing_pct": (miss.values / len(df) * 100).round(3),
        }).sort_values("missing", ascending=False)
        st.dataframe(miss_df, use_container_width=True, hide_index=True)

        if miss_df["missing"].sum() == 0:
            st.success("No missing values in this dataset.")
        else:
            fig = px.bar(
                miss_df[miss_df["missing"] > 0],
                x="column", y="missing_pct",
                title="Missing values (%) by column",
                color_discrete_sequence=["#ef4444"],
            )
            fig.update_layout(height=320, margin=dict(l=10, r=10, t=40, b=10),
                              paper_bgcolor="white", plot_bgcolor="white")
            st.plotly_chart(fig, use_container_width=True, key="view_data_missing")

    # Price distribution ─────────────────────────────────────────────────────
    with tab_dist:
        if "price" not in df.columns:
            st.info("No `price` column in this dataset.")
        else:
            stats = df["price"].describe().to_dict()
            cols = st.columns(4)
            cols[0].metric("Mean", f"{stats['mean']:,.0f}")
            cols[1].metric("Median", f"{df['price'].median():,.0f}")
            cols[2].metric("Min", f"{stats['min']:,.0f}")
            cols[3].metric("Max", f"{stats['max']:,.0f}")

            fig = px.histogram(
                df, x="price", nbins=60,
                title="Price distribution",
                color_discrete_sequence=["#3b82f6"],
            )
            fig.update_layout(height=360, margin=dict(l=10, r=10, t=40, b=10),
                              paper_bgcolor="white", plot_bgcolor="white",
                              xaxis=dict(gridcolor="#f5f5f5"),
                              yaxis=dict(gridcolor="#f5f5f5"))
            st.plotly_chart(fig, use_container_width=True, key="view_data_price_hist")

            # Optional: price by categorical column
            cat_cols = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
            if cat_cols:
                group = st.selectbox("Group price by", cat_cols, index=0)
                fig2 = px.box(df, x=group, y="price",
                              title=f"Price by {group}",
                              color_discrete_sequence=["#22c55e"])
                fig2.update_layout(height=380, margin=dict(l=10, r=10, t=40, b=10),
                                   paper_bgcolor="white", plot_bgcolor="white",
                                   xaxis=dict(gridcolor="#f5f5f5"),
                                   yaxis=dict(gridcolor="#f5f5f5"))
                st.plotly_chart(fig2, use_container_width=True, key="view_data_price_by")

    # Correlation heatmap ────────────────────────────────────────────────────
    with tab_corr:
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.shape[1] < 2:
            st.info("Not enough numeric columns to compute a correlation matrix in the raw data — "
                    "see Processed Features for the one-hot encoded version.")
        else:
            corr = numeric_df.corr().round(3)
            fig = go.Figure(data=go.Heatmap(
                z=corr.values, x=corr.columns, y=corr.columns,
                colorscale="RdBu", zmin=-1, zmax=1,
                colorbar=dict(title="r"),
            ))
            fig.update_layout(height=420, margin=dict(l=10, r=10, t=40, b=10),
                              paper_bgcolor="white", plot_bgcolor="white",
                              title="Numeric feature correlation")
            st.plotly_chart(fig, use_container_width=True, key="view_data_corr")

    # Processed features ─────────────────────────────────────────────────────
    with tab_processed:
        st.caption(
            "Preview of the dataset after the same preprocessing the training notebook uses: "
            "drop missing rows, IQR-clip numeric outliers, one-hot encode categorical features, "
            "and z-score numeric features."
        )
        processed = _preprocess(df)
        st.write(f"Resulting shape: **{processed.shape[0]:,} rows × {processed.shape[1]} features**")
        st.dataframe(processed.head(50), use_container_width=True, height=420)

        # Correlation with price after processing
        if "price" in processed.columns:
            corr_to_price = (
                processed.corr(numeric_only=True)["price"]
                .drop(labels=["price"], errors="ignore")
                .sort_values(key=lambda s: s.abs(), ascending=False)
                .head(15)
            )
            fig = px.bar(
                x=corr_to_price.values, y=corr_to_price.index,
                orientation="h",
                title="Top 15 processed features correlated with price",
                color=corr_to_price.values,
                color_continuous_scale="RdBu", range_color=[-1, 1],
            )
            fig.update_layout(height=460, margin=dict(l=10, r=10, t=40, b=10),
                              paper_bgcolor="white", plot_bgcolor="white",
                              xaxis_title="Pearson r", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True, key="view_data_corr_price")
