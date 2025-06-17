import streamlit as st
from langchain_helper import generate_restaurant_name


def main():
    st.title("Resturant Name Generator")

    cuisine =  st.sidebar.selectbox(
        "Select a Cuisine",
        [ "Indian", "Italian", "Chinese", "Mexican", "American"]
    )

    if cuisine:
        result = generate_restaurant_name(cuisine)
        print(result)  # For debugging purposes
        st.header(result['restaurant_name'].strip().strip('"'))
        menu_items = result['menu_items'].strip().strip('"').split(', ')

        for item in menu_items:
            st.write(f"- {item.strip().strip('"').strip('\n')}")

if __name__ == "__main__":
    main()