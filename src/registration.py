import streamlit as st
from neo4j_driver import execute_query
from constants import STAR_WARS_CHARACTERS
from datetime import datetime
from utils import list_from_csv
from cymple import QueryBuilder

# Functions
@st.cache_data
def programming_languages_list():
    return list_from_csv("https://gist.github.com/jalakoo/1199236143eeb6b85c8146db7ea2d925/raw", "language")

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
    return list_from_csv("https://gist.github.com/jalakoo/780b2f20bbe67ec97583df768f484912/raw", "name")

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

def registrant_exists(
    email:str
):
    query = """
    MATCH (n:Person {email: $email})
    RETURN n
    """
    clear_params = {
        "email" : email,
    }
    records = execute_query(query, clear_params)
    # If any records returned then we have an existing user
    # TODO: Does the query return at least one record with info if no matches?
    return len(records) > 0

def update_registrant(
    event: str,
    call_sign: str,
    email: str,
    skills: list,
    friends: list,
    home_system: str  
):
    # Remove existing relationships to topics(skills) and characters(friends)
    #  and add new ones, in case the user has updated their list
    query = """
MATCH (n:Person {email: $email})
OPTIONAL MATCH (n)-[k:KNOWS]-()
OPTIONAL MATCH (n)-[f:FROM]-(s:System)
DELETE k, f
WITH n
MATCH (c:Character) WHERE c.name in $friends
MATCH (s:System) WHERE s.name = $home
MATCH (t:Topic) WHERE t.name in $skills
MERGE (n)-[:KNOWS]->(c)
MERGE (n)-[:KNOWS]->(t)
MERGE (n)-[:FROM]->(s)
SET n.name = $name
RETURN n
    """
    clear_params = {
        "email" : email,
        "event" : event,
        "name" : call_sign,
        "date" : datetime.now().isoformat(),
        "home": home_system,
        "friends" : friends,
        "skills" : skills
    }
    execute_query(query, clear_params)
    # TODO: Check if returned person data matches update info
    #  If not, return false instead
    return True

# Using a single cypher query
def add_registrant(
    event: str,
    call_sign: str,
    email: str,
    skills: list,
    friends: list,
    home_system: str
):
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
MERGE (a:Person {name: $name, email: $email, created_at: datetime($date)})
MERGE (s:System {name: $system})
MERGE (a)-[:ATTENDED {date: datetime($date)}]->(e)
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
    result = execute_query(query, params)

    if result is None:
        return False
    return len(result) > 0