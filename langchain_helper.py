from secret import OPENAI_API_KEY

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import re

llm = OpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=OPENAI_API_KEY,
)

def clean_output(response: dict):
    # Clean restaurant name
    restaurant_name = response['restaurant_name'].strip().replace('"', '').replace('\n', '')
    if len(restaurant_name) > 100:
        restaurant_name = restaurant_name[:100]
    response['restaurant_name'] = restaurant_name

    # Clean menu items
    response['menu_items'] = response['menu_items'].strip().replace('"', '').replace('\n', '')

    # Rebuild menu items cleanly
    menu_items = [item.strip().strip('"') for item in response['menu_items'].split(',') if item.strip()]
    response['menu_items'] = ', '.join(menu_items[:5])  # Ensure only 5 items

    return response


def generate_restaurant_name(cuisine):
    # Chain 1: Resturant Name
    prompt_templage_name = PromptTemplate(
        input_variables=['cuisine'],
        template="Generate a single, short, and creative restaurant name for a {cuisine} restaurant. " +
        "The name should be between 2 to 5 words only, not exceed 5 words total. " +
        "Avoid unnecessary punctuation, avoid quotes or newlines, and return only the name — nothing else.",
    )

    name_chain = LLMChain(
        llm=llm,
        prompt=prompt_templage_name,
        output_key='restaurant_name'
    )

    # Chain 2: Menu Items
    prompt_template_menu_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="List exactly five popular menu items for a restaurant named {restaurant_name}. " +
        "Return only the names of the dishes as a comma-separated list. " +
        "Do not return descriptions, markdown, examples, headings, or any extra content. " +
        "End your response right after the last menu item."
    )

    menu_items_chain = LLMChain(
        llm=llm,
        prompt=prompt_template_menu_items,
        output_key='menu_items'
    )

    # Sequential Chain - Combine both chains
    
    chain = SequentialChain(
        chains=[name_chain, menu_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', 'menu_items'],
    )

    response = chain({'cuisine': cuisine})
    print("Before cleaning:", response)

    return clean_output(response)

if __name__ == "__main__":
    result = generate_restaurant_name("Indian")
    print(result)