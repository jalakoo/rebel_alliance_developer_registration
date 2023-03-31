import streamlit as st
from neo4j_driver import execute_query
from constants import PROGRAMMING_LANGUAGES, STAR_WARS_CHARACTERS
import json

# Functions
@st.cache_data
def programming_languages_list():
    return list(PROGRAMMING_LANGUAGES.keys())

# @st.cache_data
# def load_friends(filepath):
#     # f = open(filepath)
#     # return json.loads(f)
#     with open(filepath, 'r') as f:
#         return json.load(f)

@st.cache_data
def friends_list():
    friends = STAR_WARS_CHARACTERS
    friend_names = [f['name'] for f in friends]
    return friend_names

# UI
# Convulted way to center image
col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.write('')
with col2:
    st.image('./media/rebel_logo.png')
with col3:
    st.write('')

st.title('Rebel Alliance Registration System')

with st.form(key='submission_form', clear_on_submit=True):
    name = st.text_input('Call sign')
    # TODO: Verify unique

    skills = st.multiselect("What programming languages do you know?", programming_languages_list())

    friends = st.multiselect("Who are your friends?", friends_list())

    submit = st.form_submit_button('Register')
    if submit:
        # TODO:
        # Write cypher query
        # query = """
        
        # """
        # parameters = {

        # }
        # # Run query
        # result = execute_query(query, parameters)

        st.write('Registration successful!')
