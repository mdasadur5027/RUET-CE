import streamlit as st

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Navigation function
def navigate_to(page_name):
    st.session_state.page = page_name

# Sidebar for navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Go to Home"):
    navigate_to('Home')
if st.sidebar.button("Go to About"):
    navigate_to('About')
if st.sidebar.button("Go to Contact"):
    navigate_to('Contact')

# Main content rendering based on the selected page
if st.session_state.page == 'Home':
    st.title("Welcome to the Home Page")
    st.write("This is the main page of your Streamlit app.")

elif st.session_state.page == 'About':
    st.title("About Page")
    st.write("This page provides information about the app.")

elif st.session_state.page == 'Contact':
    st.title("Contact Page")
    st.write("Feel free to reach out to us!")
