import streamlit as st
import plotly.graph_objects as go

from skyscanner_api import skyscanner_search_url, fetch_top_itineraries, _api_key


def _history_points(watch):
    history = watch.get("price_history") or []
    points = [
        (str(item.get("date", "")), float(item.get("price", 0)), item.get("source", "estimated"))
        for item in history
        if item.get("date") and item.get("price")
    ]
    if points:
        return points
    return [("Now", float(watch["current_price"]), watch.get("price_source", "estimated"))]


def render():
    watches = st.session_state.watches
    watch_id = st.session_state.selected_watch_id
    if not watches:
        col_back, col_title = st.columns([0.3, 3])
        with col_back:
            if st.button("←"):
                st.session_state.page = "Dashboard"
                st.rerun()
        with col_title:
            st.markdown('<h2 style="font-size:22px;font-weight:700;color:#111;margin:0;">Route Details</h2>', unsafe_allow_html=True)
        st.info("No watches yet. Add a route to fetch a live Skyscanner price.")
        if st.button("＋  Add New Watch", type="primary"):
            st.session_state.page = "Add New Watch"
            st.rerun()
        return

    w = next((x for x in watches if x["id"] == watch_id), watches[0])

    currency = w.get("currency", "USD")
    booking_url = skyscanner_search_url(
        w["origin"], w["dest"], w["dep_date"],
        cabin_class=w.get("class", "Economy"),
        adults=w.get("adults", 1),
    )
    is_buy = w["recommendation"] == "BUY"

    # ── Header ────────────────────────────────────────────────────────────────
    col_back, col_title, col_del, col_book = st.columns([0.3, 3, 1, 1.4])
    with col_back:
        if st.button("←"):
            st.session_state.page = "Dashboard"
            st.rerun()
    with col_title:
        st.markdown(f'<h2 style="font-size:22px;font-weight:700;color:#111;margin:0;">Route Details ({w["origin"]} - {w["dest"]})</h2>', unsafe_allow_html=True)
    with col_del:
        if st.button("Delete Watch", use_container_width=True):
            st.session_state.watches = [x for x in watches if x["id"] != watch_id]
            st.session_state.page = "Dashboard"
            st.rerun()
    with col_book:
        if is_buy:
            st.link_button("Book Now ↗", booking_url, type="primary", use_container_width=True)
        else:
            st.link_button("Search Flights ↗", booking_url, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Route Info ────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Route Info</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="tw-card-sm" style="margin-bottom:16px;">
        <span style="font-weight:600; color:#111;">{w['origin']} - {w['dest']}</span>
        <span style="color:#9ca3af; font-size:13px;"> (Depart {w['dep_date']} - Arrive {w['arr_date']})</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Current / Target Price ────────────────────────────────────────────────
    col_cur, col_tgt = st.columns(2)
    with col_cur:
        st.markdown('<div class="sec-label">Current Price</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="tw-card-sm" style="margin-bottom:16px;">
            <span style="font-size:18px; font-weight:700; color:#111;">{currency} {w['current_price']:,}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_tgt:
        st.markdown('<div class="sec-label">Target Price</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="tw-card-sm" style="margin-bottom:16px;">
            <span style="font-size:18px; font-weight:700; color:#111;">{currency} {w['target']:,}</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Recommendation ────────────────────────────────────────────────────────
    rec_color = "#1a56db" if is_buy else "#6b7280"
    st.markdown('<div class="sec-label">Recommendation</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="tw-card-sm" style="margin-bottom:12px;">
        <span style="font-weight:700; color:{rec_color};">{w['recommendation']}</span>
        <span style="color:#9ca3af; font-size:13px;"> ({w['confidence']}% Confidence)</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Buy/Wait reason (narrative) ───────────────────────────────────────────
    pred_price = float(w.get("predicted_price") or w["current_price"])
    price_diff = pred_price - w["current_price"]
    diff_pct = (price_diff / w["current_price"] * 100) if w["current_price"] > 0 else 0
    vs_target_pct = ((w["current_price"] - w["target"]) / w["target"] * 100) if w["target"] > 0 else 0
    direction_text = "drop" if w["change_dir"] == "down" else "rise"

    if is_buy:
        reason_lines = [
            f"Current price is **{currency} {w['current_price']:,}** — "
            f"{'below' if vs_target_pct <= 0 else 'within ' + f'{vs_target_pct:.1f}% of'} your target of {currency} {w['target']:,}.",
            f"Our regression model expects the price to **{direction_text} ~{w['change_pct']}%** by departure "
            f"(predicted {currency} {pred_price:,.0f}).",
            f"The BUY/WAIT classifier returned **BUY** with {w['confidence']}% confidence.",
        ]
    else:
        reason_lines = [
            f"Current price is **{currency} {w['current_price']:,}**, which is **{vs_target_pct:+.1f}%** vs your target of {currency} {w['target']:,}.",
            f"Our regression model expects the price to **{direction_text} ~{w['change_pct']}%** by departure "
            f"(predicted {currency} {pred_price:,.0f}).",
            f"The BUY/WAIT classifier returned **WAIT** with {w['confidence']}% confidence — better deals are likely.",
        ]

    with st.container():
        st.markdown('<div class="sec-label">Why this recommendation?</div>', unsafe_allow_html=True)
        st.markdown('<div class="tw-card" style="margin-bottom:20px;">', unsafe_allow_html=True)
        for line in reason_lines:
            st.markdown(f"- {line}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Predicted Price summary card ──────────────────────────────────────────
    if w.get("predicted_price"):
        diff_color = "#22c55e" if price_diff < 0 else "#ef4444"
        arrow_sym = "↓" if price_diff < 0 else "↑"

        st.markdown('<div class="sec-label">AI Price Prediction</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="tw-card" style="display:flex; padding:0; overflow:hidden; margin-bottom:20px;">
            <div style="flex:1; padding:16px 20px; border-right:1px solid #ebebeb; text-align:center;">
                <div style="font-size:13px; font-weight:600; color:#111; margin-bottom:4px;">Predicted Price</div>
                <div style="font-size:18px; font-weight:700; color:#111;">{currency} {pred_price:,.0f}</div>
            </div>
            <div style="flex:1; padding:16px 20px; text-align:center;">
                <div style="font-size:13px; font-weight:600; color:#111; margin-bottom:4px;">Expected Change</div>
                <div style="font-size:16px; font-weight:700; color:{diff_color};">{arrow_sym} {abs(diff_pct):.1f}%</div>
                <div style="font-size:11px; color:#9ca3af;">{arrow_sym} {currency} {abs(price_diff):,.0f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Price Tracking Chart ──────────────────────────────────────────────────
    col_ct, col_dd = st.columns([4, 1])
    with col_ct:
        st.markdown('<div style="font-size:18px; font-weight:700; color:#111; margin-bottom:8px;">Observed Price Tracking</div>', unsafe_allow_html=True)
    with col_dd:
        st.selectbox("Range", ["Last 30 days", "Last 7 days", "Last 90 days"],
                     label_visibility="collapsed")

    points = _history_points(w)
    dates = [p[0] for p in points]
    prices = [p[1] for p in points]
    sources = [p[2] for p in points]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=prices, mode="lines+markers",
        line=dict(color="#3b82f6", width=2),
        marker=dict(size=5, color="#3b82f6"),
        fill="tozeroy", fillcolor="rgba(59,130,246,0.08)",
        text=sources,
        hovertemplate="%{x}<br>%{y:.0f}<br>%{text}<extra></extra>",
    ))
    max_price = max(prices) if prices else w["current_price"]
    fig.update_layout(
        height=320, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(gridcolor="#f5f5f5", tickfont=dict(size=10, color="#9ca3af")),
        yaxis=dict(gridcolor="#f5f5f5", tickfont=dict(size=10, color="#9ca3af"),
                   range=[0, max_price * 1.15]),
        font=dict(family="Inter"),
        showlegend=False,
    )

    st.markdown('<div class="tw-card" style="padding:20px;">', unsafe_allow_html=True)
    st.caption("Only observed prices are shown here. The app does not fetch historical Skyscanner backfill.")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="task_detail_price_chart")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Top flight options ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Top Flight Options</div>', unsafe_allow_html=True)
    api_key = _api_key()
    if not api_key:
        st.info("Set RAPIDAPI_KEY to see live flight options from Skyscanner.")
    else:
        with st.spinner("Fetching cheapest itineraries..."):
            options = fetch_top_itineraries(
                w["origin"], w["dest"], w["dep_date"],
                cabin_class=w.get("class", "Economy").lower(),
                adults=w.get("adults", 1),
                api_key=api_key,
                limit=5,
                currency=currency,
                origin_entity_id=w.get("origin_entity_id", ""),
                destination_entity_id=w.get("dest_entity_id", ""),
            )
        if not options:
            st.caption("No itineraries available right now.")
        else:
            for i, opt in enumerate(options):
                hours, mins = divmod(opt["duration_min"], 60)
                stops_label = "Non-stop" if opt["stops"] == 0 else f"{opt['stops']} stop{'s' if opt['stops'] > 1 else ''}"
                depart = (opt["depart"] or "").replace("T", " ")[:16]
                arrive = (opt["arrive"] or "").replace("T", " ")[:16]
                cols = st.columns([2, 2, 2, 1.4, 1.2])
                cols[0].markdown(f"**{opt['carrier']}**<br><span style='color:#9ca3af;font-size:12px;'>{stops_label}</span>", unsafe_allow_html=True)
                cols[1].markdown(f"{depart}<br><span style='color:#9ca3af;font-size:12px;'>Depart</span>", unsafe_allow_html=True)
                cols[2].markdown(f"{arrive}<br><span style='color:#9ca3af;font-size:12px;'>Arrive</span>", unsafe_allow_html=True)
                cols[3].markdown(f"{hours}h {mins:02d}m")
                cols[4].markdown(f"**{opt['currency']} {opt['price']:,}**")
                st.markdown("<hr style='margin:6px 0; border-color:#f0f0f0;'>", unsafe_allow_html=True)
            st.link_button("Open all on Skyscanner ↗", booking_url, use_container_width=False)

    # ── Switch route ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Switch Route</div>', unsafe_allow_html=True)
    options = {f"{x['origin']} - {x['dest']}": x["id"] for x in watches}
    selected = st.selectbox("Route", list(options.keys()),
                            index=list(options.values()).index(watch_id),
                            label_visibility="collapsed")
    if options[selected] != watch_id:
        st.session_state.selected_watch_id = options[selected]
        st.rerun()
