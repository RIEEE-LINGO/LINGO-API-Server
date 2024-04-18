from lingo.models import User, Word, Project, Team, TeamMember, Meaning, Reflection
from datetime import datetime


def get_timestamp():
    return datetime.utcnow


USERS = [
    {
        "first_name": "Mark",
        "last_name": "Hills",
        "email": "hillsma@appstate.edu",
    },
    {
        "first_name": "Elle",
        "last_name": "Russell",
        "email": "russellem@appstate.edu",
    },
    {
        "first_name": "Kim",
        "last_name": "Bourne",
        "email": "bournekd@appstate.edu",
    }
]

PROJECTS = [
    {
        "name": "Prototype Project"
    }
]

TEAMS = [
    {
        "name": "Prototype Team"
    }
]

TEAM_MEMBERS = [
    {
        "id": 1,
        "email": "hillsma@appstate.edu"
    },
    {
        "id": 2,
        "email": "russellem@appstate.edu"
    },
    {
        "id": 3,
        "email": "bournekd@appstate.edu",
    }
]

WORDS = [
    {
        "word": "co-creation of knowledge",
        "meanings": [
            "working together with those outside my area of expertise, those who offer a different perspective, those outside of academia (stakeholders) to create knowledge",
            "a reciprocal relationship between two objects",
            "collaboration",
            "The generation of understanding or new ideas that results from multiple equal contributions ",
            "Knowledge produced through collaboration efforts",
            "uncovering new things with others, especially with those who might be impacted by the thing",
            "The idea that stakeholders and researchers work together to create new knowledge",
        ],
        "reflections": [
            "does not necessarily imply \"need\"",
        ],
    },
    {
        "word": "Co-production",
        "meanings": [
            "Build in cooperation.",
            "Often times in public administration spheres, we use co-production specifically to describe programs that require community participation to be successful. The city may come around and pick up your recycling (and thus the government is providing a service), but co-production (separating your recyclables from your trash) is necessary to make that service effective or successful.",
            "Co-production can look like conducting research and collaborating on reports with members outside an academic institution. For example, we collaborate with environmental monitoring organizations to ensure that our research is relevant to their management questions. ",

        ],
        "reflections": [
            "The definition from Ostrom seems much more helpful than the vaguer, more theoretical approach used in STS fields. It's not clear to me if the two concepts are related.",
            "I have heard convergence referred to as \"an emergent property\" as a way to distinguish it from effectively \"problem-oriented interdisciplinarity.\" I'm not sure what is meant by an \"emergent property\"",
        ],
    },
    {
        "word": "Convergence",
        "meanings": [
            "I understand convergence to mean 1) research driven by a specific problem and 2) that is highly interdisciplinary.",
            "Ability to bring different fields/knowledges together.",
            "Joining of some group/idea to reach a common goal",
            "Bringing expertise from different disciplines together to ask new questions and draw on different kinds of data, which would not be possible if working in only one discipline.",
            "The STEPS definition for convergence, from Roco 2020,  is that Convergence is a problem-solving strategy to holistically understand, create, and transform a system for reaching a common goal.",
        ],
        "reflections": [],
    },
    {
        "word": "Data",
        "meanings": [
            "Input or output info",
            "Pieces of information - numbers, texts, measurements, survey responses, that can be used in research",
            "Something that becomes useful after analysis; not information†",
            "Useful things",
            "Information",
            "Information of any kind : numbers, pictures, videos, etc",
            "Numbers and letters",
            "Structured information",
            "Information created by measurements",
            "Information about anything",
            "Information collected for a purpose, including statistics and context",
            "Things you gather or collect",
            "Information represented in a numerical form ",
            "Symbolic information",
            "Organized information",
            "Information required to solve a problem",
            "knowledge",
            "Something that becomes useful after analysis; not information",
            "ay information collected and analyzed for research",
            "The information used to aide reasoning or calculation ",
            "information that can be systematically coded to investigate patterns",
        ],
        "reflections": [
            "Useless without stakeholders",
            "Experimental or theoretical?",
        ],
    },
    {
        "word": "data twinning",
        "meanings": [],
        "reflections": [],
    },
    {
        "word": "digital twinning",
        "meanings": [],
        "reflections": [],
    },
    {
        "word": "epistemic humility",
        "meanings": [
            "Being humble with knowledge",
            "i might always be wrong",
            "core value for STEPS, understanding that I do not know everything and am respectful of other disciplines and defer to experts in other fields",
            "recognition of what you do and do not know",
            "a state of knowing and interacting in a way that acknowledges that your discipline or perspective is one of many ways of knowing",
            "To me, it means that I recognize that I don't know everything, and my way of knowing isn't the best or only way",
            "the ability to avoid intellectually trespassing ",
            "humility when it comes to knowledge, knowing and/or ways of knowing",
            "Being capable of admitting you cannot/do not know it all and have much to learn from others",
            "I am not perceived to know everything",
            "Being aware that even when you feel completely confident that you're right, you could still be wrong.",
            "knowing that being an expert in something does not mean being an expert in all things",
            "In the context of knowledge, questioning my own assumptions and being open to the perspectives of others",
            "teaching kindly",
        ],
        "reflections": [
            "It shouldn't be used as a reason to discredit someone else's knowledge - i.e. epistemic humility for thee but not for me",
            "it makes me think of systematic humility, or how epistemic humility should be systematic",
        ],
    },
    {
        "word": "extension",
        "meanings": [
            "for people with a close knowledge of agricultural extension programs, the word \"extension\" carries a great deal of meaning that seems to be assumed. I heard someone say \"this is rooted in extension methods\" and realized there is an entire body of literature and knowledge, not just a type of activity or job descriptions. ",
            "Cooperative Extension System (CES) empowers farmers, ranchers, and communities of all sizes to meet the challenges they face, adapt to changing technology, improve nutrition and food safety, prepare for and respond to emergencies, and protect our environment. ",
        ],
        "reflections": [],
    },
    {
        "word": "farmer",
        "meanings": [
            "Someone who is responsible for growing food, fiber, fuel, or other natural products consumed or used by people or animals",
            "I tend to think of the word \"farmer\" to refer specifically to a group of people who are directly involved in agricultural production. I distinguish farmer from farmworker to indicate variation in labor relations, and also recognize that \"farmer\" can be a cultural category that is associated with rurality. Corporations (e.g. Cargill, Tyson, Perdue) are not farmers, but landowners who hire farmworkers can be farmers. I associate the term \"farmer\" with someone for whom agriculture is a major occupation, but in reality I know that is often not the case, many people who identify as farmers also engage in off-farm work, and many people who work on farms might not call themselves farmers. The meaning of this term also varies widely depending on geographic location.",
            "Farmers are individuals who produce food, including vegetables, grains, and meat. Emphasis on \"individual.\"",
            "agricultural steward",
        ],
        "reflections": [
            "Many seem to think that because we have \"industrial agriculture,\" that means that farmers are part of some top-down corporate structure, and that's just not so.",
        ],
    },
]


def create_users(db):
    users = []

    for data in USERS:
        new_user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email")
        )
        db.session.add(new_user)
        users.append(new_user)

    db.session.commit()
    return users


def create_projects(db):
    projects = []

    # NOTE: We need to update this to use the actual IDs
    # This is fragile to changes in IDs assigned by the db.
    for data in PROJECTS:
        new_project = Project(
            project_name=data.get("name"),
            project_owner=1,
            is_active=True
        )
        db.session.add(new_project)
        projects.append(new_project)

    db.session.commit()
    return projects


def create_teams(db):
    teams = []

    for data in TEAMS:
        new_team = Team(
            project_id=1,
            team_name=data.get("name"),
            is_active=True
        )
        db.session.add(new_team)
        teams.append(new_team)

    for data in TEAM_MEMBERS:
        new_member = TeamMember(
            team_id=1,
            user_id=data.get("id"),
            email=data.get("email"),
            is_owner=True
        )
        db.session.add(new_member)

    db.session.commit()
    return teams


def create_words(db, project_id):
    words = []

    for data in WORDS:
        new_word = Word(
            word=data.get("word"),
            project_id=project_id
        )
        db.session.add(new_word)
        db.session.commit()  # Needed so we have an ID for the word
        words.append(new_word)

        for meaning_data in data.get("meanings"):
            new_meaning = Meaning(
                meaning=meaning_data,
                word_id=new_word.id,
            )
            db.session.add(new_meaning)

        for reflection_data in data.get("reflections"):
            new_reflection = Reflection(
                reflection=reflection_data,
                word_id=new_word.id,
            )
            db.session.add(new_reflection)

        db.session.commit()

    return words
