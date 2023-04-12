import streamlit as st
from neo4j_driver import execute_query
from constants import STAR_WARS_CHARACTERS
from datetime import datetime
from utils import list_from_csv
from cymple import QueryBuilder

# Functions
@st.cache_data
def programming_languages_list():
    return list_from_csv("http://gist.githubusercontent.com/jalakoo/1199236143eeb6b85c8146db7ea2d925/raw/0178f18b3ce360017d84790b6bffaf18fd7c15d1/programming_languages.csv", "language")

@st.cache_data
def friends_list():
    friends = STAR_WARS_CHARACTERS
    friend_names = [f['name'] for f in friends]
    return friend_names

# @st.cache_data
# def friends_list():
#     return list_from_csv("https://gist.githubusercontent.com/jalakoo/ae51e1c60d12431154257b69b10ed5a0/raw/da1476950306e432275c530d31c3a54edb919727/star_wars_characters_filtered.csv", "name")


@st.cache_data
def systems():
    return list_from_csv("https://gist.githubusercontent.com/jalakoo/780b2f20bbe67ec97583df768f484912/raw/726aa15c4c3c960003522331c33b52ea7416cfb5/famous_star_wars_systems.csv", "name")

    # From local constants if added
    # systems = STAR_WARS_SYSTEMS
    # system_names = [s['Planet'] for s in systems]
    # return system_names

    # From local csv
    # with open('./sw_systesms.csv') as csv_file:
    #     systems = csv_file.reader(csv_file, delimiter=',')
    #     return list(systems)

def setup_contraints():
    add_constraints_query = """
        CREATE CONSTRAINT ON (n:Person)
        ASSERT n.email IS UNIQUE
    """
    result = execute_query(add_constraints_query)
    return result

# Using Cymple
# def add_registrant_cymple(
#     event: str,
#     call_sign: str,
#     email: str,
#     skills: list,
#     friends: list,
#     home_system: str,
# ):
#     print('not implemented yet')
#     qb = QueryBuilder()
#     query = qb.merge.node(labels="Event", ref_name="e")

# Using a single cypher query
def add_registrant(
    event: str,
    call_sign: str,
    email: str,
    skills: list,
    friends: list,
    home_system: str
):
    print(f'\nadd_registrant: event: {event}, call_sign: {call_sign}, email: {email}, skills: {skills}, friends: {len(friends)}')

    # First clear any pre-existing data
    clear_query = """
    MATCH (n:Person {email: $email})
    DETACH DELETE n
    """
    clear_params = {
        "email" : email
    }
    execute_query(clear_query, clear_params)

    query = """
MERGE (e:Event {name: $event})
MERGE (a:Person {name: $name, email: $email})
MERGE (s:System {name: $system})
MERGE (a)-[:ATTENDED {date: $date}]->(e)
MERGE (a)-[:FROM]->(s)
"""
    for idx, skill in enumerate(skills):
        # query.join(f'MATCH (t{idx}:Topic {{name: "{skill}"}})')
        # query.join(f'MERGE (a)-[r:KNOWS]->(t{idx})')
        query += f'\nMERGE (t{idx}:Topic {{name: "{skill}"}})'
        query += f'\nMERGE (a)-[:KNOWS]->(t{idx})'

    for idx, friend in enumerate(friends):
        # query.join(f'MATCH (f{idx}:Character {{name: "{friend}"}})')
        # query.join(f'MERGE (a)-[r:KNOWS]->(f{idx})')
        query += f'\nMERGE (f{idx}:Character {{name: "{friend}"}})'
        query += f'\nMERGE (a)-[:KNOWS]->(f{idx})'
    query += f'\nRETURN a'
    params = {
        "event" : event,
        "name" : call_sign,
        "email" : email,
        'date': datetime.now().isoformat(),
        "system" : home_system
    }
    print(f'add_registrant query: {query}')
    result = execute_query(query, params)

    if result is None:
        return False
    return len(result) > 0

# Using independent cypher commands
# This is the slowest method
# def add_registrant(
#     event: str,
#     call_sign: str,
#     email: str,
#     skills: list,
#     friends: list,
#     home_system: str,
#     auto_create: bool = False
# ) -> bool:
#     # This function works but is clunky. It should be refactored to use a single query or a bulk import option using APOC
#     # print(f'\nadd_registrant: event: {event}, call_sign: {call_sign}, email: {email}, skills: {skills}, friends: {friends}')
#     # Purge any pre-existing data

#     # Add person
#     query = """
#         MERGE (e:Event {name: $event})
#         MERGE (a:Person {name: $name, email: $email})
#         MERGE (s:System {name: $system})
#         MERGE (a)-[:ATTENDED {date: $date}]->(e)
#         MERGE (a)-[:FROM]->(s)
#         RETURN a
#     """
#     # TODO: Update with datetime (epoch?)
#     parameters = {
#         'event': event,
#         'name': call_sign,
#         'email': email,
#         'date': datetime.now().isoformat(),
#         'system': home_system
#     }
#     # # Run query
#     result = execute_query(query, parameters)
#     # print(f'New person result: {result}')

#     # Add skills
#     for skill in skills:
#         # TODO: Make a single query
#         # Add skill as topic, if not already present
#         if auto_create:
#             new_skill_query = """
#                 MERGE (s:Topic {name: $skill})
#                 """
#             new_skill_params = {
#                 'skill': skill
#             }
#             s_result = execute_query(new_skill_query, new_skill_params)
#             # print(f'New skill result: {s_result}')

#         # Connect skills/topics to person
#         connect_skill_query = """    
#             MATCH (a:Person {email: $email}),(t:Topic {name: $topic})
#             MERGE (a)-[r:KNOWS]->(t)
#             RETURN a,r,t
#         """
#         connect_skill_parameters = {
#             'email': email,
#             'topic': skill
#         }
#         c_result = execute_query(connect_skill_query, connect_skill_parameters)
#         # print(f'Connect skill result: {c_result}')

#         # Add associates
#         for friend in friends:
#             # Add friend as person, if not already present
#             if auto_create:
#                 new_friend_query = """
#                     MERGE (f:Character {name: $friend})
#                     """
#                 new_friend_params = {
#                     'friend': friend
#                 }
#                 f_result = execute_query(new_friend_query, new_friend_params)
#                 # print(f'New friend result: {f_result}')

#             # Connect friends to person
#             connect_friend_query = """    
#                 MATCH (a:Person {email: $email}),(f:Character {name: $friend})
#                 MERGE (a)-[r:KNOWS]->(f)
#                 RETURN a,r,f
#             """
#             connect_friend_parameters = {
#                 'email': email,
#                 'friend': friend
#             }
#             c_result = execute_query(connect_friend_query, connect_friend_parameters)
#             # print(f'Connect friend result: {c_result}')

#     # TODO: Error handling
#     # TODO: Proper Confirmation
#     check_query = """
#         MATCH (p:Person {email: $email, name: $name})
#         RETURN p
#     """
#     check_params = {
#         'email': email,
#         'name': call_sign
#     }
#     check_result = execute_query(check_query, check_params)
#     if len(check_result) > 0:
#         return True
#     else:
#         return False