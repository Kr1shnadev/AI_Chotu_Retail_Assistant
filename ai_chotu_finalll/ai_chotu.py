
import streamlit as st
from main import create_streamlit_interface
from chart import main
from bcode import bcod
# Title of the app
st.title("Multi-Page Streamlit App")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ("Main Page", "Chart Page","bcode Page"))


# Load the selected page
if page == "Main Page":
    create_streamlit_interface()
elif page == "Chart Page":
    main()
elif page == "bcode Page":
    bcod()