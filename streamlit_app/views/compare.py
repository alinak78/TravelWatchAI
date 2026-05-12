import streamlit as st
import plotly.graph_objects as go

from skyscanner_api import skyscanner_search_url


def _history_points(watch):
    history = watch.get("price_history") or []
    points = [
        (str(item.get("date", "")), float(item.get("price", 0)))
        for item in history
        if item.get("date") and item.get("price")
    ]
    if points:
        return points
    return [("Now", float(watch["current_price"]))]


def render():
    watches = st.session_state.watches

    st.markdown('<h2 style="font-size:24px;font-weight:700;color:#111;margin:0 0 8px 0;">Compare Routes</h2>', unsafe_allow_html=True)
    st.caption("Side-by-side comparison of tracked routes — current lowest price, AI predicted price, "
               "BUY/WAIT recommendation, and the estimated saving vs. your target.")

    if len(watches) < 2:
        st.info("Add at least 2 routes to compare.")
        if st.button("➕ Add New Watch"):
            st.session_state.page = "Add New Watch"
            st.rerun()
        return

    n = min(3, len(watches))

    # ── Route dropdown selectors ──────────────────────────────────────────────
    all_labels = [f"{w['origin']} - {w['dest']} ({w['dep_date']})" for w in watches]
    cols = st.columns(n)
    selected_watches = []
    used_ids: set[int] = set()
    for i in range(n):
        with cols[i]:
            # Default to the i-th watch that hasn't been picked yet
            default_idx = next(
                (j for j, w in enumerate(watches) if w["id"] not in used_ids),
                0,
            )
            chosen = st.selectbox(
                f"Route {i + 1}",
                all_labels,
                index=default_idx,
                key=f"compare_sel_{i}",
                label_visibility="collapsed",
            )
            chosen_w = next(w for w, lbl in zip(watches, all_labels) if lbl == chosen)
            selected_watches.append(chosen_w)
            used_ids.add(chosen_w["id"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Real observed-price mini charts ───────────────────────────────────────
    palette = [
        ("rgba(59,130,246,0.9)", "rgba(59,130,246,0.15)"),
        ("rgba(34,197,94,0.9)",  "rgba(34,197,94,0.15)"),
        ("rgba(239,68,68,0.9)",  "rgba(239,68,68,0.15)"),
    ]
    chart_cols = st.columns(n)
    for i, w in enumerate(selected_watches):
        with chart_cols[i]:
            points = _history_points(w)
            x = [p[0] for p in points]
            y = [p[1] for p in points]
            lc, fc = palette[i % len(palette)]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x, y=y, mode="lines+markers" if len(points) == 1 else "lines",
                line=dict(color=lc, width=2),
                marker=dict(size=6, color=lc),
                fill="tozeroy", fillcolor=fc,
            ))
            fig.update_layout(
                height=160, margin=dict(l=0, r=0, t=0, b=20),
                paper_bgcolor="white", plot_bgcolor="white", showlegend=False,
                xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#9ca3af")),
                yaxis=dict(showgrid=False, visible=False),
            )
            st.plotly_chart(
                fig, use_container_width=True,
                config={"displayModeBar": False},
                key=f"compare_price_chart_{i}_{w['id']}",
            )
            st.caption(f"{len(points)} observed price point{'s' if len(points) != 1 else ''}")

    # ── Stats row ─────────────────────────────────────────────────────────────
    stat_cols = st.columns(n)
    for i, w in enumerate(selected_watches):
        currency = w.get("currency", "USD")
        is_buy = w["recommendation"] == "BUY"
        pred = float(w.get("predicted_price") or w["current_price"])

        # Estimated saving = target - current (positive means already below target).
        saving_vs_target = w["target"] - w["current_price"]
        save_color = "#22c55e" if saving_vs_target >= 0 else "#ef4444"
        save_sign = "+" if saving_vs_target >= 0 else "-"

        # If model predicts a rise, the saving from booking now is current - predicted (positive=saving).
        future_saving = pred - w["current_price"]  # positive if predicted will be higher than current
        future_color = "#22c55e" if future_saving >= 0 else "#ef4444"
        future_sign = "+" if future_saving >= 0 else "-"

        with stat_cols[i]:
            st.markdown(f"""
            <div style="margin-bottom:4px;">
                <div class="sec-label">Route</div>
                <div style="font-size:16px; font-weight:700; color:#111; margin-bottom:12px;">
                    {w['origin']} → {w['dest']}
                    <div style="font-size:11px; font-weight:500; color:#9ca3af; margin-top:2px;">{w['dep_date']}</div>
                </div>

                <div class="sec-label">Current Lowest Price</div>
                <div style="font-size:22px; font-weight:700; color:#111; margin-bottom:12px;">{currency} {w['current_price']:,}</div>

                <div class="sec-label">Predicted Price</div>
                <div style="font-size:18px; font-weight:700; color:#111; margin-bottom:12px;">{currency} {pred:,.0f}</div>

                <div class="sec-label">Target Price</div>
                <div style="font-size:16px; font-weight:600; color:#374151; margin-bottom:12px;">{currency} {w['target']:,}</div>

                <div class="sec-label">Recommendation</div>
                <div style="margin-bottom:12px;">
                    <span class="badge-{'buy' if is_buy else 'wait'}">{w['recommendation']} ({w['confidence']}%)</span>
                </div>

                <div class="sec-label">Estimated Saving (vs Target)</div>
                <div style="font-size:16px; font-weight:700; color:{save_color}; margin-bottom:6px;">
                    {save_sign}{currency} {abs(saving_vs_target):,.0f}
                </div>

                <div class="sec-label">If You Wait (vs Predicted)</div>
                <div style="font-size:14px; font-weight:600; color:{future_color}; margin-bottom:12px;">
                    Book now saves {future_sign}{currency} {abs(future_saving):,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Action row
            booking_url = skyscanner_search_url(
                w["origin"], w["dest"], w["dep_date"],
                cabin_class=w.get("class", "Economy"),
                adults=w.get("adults", 1),
            )
            a, b = st.columns(2)
            with a:
                if st.button("Detail", key=f"cmp_detail_{w['id']}_{i}", use_container_width=True):
                    st.session_state.selected_watch_id = w["id"]
                    st.session_state.page = "Task Detail"
                    st.rerun()
            with b:
                st.link_button(
                    "Book" if is_buy else "Search",
                    booking_url,
                    type="primary" if is_buy else "secondary",
                    use_container_width=True,
                )

    # ── Verdict ──────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    best = min(selected_watches, key=lambda w: w["current_price"])
    best_currency = best.get("currency", "USD")
    st.success(
        f"Best deal right now: **{best['origin']} → {best['dest']}** at "
        f"**{best_currency} {best['current_price']:,}** on {best['dep_date']} "
        f"({best['recommendation']}, {best['confidence']}% confidence)."
    )
