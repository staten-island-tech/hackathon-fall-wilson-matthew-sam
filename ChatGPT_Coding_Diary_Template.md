
# ChatGPT Coding Diary

## Project Name: _A Dance of Fire and Ice_

### Date: _11/21/24_

---

## 1. **Task/Problem Description**

I am currently working on creating a game on python pygame where the mechanics are inspired by the real A Dance of Fire and Ice game.

---

## 2. **Initial Approach/Code**

My intial approach were to make a rhythm game where the player has to press space bar at the correct timing to proceed and the beats are song based.

---

## 3. **Interaction with ChatGPT**

### Questions/Requests to ChatGPT

How do I create an ball orbiting another stationary ball in python?

---

## 4. **ChatGPT's Suggestions/Code Changes**

To create a ball orbiting another stationary ball in Python using the pygame library, we can use basic trigonometry to calculate the position of the orbiting ball. Here's a step-by-step guide on how to create this effect:
Concept
Stationary Ball: A ball that stays in one place.
Orbiting Ball: A ball that moves in a circular path around the stationary ball.
Trigonometry: We use the sin and cos functions to calculate the position of the orbiting ball relative to the center (stationary ball) in a circular orbit.
Steps:
Set up Pygame: Initialize the Pygame library and set up the screen and other basic configurations.
Create the Stationary Ball: Draw the stationary ball at a fixed position.
Orbit Calculation: Use math.cos() and math.sin() to calculate the position of the orbiting ball over time.
Update the Position: Continuously update the orbiting ball’s position based on the time passed (this creates smooth movement).
Draw Both Balls: Continuously update the display.

---

## 5. **Reflection on Changes**

ChatGPT utlized more efficient codes and algorithm which reduced my original code by a few lines.

---

## 6. **Testing and Results**

After changing my code according to ChatGPT's suggestions, I found bugs where the player was able to spam for the win.

- Did you run any tests (e.g., unit tests, edge cases)?
- Did the code work as expected after incorporating ChatGPT's changes?

```python
# Example: Testing the updated sorting function
numbers = [5, 2, 9, 1]
print(optimized_sort(numbers))  # Expected output: [1, 2, 5, 9]
```

- Did you encounter any bugs or issues during testing?
Yes, there were bugs where the player was able to spam in order to gain scores
---

## 7. **What Did You Learn?**

In this section, reflect on what you learned from this coding session. Did you gain any new insights, or were there areas you still struggled with? 

Example:
> I learned how to implement an efficient sorting algorithm, and I now understand the time complexity differences between various sorting methods.

---