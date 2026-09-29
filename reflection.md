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
| New Game, then correct guess immediately | Reset attempts to 0 and award 100 points for the first valid guess. | The previous formula awarded 80 points even after the new game reset. | none |
| Easy difficulty, guess 21 | Reject the guess because Easy allows only 1 through 20, without consuming an attempt. | The out-of-range guess was accepted for comparison. | none |
| Enter 40, then click "New Game" | Start with an empty guess field in the new game. | The previous guess remained in the input field. | none |
| Three incorrect guesses | End the game with a game-over message after attempt 3. | The old difficulty limits allowed more than three attempts. | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

I decided that the first logic error was fixed when `check_guess` stopped raising `NotImplementedError` and returned the expected result for equal, higher, and lower guesses. I ran `python3 -m pytest tests/test_game_logic.py`, and all three tests passed. I then corrected the reversed hint messages in `app.py` and used Streamlit's app test runner with a secret of 50 and guesses of 60 and 40; both hints were correct, and the full test suite still reported 3 passed. Finally, I removed the conversion of the secret to text on even attempts and verified that a guess of 9 against 50 showed `Go HIGHER!` while all 3 tests continued to pass. I also fixed `New Game` so a won game resets its status, score, attempts, history, and secret; a Streamlit test confirmed the new game was playable and all 3 tests still passed. I corrected the range text too, verifying that Easy displays `1 and 20`; the full test suite still reported 3 passed. When changing from Normal to Easy, the app now resets the state and generates a secret between 1 and 20; that transition test also passed with all 3 tests. Finally, I changed the initial attempt count to zero and verified that a new Normal game shows 8 attempts left; all 3 tests still passed. I updated input validation so `9.8` is rejected instead of silently truncated to 9, while integer input still works; the full test suite remained at 3 passed. I fixed the score calculation so the first-attempt win gives 80 points and each later attempt reduces the win reward by 20 points; direct logic checks and Streamlit tests for 80, 60, and 40 passed, with the full suite still at 5 passed. I then refactored the shared range, parsing, guessing, and scoring functions into `logic_utils.py`, updated `app.py` to import them, and verified a real Streamlit win plus all 3 tests. The refactor keeps the tested behavior in one place instead of maintaining duplicate implementations. Finally, I moved attempt counting after validation so `abc` does not consume an attempt while a valid guess does; the focused Streamlit check and all 3 tests passed. I added reusable range validation so a guess of 21 in Easy is rejected without consuming an attempt, while 20 remains valid; the focused check and all 3 tests passed. I also removed the arbitrary score changes for incorrect guesses, added tests for the 80, 60, and 40 point progression, and confirmed that the full suite now reports 5 passed.

---

The latest fix gives each game a new text-input key, so the previous guess is cleared after `New Game`; the Streamlit check passed. I also expanded the unit tests for difficulty ranges, parsing, and inclusive boundaries, bringing the full suite to 8 passed. The final scoring rule is that `New Game` starts with zero attempts and zero score, a first valid guess awards 100 points, and each later attempt reduces the reward by 20 points. Finally, I set the game-over limit to three incorrect guesses and verified that the third failure changes the status to `lost` and blocks a fourth submission.

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
