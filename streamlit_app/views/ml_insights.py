import json
import os

import plotly.graph_objects as go
from sklearn.metrics import auc
import streamlit as st


ML_SECTIONS = [
    "View Data",
    "Data Exploration",
    "Preprocessing",
    "Model Training",
    "Model Evaluation",
    "Best Model Selection",
]


@st.cache_data
def load_model_data():
    base = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base, "model_weights", "travelwatch_models.json")
    with open(path, "r") as f:
        return json.load(f)


def get_roc_curve(model_data):
    roc_curve = model_data.get("roc_curve", {})
    fpr = roc_curve.get("fpr")
    tpr = roc_curve.get("tpr")
    if not fpr or not tpr:
        return None, None
    return fpr, tpr


def _metric_card(label, value):
    return f"""
    <div style="border:1px solid #ebebeb; border-radius:8px; padding:12px 14px; text-align:center;">
        <div style="font-size:12px; color:#9ca3af; margin-bottom:5px;">{label}</div>
        <div style="font-size:18px; font-weight:700; color:#111;">{value}</div>
    </div>
    """


def _section_picker():
    current = st.session_state.get("ml_section", "Model Evaluation")
    if current not in ML_SECTIONS:
        current = "Model Evaluation"

    cols = st.columns(len(ML_SECTIONS))
    for i, section in enumerate(ML_SECTIONS):
        with cols[i]:
            if st.button(
                section,
                key=f"ml_section_{section}",
                use_container_width=True,
                type="primary" if section == current else "secondary",
            ):
                st.session_state.ml_section = section
                st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    return current


def _render_model_evaluation(data):
    clf = data["classification"]
    reg = data["regression"]

    st.markdown('<div class="sec-label">Model</div>', unsafe_allow_html=True)
    model = st.radio(
        "Model",
        ["Logistic Regression", "KNN"],
        label_visibility="collapsed",
        horizontal=True,
    )
    m_data = clf["logistic_regression"] if model == "Logistic Regression" else clf["knn"]

    f1 = m_data["f1"]
    auc = m_data["auc"]
    cm = m_data["confusion_matrix"]
    acc = (cm[0][0] + cm[1][1]) / (cm[0][0] + cm[0][1] + cm[1][0] + cm[1][1])

    st.markdown('<div class="sec-label">Classification Performance</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Accuracy", f"{acc*100:.1f}%")

    with col2:
        st.metric("F1 Score", f"{f1:.3f}")

    with col3:
        st.metric("AUC-ROC", f"{auc:.3f}")

    st.markdown('<div class="sec-label">Confusion Matrix</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <table style="border-collapse:collapse; margin-bottom:20px; font-family:Inter,sans-serif;">
        <thead>
            <tr>
                <td style="padding:8px 16px;"></td>
                <td style="padding:8px 24px; font-size:13px; color:#374151; font-weight:500; text-align:center;">Predicted BUY</td>
                <td style="padding:8px 24px; font-size:13px; color:#374151; font-weight:500; text-align:center;">Predicted WAIT</td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding:8px 16px; font-size:13px; color:#374151; font-weight:500;">Actual BUY</td>
                <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center; font-size:18px; font-weight:600; color:#111;">{cm[0][0]}</td>
                <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center; font-size:18px; font-weight:600; color:#111;">{cm[0][1]}</td>
            </tr>
            <tr>
                <td style="padding:8px 16px; font-size:13px; color:#374151; font-weight:500;">Actual WAIT</td>
                <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center; font-size:18px; font-weight:600; color:#111;">{cm[1][0]}</td>
                <td style="border:1px solid #d1d5db; padding:16px 32px; text-align:center; font-size:18px; font-weight:600; color:#111;">{cm[1][1]}</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">ROC Curve</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fpr, tpr = get_roc_curve(m_data)
    if fpr is not None and tpr is not None:
        fig.add_trace(go.Scatter(
            x=fpr, y=tpr, mode="lines",
            line=dict(color="#3b82f6", width=2.5),
            name=f"AUC = {auc:.3f}",
        ))
    else:
        st.info("ROC curve points are not saved in the current model artifact yet.")
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode="lines",
        line=dict(color="#e5e7eb", dash="dash", width=1),
        name="Random",
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(title="False Positive Rate", gridcolor="#f5f5f5"),
        yaxis=dict(title="True Positive Rate", gridcolor="#f5f5f5"),
        legend=dict(font=dict(size=11)),
        font=dict(family="Inter"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="ml_eval_roc")

    ridge = reg["ridge"]
    lasso = reg["lasso"]
    st.markdown('<div class="sec-label">Regression Evaluation</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="tw-card" style="display:grid; grid-template-columns:repeat(2,1fr); gap:12px; margin-bottom:20px;">
        <div class="tw-card-sm">
            <div style="font-size:13px; font-weight:700; color:#111; margin-bottom:8px;">Ridge Regression</div>
            <div style="font-size:13px; color:#374151;">R2 = {ridge['r2']:.4f}</div>
            <div style="font-size:13px; color:#374151;">RMSE = {ridge['rmse']:.1f}</div>
            <div style="font-size:13px; color:#374151;">MAE = {ridge['mae']:.1f}</div>
        </div>
        <div class="tw-card-sm">
            <div style="font-size:13px; font-weight:700; color:#111; margin-bottom:8px;">Lasso Regression</div>
            <div style="font-size:13px; color:#374151;">R2 = {lasso['r2']:.4f}</div>
            <div style="font-size:13px; color:#374151;">RMSE = {lasso['rmse']:.1f}</div>
            <div style="font-size:13px; color:#374151;">MAE = {lasso['mae']:.1f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _render_model_training(data):
    lc = data["learning_curves"]
    reg = data["regression"]
    clf = data["classification"]

    st.markdown('<div class="sec-label">Training Pipeline</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tw-card" style="margin-bottom:20px;">
        <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:12px;">
            <div style="border:1px solid #ebebeb; border-radius:8px; padding:12px;"><b>1. Clean</b><br><span style="color:#6b7280;font-size:13px;">Drop null rows and clip outliers.</span></div>
            <div style="border:1px solid #ebebeb; border-radius:8px; padding:12px;"><b>2. Encode</b><br><span style="color:#6b7280;font-size:13px;">One-hot categorical flight fields.</span></div>
            <div style="border:1px solid #ebebeb; border-radius:8px; padding:12px;"><b>3. Scale</b><br><span style="color:#6b7280;font-size:13px;">Normalize numeric inputs.</span></div>
            <div style="border:1px solid #ebebeb; border-radius:8px; padding:12px;"><b>4. Train</b><br><span style="color:#6b7280;font-size:13px;">Fit classifier and regression models.</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Saved Model Families</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="tw-card" style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:20px;">
        {_metric_card("Classification", "Logistic Regression / KNN")}
        {_metric_card("Regression", "Ridge / Lasso")}
        {_metric_card("Regression Features", f"{len(reg.get('feature_cols', []))}")}
    </div>
    <div style="font-size:12px; color:#6b7280; margin-bottom:20px;">
        Current classification winner: <b>{clf.get('best_model')}</b>. Current regression winner: <b>{reg.get('best_model')}</b>.
    </div>
    """, unsafe_allow_html=True)

    _render_learning_curves(lc)


def _render_learning_curves(lc):
    st.markdown('<div class="sec-label">Learning Curves (Ridge vs Lasso)</div>', unsafe_allow_html=True)
    fig_lc = go.Figure()
    fig_lc.add_trace(go.Scatter(
        x=lc["ridge_sizes"], y=lc["ridge_train_r2"],
        mode="lines+markers", name="Ridge Train",
        line=dict(color="#3b82f6", width=2),
    ))
    fig_lc.add_trace(go.Scatter(
        x=lc["ridge_sizes"], y=lc["ridge_val_r2"],
        mode="lines+markers", name="Ridge Val",
        line=dict(color="#3b82f6", dash="dash", width=2),
    ))
    fig_lc.add_trace(go.Scatter(
        x=lc["lasso_sizes"], y=lc["lasso_train_r2"],
        mode="lines+markers", name="Lasso Train",
        line=dict(color="#e05c3a", width=2),
    ))
    fig_lc.add_trace(go.Scatter(
        x=lc["lasso_sizes"], y=lc["lasso_val_r2"],
        mode="lines+markers", name="Lasso Val",
        line=dict(color="#e05c3a", dash="dash", width=2),
    ))
    fig_lc.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(title="Training Set Size", gridcolor="#f5f5f5"),
        yaxis=dict(title="R2 Score", gridcolor="#f5f5f5"),
        legend=dict(font=dict(size=11), orientation="h", y=-0.25),
        font=dict(family="Inter"),
    )
    st.plotly_chart(fig_lc, use_container_width=True, config={"displayModeBar": False}, key="ml_training_lc")


def _render_best_model_selection(data):
    clf = data["classification"]
    reg = data["regression"]
    ridge = reg["ridge"]
    lasso = reg["lasso"]

    lr = clf["logistic_regression"]
    knn = clf["knn"]
    rows = [
        ("Logistic Regression", "Classification", "F1", lr["f1"], clf["best_model"] == "Logistic Regression"),
        ("KNN", "Classification", "F1", knn["f1"], clf["best_model"] == "KNN"),
        ("Ridge", "Regression", "R2", ridge["r2"], reg["best_model"] == "Ridge"),
        ("Lasso", "Regression", "R2", lasso["r2"], reg["best_model"] == "Lasso"),
    ]

    st.markdown('<div class="sec-label">Best Model Selection</div>', unsafe_allow_html=True)
    for name, task, metric, score, winner in rows:
        badge = '<span class="badge-buy">Selected</span>' if winner else '<span class="badge-wait">Candidate</span>'
        st.markdown(f"""
        <div class="tw-card-sm" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div>
                <div style="font-size:15px; font-weight:700; color:#111;">{name}</div>
                <div style="font-size:12px; color:#6b7280;">{task} model selected by {metric}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:14px; font-weight:700; color:#111;">{metric}: {score:.4f}</div>
                {badge}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.success(
        f"Deployed recommendation stack: {clf['best_model']} for BUY/WAIT classification "
        f"and {reg['best_model']} for price prediction."
    )


def _render_preprocessing(data):
    reg = data["regression"]
    feature_cols = reg.get("feature_cols", [])

    st.markdown('<div class="sec-label">Preprocessing Steps</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tw-card" style="margin-bottom:20px;">
        <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:12px;">
            <div style="border:1px solid #ebebeb; border-radius:8px; padding:12px;"><b>Missing Values</b><br><span style="color:#6b7280;font-size:13px;">Rows with missing training values are removed.</span></div>
            <div style="border:1px solid #ebebeb; border-radius:8px; padding:12px;"><b>Outliers</b><br><span style="color:#6b7280;font-size:13px;">Numeric outliers are clipped with IQR bounds.</span></div>
            <div style="border:1px solid #ebebeb; border-radius:8px; padding:12px;"><b>Categorical Encoding</b><br><span style="color:#6b7280;font-size:13px;">Airline, cities, stops, times, and class become one-hot columns.</span></div>
            <div style="border:1px solid #ebebeb; border-radius:8px; padding:12px;"><b>Numeric Scaling</b><br><span style="color:#6b7280;font-size:13px;">Duration and days-left style features are normalized.</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Processed Feature Columns</div>', unsafe_allow_html=True)
    st.dataframe(
        [{"feature": col} for col in feature_cols],
        use_container_width=True,
        hide_index=True,
        height=360,
    )


def _render_data_exploration():
    from views import view_data

    df, path = view_data._load_dataset()
    if df is None:
        st.warning("Dataset not found. Place Clean_Dataset.csv at datasets/Clean_Dataset.csv.")
        return

    st.caption(f"Loaded from `{path}` - {len(df):,} rows x {len(df.columns)} columns.")
    cols = st.columns(4)
    cols[0].metric("Rows", f"{len(df):,}")
    cols[1].metric("Columns", f"{len(df.columns):,}")
    cols[2].metric("Missing Cells", f"{int(df.isna().sum().sum()):,}")
    cols[3].metric("Numeric Columns", f"{len(df.select_dtypes(include='number').columns):,}")

    numeric_df = df.select_dtypes(include="number")
    if "price" in df.columns:
        st.markdown('<div class="sec-label">Price Distribution</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df["price"], nbinsx=60, marker_color="#3b82f6"))
        fig.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(title="Price", gridcolor="#f5f5f5"),
            yaxis=dict(title="Count", gridcolor="#f5f5f5"),
            font=dict(family="Inter"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="ml_explore_price")

    if numeric_df.shape[1] >= 2:
        st.markdown('<div class="sec-label">Numeric Correlation</div>', unsafe_allow_html=True)
        corr = numeric_df.corr().round(3)
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            colorbar=dict(title="r"),
        ))
        fig.update_layout(
            height=420,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(family="Inter"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="ml_explore_corr")


def render():
    st.markdown(
        '<h2 style="font-size:24px;font-weight:700;color:#111;margin:0 0 20px 0;">ML Insights</h2>',
        unsafe_allow_html=True,
    )
    section = _section_picker()

    if section == "View Data":
        from views import view_data

        view_data.render()
        return

    try:
        data = load_model_data()
    except FileNotFoundError:
        st.warning("Model weights not found. Please run the training notebook first.")
        return

    if section == "Data Exploration":
        _render_data_exploration()
    elif section == "Preprocessing":
        _render_preprocessing(data)
    elif section == "Model Training":
        _render_model_training(data)
    elif section == "Best Model Selection":
        _render_best_model_selection(data)
    else:
        _render_model_evaluation(data)
