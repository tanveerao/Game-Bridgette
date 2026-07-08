# 🃏 Bridgette

**Status:** Work in progress / MVP

Bridgette is a self-paced practice tool for new-to-intermediate bridge players who
want to sharpen one core skill: **tracking which cards have already been played**.
No bidding, no scoring tables, no opponents — just you, a snarky-but-kind virtual
bridge mentor, and a growing pile of cards you'd better remember.

## How it works

The game loops between two phases until all tricks are played:

1. **Trick playing** — four new cards (a "trick") are flashed on the left side of
   the screen for a few seconds, then hidden.
2. **Card marking** — on the right side, you mark **every card you've seen so far
   this game** on a board of buttons (4 cards after trick 1, 8 after trick 2, …)
   and hit **Check**. Get it right and the next trick is dealt.

### Setup choices

- **Cards per suit** (6, 8, 10, 12, or 13): sets the deck (that many of the lowest
  ranks — A, 2, 3, … — in each suit), the number of tricks (equal to the card
  count), and the size of the marking board.
- **Difficulty**:

  | Difficulty | Flash duration | Visible during the flash |
  |------------|----------------|--------------------------|
  | Easy       | 7 seconds      | Current trick + all prior tricks |
  | Medium     | 5 seconds      | Current trick + previous trick |
  | Hard       | 3 seconds      | Current trick only |

### Scoring

Your **first** Check of each round is scored on accuracy of the cards you marked:

- **1 point** — every marked card was actually played
- **½ point** — at least half of your marked cards were actually played
- **0 points** — fewer than half were

If you miss, you can **Try again** (your marks stay put for editing) or ask
Bridgette to **Give me the answer** — the board color-codes green (correctly
marked), red (marked but never played), and yellow (played but missed). Retries
don't change the round's score.

### Dealing logic

Each trick prefers a single random suit (never the same suit twice in a row)
while that suit still has 4+ cards. As suits run dry, tricks naturally start
mixing suits — the depletion itself creates the difficulty curve. No card ever
repeats within a game.

## Setup & run

Requires Python 3.10+.

```bash
git clone https://github.com/tanveerao/Game-Bridgette.git
cd Game-Bridgette
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

## Project structure

```
Game-Bridgette/
├── app.py                  # Streamlit entry point: screens, session state, phase loop
├── bridgette/
│   ├── game.py             # Pure game logic: deck, trick dealing, scoring
│   ├── persona.py          # All of Bridgette's user-facing copy
│   └── ui.py               # Rendering helpers: card chips, marking grid, CSS
├── requirements.txt
└── README.md
```

## Future features (for consideration only — not in this build)

- Adaptive timing based on right/wrong answers
- Cross-session progression / persistence
- Coaching tips triggered by failure patterns
- Trick-winner memory tracking
- Real card graphics instead of Unicode suit symbols
