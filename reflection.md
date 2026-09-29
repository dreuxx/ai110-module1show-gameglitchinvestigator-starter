# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it displayed a number guessing interface with a developer panel that revealed the secret number. The hint direction was backwards: a guess above the secret told me to go higher, and a guess below the secret told me to go lower. I also found that some guesses were compared as text instead of numbers, which could produce the wrong result, and starting a new game did not fully reset the previous game state.

Concrete bugs I noticed:

- With a secret of 50 and a guess of 60, I expected a "Too High" result with a "Go LOWER" hint, but the game displayed "Go HIGHER!".
- With a secret of 50 and a guess of 40, I expected a "Too Low" result with a "Go HIGHER" hint, but the game displayed "Go LOWER!".
- On an even-numbered attempt, a guess of 9 with a secret of 50 could be compared as the strings "9" and "50", causing the game to report "Too High" instead of "Too Low".
- After winning, clicking "New Game" was expected to start a fresh playable round, but the previous won status remained and the game continued to say that I had already won.

**Bug Reproduction Log**

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
|------------|-------------------|-----------------|------------------------|
| Secret 50, guess 60 | Show a "Too High" result and tell the player to go lower. | The result was "Too High", but the hint said "Go HIGHER!". | none |
| Secret 50, guess 40 | Show a "Too Low" result and tell the player to go higher. | The result was "Too Low", but the hint said "Go LOWER!". | none |
| Secret 50, guess 9 on an even-numbered attempt | Compare both values numerically and show "Too Low". | The values could be compared as strings, so the game showed "Too High". | none |
| Win the game, then click "New Game" | Reset the status, score, attempts, history, and secret for a new playable game. | The old won status remained, so the game displayed "You already won. Start a new game to play again.". | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

I decided that the first logic error was fixed when `check_guess` stopped raising `NotImplementedError` and returned the expected result for equal, higher, and lower guesses. I ran `python3 -m pytest tests/test_game_logic.py`, and all three tests passed. The test run confirmed the implementation in `logic_utils.py`, but the remaining Streamlit state and hint bugs still need separate fixes and tests.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
