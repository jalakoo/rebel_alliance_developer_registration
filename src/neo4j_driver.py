from neo4j import GraphDatabase, basic_auth
import streamlit as st
import os
import logging
import sys

host = st.secrets['NEO4J_URI']
user = st.secrets['NEO4J_USER']
password = st.secrets['NEO4J_PASSWORD']

driver = GraphDatabase.driver(host, auth=basic_auth(user, password))

# Uncomment to debug neo4j
# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# logging.getLogger("neo4j").addHandler(handler)
# logging.getLogger("neo4j").setLevel(logging.DEBUG)

def execute_query(query, params={}):
    print(f'host: {host}, user: {user}, password: {password}')
    # Using experimental API
    with GraphDatabase.driver(host, auth=basic_auth(user, password)) as driver:
        records, summary, keys = driver.execute_query(query, params)
        logging.info(f"keys: {keys}, summary: {summary}, records: {records}")
        return records

