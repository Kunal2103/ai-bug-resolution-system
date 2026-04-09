# demo_app/inventory.py

def get_top_three_items(item_list: list) -> list:
    """
    Returns the top three items from a dynamically generated list.
    """
    # BUG: If the list has fewer than 3 items, this will crash!
    top_items = [
        item_list[0],
        item_list[1],
        item_list[2]
    ]
    return top_items