import streamlit as st

from skyscanner_api import skyscanner_search_url


def _status(w: dict) -> tuple[str, str]:
    """Return (label, color) describing the watch state vs. its target."""
    cur, tgt = w["current_price"], w["target"]
    if cur <= tgt:
        return ("At/Below Target", "#22c55e")
    if cur <= tgt * 1.05:
        return ("Near Target", "#f59e0b")
    return ("Above Target", "#ef4444")


def render():
    watches = sorted(st.session_state.watches, key=lambda w: w["id"], reverse=True)

    # ── Header ────────────────────────────────────────────────────────────────
    col_title, col_btn = st.columns([5, 1])
    with col_title:
        st.markdown('<h2 style="font-size:24px;font-weight:700;color:#111;margin:0;">All Watches</h2>', unsafe_allow_html=True)
    with col_btn:
        if st.button("＋  Add New Watch", type="primary", use_container_width=True):
            st.session_state.page = "Add New Watch"
            st.rerun()

    st.caption(f"{len(watches)} active watch{'es' if len(watches) != 1 else ''}.")
    st.markdown("<br>", unsafe_allow_html=True)

    if not watches:
        st.info("You aren't tracking any routes yet. Click **Add New Watch** to start.")
        return

    # ── Filters ──────────────────────────────────────────────────────────────
    col_f1, col_f2, _ = st.columns([1.2, 1.2, 4])
    with col_f1:
        rec_filter = st.selectbox("Recommendation", ["All", "BUY", "WAIT"], label_visibility="collapsed")
    with col_f2:
        sort_by = st.selectbox(
            "Sort",
            ["Newest", "Cheapest first", "Confidence ↓", "Departure date"],
            label_visibility="collapsed",
        )

    if rec_filter != "All":
        watches = [w for w in watches if w["recommendation"] == rec_filter]
    if sort_by == "Cheapest first":
        watches.sort(key=lambda w: w["current_price"])
    elif sort_by == "Confidence ↓":
        watches.sort(key=lambda w: w["confidence"], reverse=True)
    elif sort_by == "Departure date":
        watches.sort(key=lambda w: str(w.get("dep_date", "")))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Header row ───────────────────────────────────────────────────────────
    header_cols = st.columns([1.6, 1.4, 1.3, 1.3, 1.6, 1.2, 1.4])
    headers = ["Route", "Depart", "Current", "Target", "Recommendation", "Status", "Action"]
    for col, label in zip(header_cols, headers):
        col.markdown(
            f"<div style='font-size:11px; font-weight:600; color:#9ca3af; "
            f"letter-spacing:0.06em; text-transform:uppercase;'>{label}</div>",
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='margin:6px 0; border-color:#ebebeb;'>", unsafe_allow_html=True)

    # ── Rows ─────────────────────────────────────────────────────────────────
    for w in watches:
        currency = w.get("currency", "USD")
        is_buy = w["recommendation"] == "BUY"
        status_label, status_color = _status(w)
        booking_url = skyscanner_search_url(
            w["origin"], w["dest"], w["dep_date"],
            cabin_class=w.get("class", "Economy"),
            adults=w.get("adults", 1),
        )

        cols = st.columns([1.6, 1.4, 1.3, 1.3, 1.6, 1.2, 1.4])
        cols[0].markdown(
            f"<div style='font-weight:600; color:#111;'>{w['origin']} - {w['dest']}</div>"
            f"<div style='font-size:11px; color:#9ca3af;'>ID #{w['id']}</div>",
            unsafe_allow_html=True,
        )
        cols[1].markdown(
            f"<div style='color:#111;'>{w.get('dep_date', '—')}</div>"
            f"<div style='font-size:11px; color:#9ca3af;'>Arr {w.get('arr_date', '—')}</div>",
            unsafe_allow_html=True,
        )
        cols[2].markdown(
            f"<div style='font-weight:600; color:#111;'>{currency} {w['current_price']:,}</div>",
            unsafe_allow_html=True,
        )
        cols[3].markdown(
            f"<div style='color:#111;'>{currency} {w['target']:,}</div>",
            unsafe_allow_html=True,
        )
        badge_class = "badge-buy" if is_buy else "badge-wait"
        cols[4].markdown(
            f"<span class='{badge_class}'>{w['recommendation']} ({w['confidence']}%)</span>",
            unsafe_allow_html=True,
        )
        cols[5].markdown(
            f"<span style='color:{status_color}; font-weight:600; font-size:13px;'>{status_label}</span>",
            unsafe_allow_html=True,
        )
        with cols[6]:
            sub = st.columns(2)
            with sub[0]:
                if st.button("Detail", key=f"sa_detail_{w['id']}", use_container_width=True):
                    st.session_state.selected_watch_id = w["id"]
                    st.session_state.page = "Task Detail"
                    st.rerun()
            with sub[1]:
                st.link_button(
                    "Book" if is_buy else "Search",
                    booking_url,
                    type="primary" if is_buy else "secondary",
                    use_container_width=True,
                )
        st.markdown("<hr style='margin:6px 0; border-color:#f0f0f0;'>", unsafe_allow_html=True)
