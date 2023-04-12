# Generate sample data set to 

# Create x number of random registrants to test data with.

from num2words import num2words
import random
from constants import STAR_WARS_CHARACTERS, TOP_PROGRAMMING_LANGUAGES, FAMOUS_STAR_WARS_SYSTEMS
from registration import add_registrant
import streamlit as st


# TEST_EMAIL = "test@test.com"
TEST_CALL_SIGN_PREFIX = "Grey"
# TEST_DEVELOPERS = 12

def generate_random_number_str(num)-> str:
    return num2words(num, to="cardinal").title()

def generate_random_call_sign(idx) -> str:
    """Generate a random call sign"""
    return f"{TEST_CALL_SIGN_PREFIX} {generate_random_number_str(idx+1)}"
    
def generate_random_skills(max) -> list[str]:
    """Generate a random skill set"""

    num_skills = random.randint(1, max)

    # If wanting to use full programming lanugage list
    # languages = programming_languages_list()
    # random_skills = random.sample(languages, num_skills)
    # return random_skills

    random_skills = random.sample(TOP_PROGRAMMING_LANGUAGES, num_skills)
    return random_skills

def generate_random_friends(max) -> list[str]:
    """Generate a random skill set"""
    num_friends = random.randint(1, max)
    random_friends = random.sample(STAR_WARS_CHARACTERS, num_friends)
    result = [friend["name"] for friend in random_friends]
    return result

def generate_random_home_system() -> str:
    """Generate a random home system"""
    random_system = random.choice(FAMOUS_STAR_WARS_SYSTEMS)
    return random_system

def generate_random_test_developers(
        max_devs: int = 12,
        max_skills: int = 5,
        max_friends: int = 5
    ) -> list[dict]:
    """Generate a random set of developers"""
    developers = []
    for idx in range(max_devs):
        call_sign = generate_random_call_sign(idx)
        skills = generate_random_skills(max_skills)
        friends = generate_random_friends(max_friends)
        home_system = generate_random_home_system()
        developer = {
            "call_sign": call_sign,
            "email": f"{idx}@test.com",
            "skills": skills,
            "friends": friends,
            "home_system": home_system
        }
        developers.append(developer)
    return developers

def generate_devs() -> list[dict]:
    """Generate a random set of developers"""
    devs = generate_random_test_developers(
        max_devs=st.session_state["dev_count"],
        max_skills=st.session_state["max_skills"],
        max_friends=max_friends
    )
    st.session_state['devs'] = devs

def register_devs():
    if st.session_state.get('devs'):
        st.info("Registering devs...")
        devs = st.session_state['devs']
        for dev in devs:
            add_registrant(
                event="Rebel Developer Registration Test",
                call_sign=dev['call_sign'],
                email=dev['email'],
                skills=dev['skills'],
                friends=dev['friends'],
                home_system=dev['home_system']
            )
        # TODO: Actual verification
        st.success("Devs registered")
    else:
        st.error("No devs to register")

@st.cache_data
def devs_file():
    import csv
    from io import StringIO 

    if st.session_state.get('devs'):
        devs = st.session_state['devs']
        if not devs:
            print(f'No devs to write to file')
            return None
        print(f'Writing {len(devs)} devs to file')
        data = StringIO()
        writer = csv.DictWriter(data, fieldnames=["call_sign", "email", "skills", "friends", "home_system"])
        writer.writeheader()
        for row in devs:
            writer.writerow(row)
        return data.getValue()
    else:
        print(f'No devs in session state to write to file')
        return None
    
# Streamlit UI
# For interactive running instead
st.title("Rebel Developer Registration Test System")

dev_count = st.slider("Number of Developers", 1, 100, 12)
max_skills = st.slider("Max Skills per Developer", 1, 20, 5)
max_friends = st.slider("Max Associatese per Developer", 1, 20, 5)

st.session_state["dev_count"] = dev_count
st.session_state["max_skills"] = max_skills
st.session_state["max_friends"] = max_friends

c1, c2, c3 = st.columns(3)
with c1:
    st.button("Generate Test Data", on_click=generate_devs)
with c2:
    st.button("Upload Test Data", on_click=register_devs)
with c3:
    file = devs_file()
    if file:
        st.download_button(label="Download .csv", data=file, file_name=f"rebel_devs.csv", mime="application/zip")

if st.session_state.get('devs'):
    devs = st.session_state['devs']
    st.json(devs)


# Main for direct script running
# if __name__ == '__main__':
#     devs = generate_random_test_developers(
#         max_devs=TEST_DEVELOPERS,
#         max_skills=3,
#         max_friends=2
#     )
#     print(f'devs: {devs}')
#     for dev in devs:
#         add_registrant(
#             event="Rebel Developer Registration Test System",
#             call_sign=dev["call_sign"],
#             email=dev["email"],
#             skills=dev["skills"],
#             friends=dev["friends"],
#             home_system=dev["home_system"],
#             auto_create=True
#         )
    
