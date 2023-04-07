# Generate sample data set to 

# Create x number of random registrants to test data with.

from num2words import num2words
import random
from constants import STAR_WARS_CHARACTERS, STAR_WARS_SYSTEMS
from registration import programming_languages_list, add_registrant

TEST_EMAIL = "test@test.com"
TEST_CALL_SIGN_PREFIX = "Grey"
TEST_DEVELOPERS = 12

def generate_random_number_str(num)-> str:
    return num2words(num, to="cardinal").title()

def generate_random_call_sign(idx) -> str:
    """Generate a random call sign"""
    return f"{TEST_CALL_SIGN_PREFIX} {generate_random_number_str(idx+1)}"

def generate_random_skills(max) -> list[str]:
    """Generate a random skill set"""
    num_skills = random.randint(1, max)
    languages = programming_languages_list()
    random_skills = random.sample(languages, num_skills)
    return random_skills

def generate_random_friends(max) -> list[str]:
    """Generate a random skill set"""
    num_friends = random.randint(1, max)
    random_friends = random.sample(STAR_WARS_CHARACTERS, num_friends)
    result = [friend["name"] for friend in random_friends]
    return result

def generate_random_home_system() -> str:
    """Generate a random home system"""
    random_system = random.choice(STAR_WARS_SYSTEMS)
    return random_system["Planet"]

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
            "email": TEST_EMAIL,
            "skills": skills,
            "friends": friends,
            "home_system": home_system
        }
        developers.append(developer)
    return developers

if __name__ == '__main__':
    devs = generate_random_test_developers(
        max_devs=TEST_DEVELOPERS,
        max_skills=3,
        max_friends=2
    )
    print(f'devs: {devs}')
    for dev in devs:
        add_registrant(
            event="Rebel Developer Registration Test System",
            call_sign=dev["call_sign"],
            email=dev["email"],
            skills=dev["skills"],
            friends=dev["friends"],
            home_system=dev["home_system"],
            auto_create=True
        )
    
