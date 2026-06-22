# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
A: A simple UI that hosted a guessing game with a certain amount of attempts. It has general customization as in difficulty or light mode and it kept track of the history of attempts and score. The concept is very clear and easy to follow.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  A: When you switch between difficulty in the game the range is supposed to differ yet it remains 1-100. The easy mode has LESS attempts than the harder modes. I believe this is highly unintentional as easier modes should have the same if not more attempts for the user.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.
                                              
| Input | Expected Behavior | Actual Behavior | Error
  2     | higher            | lower           | none
  -10   | out of bounds     | lower           | none
  88    | lower             | higher          | none



It is harder to fit my explainations in this format and the terminal didnt throw an error message so i will explain some bugs in written form:

1. The hints are inconsistent with the state of the secret number. What I mean by this is that when I entered 2 with a secret of 100, the hint would tell me to go lower and higher every instance I entered 2 when it should only say higher. This seems to fall into the logical error category.

2. The attempts left is not accurately represented by the code. What I mean by this is that in normal mode for example the number of attempts is stated to be 8 however the game terminates after 6 attempts. I believe this to be either a visual error(actually 6) or logical one(broken code.)

3. There is another bug regarding the new game button. To actually restart the instance of the game you need to reload the webpage otherwise there is no other way. The new game button works before or during the game but after a conclusion is reached it will cease to work. I also believe this is a broken logic error one that doesn't account for the case of the games conclusion. 

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
A: Claude Code of course

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
A: For the flipping-hint bug, Claude correctly traced the cause to app.py, where the secret was being turned into a string with str() on every even attempt. That made check_guess compare an int to a string and fall into a hidden except TypeError block that did string comparison, so something like "9" > "100" came out True. It removed the str() cast so the secret stays an int and deleted the dead except block. I verified it by running pytest (the consistency test and the 9-vs-100 test both pass) and by checking that the same guess no longer flips between higher and lower.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
A: There was a suggestion claude made which was to fully rewrite a certain logic which was not needed whatsoever. After explaining how streamlit works we were able to edit a variable that immediately resolved one of the glitches.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
A: I decided a bug was fixed only when both the tests and the actual game agreed, not just one of them. For the flipping-hint bug I checked that the same guess always returned the same outcome instead of switching between higher and lower, and for the New Game bug I confirmed the game restarted without reloading the page. If pytest passed but the behavior still looked wrong in the app, I treated it as not fixed.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
A: I ran the pytest suite in test_game_logic.py and got 9 passing tests, 3 from the starter and 6 new ones. The most useful one checked that guessing 9 against a secret of 100 returns "Too Low," which proved the hint was no longer doing string comparison. It also showed me that check_guess actually returns a tuple of outcome and message, so the starter tests had to be unpacked before they made sense.

- Did AI help you design or understand any tests? How?
A: Yes, the AI generated the pytest cases that targeted the exact bug I fixed and explained why check_guess returns a tuple instead of a plain string. It actually got one test wrong at first by checking for the word "HIGHER" in a too low message, which failed when I ran it. Seeing that failure taught me that the outcome and the message are separate things and that AI-written tests still have to be run, not just trusted.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
A: 
Every time you interact with a Streamlit app (click, type, slide), the entire Python script reruns from scratch, resetting all regular variables(score, counter, etc). st.session_state is a special dictionary that survives these reruns, letting you persist values like counters or user inputs across interactions. The key habit is initializing session state values with an if "key" not in st.session_state guard so they're only set once, on first load.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects? This could be a testing habit, a prompting strategy, or a way you used Git.
A: Having multiple sessions of AI focus on one specific bug fix to ensure accuracy. I think being able to have AI fully focus on a problem is much more convinient than letting it give poorer results for the sake of one chat convienience. It is definitely a technique I will consider later.

- What is one thing you would do differently next time you work with AI on a coding task?
A: I would have it immediately show me the understanding of code logic BEFORE I start presenting bug findings. Breaking down the logic before hand can have me solve the issues before AI fixes it so that I can understand how to prompt better or code better next time. It is very important for the PERSON using AI to be competent on these issues.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
A: AI is powerful but it is not perfect. Many AI generated codes have hallucinations, errors, things unaccounted for that you must review before production. Luckily you also can use AI to help you review that as long as you've identified the problems. 

