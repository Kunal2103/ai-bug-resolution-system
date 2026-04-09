# Bug Report: Crash on Small Inventories

**Description:**
When the system tries to fetch the top three trending items for a user, it crashes if the user's local store has fewer than 3 items in stock.

**Expected vs Actual Behavior:**
- *Expected:* The system should safely return however many items are available (1 or 2), or an empty list if none are available.
- *Actual:* Fatal system crash.

**Steps to Reproduce:**
1. Call `get_top_three_items` from the `demo_app.inventory` module.
2. Pass a list with only 2 items (e.g., `['apple', 'banana']`).