from demo_app.inventory import get_top_three_items

top_items = get_top_three_items([1, 2])
print(top_items)
try:
    top_items = get_top_three_items([1, 2])
    print(top_items)
except Exception as e:
    print(e)