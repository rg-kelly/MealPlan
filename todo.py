"""
TO DO:
- Ability to delete ingredients from recipe
- On date go, add column for calendar events that would affect meals
- Generate shopping list button on meal plan tab. That would display all ingredients needed (and prices?). Could edit prices/amounts and then generate budget prediction.
- Store extra reminder (True/False and length) info in db instead of hard code in calendar.py
- Verify that calculations are accurate for report (esp. min/max values)
- Alpha order the recipes on the meal plan tab
- Automatically generate meal plan (check calendar for night time events over dinner hour and go off baseline meal plan like as in sheets etc)
  #####
- Add 'add to inventory' check box for enter prices screen, then don't have to enter
  price but just amount and ingredient so that the pantry inventory is accurate
  and another use case is that then items that I want to enter prices for but
  didn't actually buy won't affect the inventory
- When choose main dish, auto select sides based on most common pairing
- Copy from week feature for meal plan. Can copy meal assignments from a previous week to current one...
- Order ingredients list in enter prices tab with most commonly used ones at top (order by most common use then alpha) and then alpha the rest
- Leftovers box to check on meal plan screen for when meal will be using leftover ingredients from something made previous (and won't be counted for grocery bill)
- Ingredient drop down for 'configure ingredients' screen? (Logic for not adding duplicate ingredients because of plurality... maybe use like query to try to catch and then throw a 'did you mean this' window for user to verify...)
- Tab to display inventory for ingredients (basically ingredient info page -- price per unit / last 5 purchase history, inventory, recipes...)
- Lunch and breakfast and snacks capabilities
- Add recipes to 'cookbook' in slides (attribute in recipe table for distinguishing dessert from main from soup...)
- Ability to switch meals from one day to another
- Intelligence to project this week's grocery bill (still need some kind of inventory tracker and place to add misc foods like snacks/bfast)
    - Define own conversions for foods that have mass for purchase_history and volume for recipes (i.e. pb, flour, salsa, bbq sauce, etc.)
"""
