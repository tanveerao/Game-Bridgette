"""Rendering helpers: flash-phase card chips, the marking grid, and CSS."""

import streamlit as st

from . import game

SUIT_CODE = {"♠": "S", "♥": "H", "♦": "D", "♣": "C"}

# (background, text) for the give-me-the-answer reveal
REVEAL_STYLES = {
    "hit": ("#16a34a", "#ffffff"),     # green: marked and actually played
    "wrong": ("#dc2626", "#ffffff"),   # red: marked but never played
    "missed": ("#eab308", "#1f2937"),  # yellow: played but not marked
}


def inject_base_css():
    st.markdown(
        """<style>
        [class*="st-key-mark_"] button {
            padding: 0.15rem 0.05rem;
            min-height: 2.1rem;
            line-height: 1.1;
        }
        [class*="st-key-mark_"] button p {
            font-size: 0.85rem;
            font-weight: 700;
        }
        </style>""",
        unsafe_allow_html=True,
    )


def _card_color(suit):
    return "#c1121f" if suit in game.RED_SUITS else "#111111"


def card_chip(card, big=True):
    rank, suit = card
    size = "1.9rem" if big else "1.2rem"
    pad = "0.45rem 0.85rem" if big else "0.25rem 0.55rem"
    return (
        f'<span style="display:inline-block;background:#fdfdf8;border:1px solid #b9b3a5;'
        f"border-radius:10px;padding:{pad};margin:0.15rem;font-size:{size};font-weight:700;"
        f"font-family:Georgia,'Times New Roman',serif;color:{_card_color(suit)};"
        f'box-shadow:1px 2px 4px rgba(0,0,0,0.25);">{rank}{suit}</span>'
    )


def render_flash(tricks, difficulty):
    """Show the current trick at the bottom, prior tricks (per difficulty) above it."""
    mode = game.DIFFICULTIES[difficulty]["visible"]
    if mode == "current":
        visible = tricks[-1:]
    elif mode == "previous":
        visible = tricks[-2:]
    else:  # "all"
        visible = list(tricks)

    offset = len(tricks) - len(visible)
    for i, trick in enumerate(visible):
        trick_no = offset + i + 1
        is_current = trick_no == len(tricks)
        label = "This trick" if is_current else f"Trick {trick_no}"
        st.markdown(
            f"<div style='margin:0.5rem 0 0.1rem;font-size:0.8rem;color:#8a8578;'>{label}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div>" + "".join(card_chip(c, big=is_current) for c in trick) + "</div>",
            unsafe_allow_html=True,
        )


def render_grid(card_count, marked, disabled, reveal_map, toggle_cb):
    """The marking board: one button per card in the deck, one row per suit.

    Marked cards render as primary buttons. When reveal_map is given, buttons
    are color-coded green / red / yellow via CSS keyed on Streamlit's
    st-key-* container classes.
    """
    ranks = game.ALL_RANKS[:card_count]
    css = []
    for suit in game.SUITS:
        cols = st.columns(card_count, gap="small")
        for i, rank in enumerate(ranks):
            card = (rank, suit)
            key = f"mark_{SUIT_CODE[suit]}_{rank}"
            is_marked = card in marked
            if not is_marked and suit in game.RED_SUITS:
                label = f":red[{rank}{suit}]"
            else:
                label = f"{rank}{suit}"
            cols[i].button(
                label,
                key=key,
                disabled=disabled,
                type="primary" if is_marked else "secondary",
                on_click=toggle_cb,
                args=(card,),
                use_container_width=True,
            )
            if reveal_map and card in reveal_map:
                bg, fg = REVEAL_STYLES[reveal_map[card]]
                css.append(
                    f".st-key-{key} button{{background-color:{bg} !important;"
                    f"border-color:{bg} !important;opacity:1 !important;}}"
                    f".st-key-{key} button p,.st-key-{key} button span"
                    f"{{color:{fg} !important;}}"
                )
    if css:
        st.markdown("<style>" + "".join(css) + "</style>", unsafe_allow_html=True)
