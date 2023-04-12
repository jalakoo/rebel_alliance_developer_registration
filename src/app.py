import streamlit as st
import random
from call_signs import FIRST_WORD, SECOND_WORD
from registration import add_registrant, programming_languages_list, friends_list, systems

# Constants
EVENT_NAME = st.secrets['EVENT_NAME']
RANDOM_CALL_SIGN = f"{random.choice(FIRST_WORD)} {random.choice(SECOND_WORD)}"


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

    n1, n2 = st.columns(2)
    with n1:
        # NOTE: Adding randomized call-sign to placeholder DOES NOT WORK. Text input outputs empty
        call_sign = st.text_input('Call sign', placeholder="Red One", help='Unique call sign for the Rebel Alliance')
    with n2:
        email = st.text_input('Email', help='Email address for a unique call sign verfication')

    skills = st.multiselect("What programming languages do you know?", programming_languages_list())

    f1, f2 = st.columns(2)
    with f1:
        friends = st.multiselect("Who do you associate with?", friends_list())
    with f2:
        home = st.selectbox("Where's your homeworld?", systems())

    submit = st.form_submit_button('Register')
    if submit:
        st.info("Registration in progress...")
        success = add_registrant(
            event=EVENT_NAME, 
            call_sign=call_sign, 
            email=email, 
            skills=skills, 
            friends=friends,
            home_system=home)
        if success:
            st.success('Registration successful!')
        else:
            st.error('Registration failed. Please try again.')
