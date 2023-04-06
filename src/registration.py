import streamlit as st
from neo4j_driver import execute_query
from constants import STAR_WARS_CHARACTERS, STAR_WARS_SYSTEMS
from datetime import datetime
from utils import list_from_csv
# Functions
@st.cache_data
def programming_languages_list():
    return list_from_csv("http://gist.githubusercontent.com/jalakoo/1199236143eeb6b85c8146db7ea2d925/raw/0178f18b3ce360017d84790b6bffaf18fd7c15d1/programming_languages.csv", "language")

@st.cache_data
def friends_list():
    friends = STAR_WARS_CHARACTERS
    friend_names = [f['name'] for f in friends]
    return friend_names

@st.cache_data
def systems():
    systems = STAR_WARS_SYSTEMS
    system_names = [s['Planet'] for s in systems]
    return system_names
    # with open('./sw_systesms.csv') as csv_file:
    #     systems = csv_file.reader(csv_file, delimiter=',')
    #     return list(systems)

def add_registrant(
    event: str,
    call_sign: str,
    email: str,
    skills: list,
    friends: list,
    home_system: str
) -> bool:
    print(f'\nadd_registrant: event: {event}, call_sign: {call_sign}, email: {email}, skills: {skills}, friends: {friends}')
    # Purge any pre-existing data

    # Add person
    new_person_query = """
        MERGE (e:Event {name: $event})
        MERGE (a:Person {name: $name, email: $email})
        MERGE (a)-[:ATTENDED {date: $date}]->(e)
        RETURN a
    """
    # TODO: Update with datetime (epoch?)
    new_person_parameters = {
        'event': event,
        'name': call_sign,
        'email': email,
        'date': datetime.now().strftime("%Y-%m-%d")
    }
    # # Run query
    result = execute_query(new_person_query, new_person_parameters)
    print(f'New person result: {result}')

    # Add home system
    # new_system_query = """
    #     MERGE (s:System {name: $system})
    #     """
    # new_system_params = {
    #     'system': home_system
    # }
    # s_result = execute_query(new_system_query, new_system_params)
    # print(f'New system result: {s_result}')

    # Add skills
    for skill in skills:
        # Add skill as topic, if not already present
        # new_skill_query = """
        #     MERGE (s:Topic {name: $skill})
        #     """
        # new_skill_params = {
        #     'skill': skill
        # }
        # s_result = execute_query(new_skill_query, new_skill_params)
        # print(f'New skill result: {s_result}')

        # Connect skills/topics to person
        connect_skill_query = """    
            MATCH (a:Person {email: $email}),(t:Topic {name: $topic})
            MERGE (a)-[r:KNOWS]->(t)
            RETURN a,r,t
        """
        connect_skill_parameters = {
            'email': email,
            'topic': skill
        }
        c_result = execute_query(connect_skill_query, connect_skill_parameters)
        print(f'Connect skill result: {c_result}')

        # Add associates
        for friend in friends:
            # Add friend as person, if not already present
            new_friend_query = """
                MERGE (f:Person {name: $friend})
                """
            new_friend_params = {
                'friend': friend
            }
            f_result = execute_query(new_friend_query, new_friend_params)
            print(f'New friend result: {f_result}')

            # Connect friends to person
            connect_friend_query = """    
                MATCH (a:Person {email: $email}),(f:Person {name: $friend})
                MERGE (a)-[r:KNOWS]->(f)
                RETURN a,r,f
            """
            connect_friend_parameters = {
                'email': email,
                'friend': friend
            }
            c_result = execute_query(connect_friend_query, connect_friend_parameters)
            print(f'Connect friend result: {c_result}')

    # TODO: Error handling
    # TODO: Proper Confirmation
    check_query = """
        MATCH (p:Person {email: $email, name: $name})
        RETURN p
    """
    check_params = {
        'email': email,
        'name': call_sign
    }
    check_result = execute_query(check_query, check_params)
    if len(check_result) > 0:
        return True
    else:
        return False