"""All of Bridgette's user-facing copy lives here.

Bridgette: accomplished bridge player, a bit snarky, always warm and encouraging.
"""

APP_TITLE = "Bridgette"

WELCOME_HEADER = "🃏 Well hello there, I'm Bridgette."

WELCOME = """
I've played more bridge hands than you've had hot dinners, and if there's one
thing I've learned at the table, it's this: new players forget which cards have
been played faster than they forget their partner's birthday.

**So here's my little parlor game.** I'll flash you a trick's worth of cards,
whisk them away, and you tell me exactly what you saw. Round after round, the
pile grows. Simple. Humbling. *Terribly* good for your game — like vegetables,
but with more drama.

Two small decisions before we begin, darling:
"""

CARD_COUNT_LABEL = "How many cards per suit shall we play with?"
CARD_COUNT_CAPTION = (
    "This sets your deck (that many of the lowest cards — A, 2, 3, … — in each suit), "
    "how many tricks you'll play, and how big the marking board gets. "
    "Pick 6 if we've just met. Pick 13 if you have something to prove."
)

DIFFICULTY_LABEL = "And how brave are we feeling today?"
DIFFICULTY_CAPTIONS = [
    "7 seconds to look, and every trick so far stays on the table. Cozy.",
    "5 seconds, and you see the current trick plus the one before it.",
    "3 seconds, current trick only. For show-offs. I respect it.",
]

START_BUTTON = "Start"

FLASH_HEADER = "Eyes on the table, darling 👀"
FLASH_HINT = "Memorize these — they vanish when the timer runs out."
GRID_LOCKED_HINT = "No peeking at the buttons yet. Cards first, clicking later."

MARK_HEADER = "So — what flew by?"
MARK_HINT = "Mark every card you've seen so far this game. Yes, *all* of them — from the very first trick."

CHECK_BUTTON = "Check"
CHECK_HELP = "Mark exactly the right number of cards to unlock this."

CORRECT_MSG = "**Congratulations!** 🎉 Every card accounted for. I may have shed a single, dignified tear."
WRONG_MSG = "Hmm. Not *quite*, dear. Some of those cards are right, and some are… creative. Care to try again, or shall I just show you?"
TRY_AGAIN_BUTTON = "Try again"
TRY_AGAIN_HINT = "Go on then — fix your marks, and hit Check when you're feeling confident."
REVEAL_BUTTON = "Give me the answer"
REVEAL_MSG = (
    "Here's the truth of it: 🟩 green you got right, 🟥 red you imagined, "
    "🟨 yellow slipped past you. It happens to the best of us. Rarely to me, but still."
)

NEXT_TRICK_BUTTON = "Next trick"
FINISH_BUTTON = "See how I did"

END_HEADER = "That's the last trick! 🃏"

END_PERFECT = (
    "A **perfect score**! Either you're a natural or you're counting cards — and in "
    "this house, that's a compliment. You've outgrown this setting, hotshot: fewer "
    "seconds, more cards. Level up. Go on, I'll wait."
)
END_MIXED = (
    "A respectable showing! Some tricks stuck, some slipped away — which is exactly "
    "how memory training is supposed to feel. Keep practicing, darling; the cards "
    "reward the stubborn."
)
END_ROUGH = (
    "Oh, sweetheart. A rough table tonight — it truly happens to everyone, and it "
    "says nothing about the player you're becoming. Be kind to yourself: try an "
    "easier setting, take a breath, and build up from there. I'll keep the tea warm."
)

PLAY_AGAIN_BUTTON = "Deal me in again"


def closing_note(scores):
    """Pick the end-screen note based on per-round scores."""
    if scores and all(s == 1.0 for s in scores):
        return END_PERFECT
    if scores and all(s == 0.0 for s in scores):
        return END_ROUGH
    return END_MIXED
