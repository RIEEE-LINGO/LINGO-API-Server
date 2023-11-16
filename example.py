from sqlalchemy import create_engine
from sqlalchemy import MetaData
from lingo.models import Project
from lingo.models import Term
from lingo.models import Reflection
from lingo.models import Base
from sqlalchemy.orm import Session
from datetime import datetime

engine = create_engine("sqlite://", echo=True)

with Session(engine) as session:
    project = Project(name="Project 1", description="Description 1", created=datetime.now, modified=datetime.now)
    term = Term(term="Farmer", created=datetime.now, modified=datetime.now, project_id=project.id)
    project.terms.append(term)
    session.add(project)
    session.commit