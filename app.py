"""Main Streamlit entry point for the Public Holiday & Cultural Awareness Planner."""


def main():
    """Display the initial application page."""
    try:
        import streamlit as st
    except ImportError:
        print("Streamlit is not installed. Run: pip install -r requirements.txt")
        return

    st.set_page_config(page_title="Public Holiday & Cultural Awareness Planner", page_icon="🌍", layout="wide")
    st.title("🌍 Public Holiday & Cultural Awareness Planner")
    st.write("Explore public holidays, learn about cultural traditions, compare countries, and save holiday guides.")
    st.info("The project starter is ready. Feature modules are being developed by the team and will be connected here.")


if __name__ == "__main__":
    main()
