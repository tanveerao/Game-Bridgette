"""Bridgette — a card-memory practice game for bridge players.

Run with: streamlit run app.py
"""

import math
import time

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from bridgette import game, persona, ui

st.set_page_config(page_title=persona.APP_TITLE, page_icon="🃏", layout="wide")
ui.inject_base_css()


# ---------------------------------------------------------------------------
# State transitions (all mutations happen in callbacks, before the rerun)
# ---------------------------------------------------------------------------

def _deal_next_trick():
    ss = st.session_state
    trick, suit = game.deal_trick(ss.deck, ss.last_suit)
    for card in trick:
        ss.deck.remove(card)
    ss.tricks.append(trick)
    ss.last_suit = suit
    ss.phase = "flash"
    ss.flash_start = time.time()


def start_game():
    ss = st.session_state
    ss.card_count = ss.opt_card_count
    ss.difficulty = ss.opt_difficulty
    ss.total_tricks = ss.card_count
    ss.deck = game.build_deck(ss.card_count)
    ss.tricks = []
    ss.trick_num = 0
    ss.scores = []
    ss.marked = set()
    ss.check_result = None
    ss.first_checked = False
    ss.last_suit = None
    ss.screen = "game"
    _deal_next_trick()


def toggle_card(card):
    ss = st.session_state
    if card in ss.marked:
        ss.marked.discard(card)
    else:
        ss.marked.add(card)


def do_check():
    ss = st.session_state
    correct = {card for trick in ss.tricks for card in trick}
    if not ss.first_checked:
        ss.scores.append(game.score_first_guess(ss.marked, correct))
        ss.first_checked = True
    ss.check_result = "correct" if ss.marked == correct else "wrong"


def try_again():
    st.session_state.check_result = None


def reveal_answer():
    st.session_state.check_result = "revealed"


def next_trick():
    ss = st.session_state
    ss.trick_num += 1
    ss.marked = set()  # the board resets — re-mark everything from memory
    ss.check_result = None
    ss.first_checked = False
    if ss.trick_num >= ss.total_tricks:
        ss.screen = "end"
    else:
        _deal_next_trick()


def restart():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


# ---------------------------------------------------------------------------
# Screens
# ---------------------------------------------------------------------------

def start_screen():
    st.title(persona.WELCOME_HEADER)
    st.markdown(persona.WELCOME)

    st.radio(
        persona.CARD_COUNT_LABEL,
        game.CARD_COUNTS,
        index=0,
        horizontal=True,
        key="opt_card_count",
    )
    st.caption(persona.CARD_COUNT_CAPTION)

    st.radio(
        persona.DIFFICULTY_LABEL,
        list(game.DIFFICULTIES.keys()),
        index=0,
        horizontal=True,
        key="opt_difficulty",
        captions=persona.DIFFICULTY_CAPTIONS,
    )

    st.button(persona.START_BUTTON, key="start_btn", type="primary", on_click=start_game)


def game_screen():
    ss = st.session_state
    duration = game.DIFFICULTIES[ss.difficulty]["duration"]

    # Flash timer: rerun-based countdown, flip to marking when time is up.
    if ss.phase == "flash":
        if time.time() - ss.flash_start >= duration:
            ss.phase = "mark"
        else:
            st_autorefresh(interval=250, key=f"flash_tick_{ss.trick_num}")

    st.caption(
        f"Trick {ss.trick_num + 1} of {ss.total_tricks} · {ss.difficulty} · "
        f"{ss.card_count} cards per suit"
    )

    left, right = st.columns(2, gap="large")

    with left:
        if ss.phase == "flash":
            remaining = max(0.0, duration - (time.time() - ss.flash_start))
            st.subheader(persona.FLASH_HEADER)
            st.markdown(f"⏱ **{math.ceil(remaining)}s** — {persona.FLASH_HINT}")
            ui.render_flash(ss.tricks, ss.difficulty)
        else:
            # Deliberately blank: no cards visible while marking.
            st.empty()

    with right:
        marking_panel()


def marking_panel():
    ss = st.session_state
    correct = {card for trick in ss.tricks for card in trick}
    n_expected = game.TRICK_SIZE * (ss.trick_num + 1)
    is_last = ss.trick_num + 1 >= ss.total_tricks

    locked = ss.phase == "flash"
    settled = ss.check_result in ("correct", "revealed")
    # While the wrong-answer warning is up, the board locks: the player must
    # explicitly pick "Try again" (re-enables editing) or "Give me the answer".
    awaiting_choice = ss.check_result == "wrong"

    st.subheader(persona.MARK_HEADER)
    if locked:
        st.caption(persona.GRID_LOCKED_HINT)
    elif ss.first_checked and ss.check_result is None:
        st.caption(persona.TRY_AGAIN_HINT)
    else:
        st.caption(persona.MARK_HINT)

    reveal_map = None
    if ss.check_result == "revealed":
        reveal_map = {}
        for card in ss.marked | correct:
            if card in ss.marked and card in correct:
                reveal_map[card] = "hit"
            elif card in ss.marked:
                reveal_map[card] = "wrong"
            else:
                reveal_map[card] = "missed"

    ui.render_grid(
        ss.card_count,
        ss.marked,
        disabled=locked or settled or awaiting_choice,
        reveal_map=reveal_map,
        toggle_cb=toggle_card,
    )

    n_marked = len(ss.marked)
    if not locked and not settled and not awaiting_choice and n_marked != n_expected:
        missing = n_expected - n_marked
        if missing > 0:
            st.write(f"Marked **{n_marked} of {n_expected}** — mark {missing} more to unlock Check.")
        else:
            st.write(f"Marked **{n_marked} of {n_expected}** — unmark {-missing} to unlock Check.")
    else:
        st.write(f"Marked **{n_marked} of {n_expected}**")
    st.button(
        persona.CHECK_BUTTON,
        key="check_btn",
        type="primary",
        disabled=locked or settled or awaiting_choice or n_marked != n_expected,
        help=persona.CHECK_HELP,
        on_click=do_check,
    )

    if ss.check_result == "correct":
        st.success(persona.CORRECT_MSG)
        st.button(
            persona.FINISH_BUTTON if is_last else persona.NEXT_TRICK_BUTTON,
            key="next_btn",
            on_click=next_trick,
        )
    elif ss.check_result == "wrong":
        st.warning(persona.WRONG_MSG)
        col_a, col_b = st.columns(2)
        col_a.button(persona.TRY_AGAIN_BUTTON, key="try_again_btn", on_click=try_again)
        col_b.button(persona.REVEAL_BUTTON, key="reveal_btn", on_click=reveal_answer)
    elif ss.check_result == "revealed":
        st.info(persona.REVEAL_MSG)
        st.button(
            persona.FINISH_BUTTON if is_last else persona.NEXT_TRICK_BUTTON,
            key="next_btn",
            on_click=next_trick,
        )


def end_screen():
    ss = st.session_state
    st.title(persona.END_HEADER)

    total = sum(ss.scores)
    total_str = f"{total:g}"
    st.markdown(f"### Final score: **{total_str} / {ss.total_tricks}**")

    pretty = {1.0: "1", 0.5: "½", 0.0: "0"}
    st.caption("Trick by trick: " + " · ".join(pretty[s] for s in ss.scores))

    st.markdown(persona.closing_note(ss.scores))
    st.button(persona.PLAY_AGAIN_BUTTON, key="play_again_btn", type="primary", on_click=restart)


# ---------------------------------------------------------------------------

def main():
    st.session_state.setdefault("screen", "start")
    screen = st.session_state.screen
    if screen == "start":
        start_screen()
    elif screen == "game":
        game_screen()
    else:
        end_screen()


main()
