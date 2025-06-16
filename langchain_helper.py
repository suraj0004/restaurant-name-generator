from secret import OPENAI_API_KEY

def generate_restaurant_name(cuisine):
    return {
        'restaurant_name': f"{cuisine} Delight",
        'menu_items': 'pasta, pizza, salad'
    }