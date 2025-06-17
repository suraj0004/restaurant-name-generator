from secret import OPENAI_API_KEY

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain


llm = OpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    api_key=OPENAI_API_KEY,
)

def generate_restaurant_name(cuisine):
    # Chain 1: Resturant Name
    prompt_templage_name = PromptTemplate(
        input_variables=['cuisine'],
        template="Generate a creative restaurant name for a {cuisine} restaurant. Return only one name.",
    )

    name_chain = LLMChain(
        llm=llm,
        prompt=prompt_templage_name,
        output_key='restaurant_name'
    )

    # Chain 2: Menu Items
    prompt_template_menu_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="List five popular menu items for a restaurant named {restaurant_name}, Return a comma-separated list.",
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

    return response

if __name__ == "__main__":
    result = generate_restaurant_name("Indian")
    print(result)