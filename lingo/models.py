from datetime import datetime
from config import db, ma

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=True, unique=False)
    last_name = db.Column(db.String, nullable=True, unique=False)
    email = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    team_roles = db.relationship(
        "TeamMember",
        backref="user",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )

class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, nullable=False, unique=True)
    project_owner_email = db.Column(db.String, nullable=False, unique=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    teams = db.relationship(
        "Team",
        backref="project",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="Team.team_name"
    )

class Team(db.Model):
    __tablename__ = "team"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    team_name = db.Column(db.String, nullable=False, unique=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    team_members = db.relationship(
        "TeamMember",
        backref="team",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="TeamMember.email"
    )

class TeamMember(db.Model):
    __tablename__ = "team_member"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    email = db.Column(db.String, nullable=False, unique=False)
    is_owner = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class Word(db.Model):
    __tablename__ = "word"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False, unique=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    meanings = db.relationship(
        "Meaning",
        backref="word",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="Meaning.created_at"
    )
    reflections = db.relationship(
        "Reflection",
        backref="word",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="Reflection.created_at"
    )

class Meaning(db.Model):
    __tablename__ = "meaning"
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey("word.id"))
    meaning = db.Column(db.String, nullable=False, unique=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class Reflection(db.Model):
    __tablename__ = "reflection"
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey("word.id"))
    reflection = db.Column(db.String, unique=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True

class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        load_instance = True
        sqla_session = db.session
        include_relationships = True

class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        load_instance = True
        sqla_session = db.session
        include_relationships = True

class TeamMemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TeamMember
        load_instance = True
        sqla_session = db.session
        include_relationships = True

class WordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Word
        load_instance = True
        sqla_session = db.session
        include_relationships = True

class MeaningSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Meaning
        load_instance = True
        sqla_session = db.session
        include_fk = True

class ReflectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reflection
        load_instance = True
        sqla_session = db.session
        include_fk = True

user_schema = UserSchema()
project_schema = ProjectSchema()
team_schema = TeamSchema()
team_member_schema = TeamMemberSchema()
word_schema = WordSchema()
meaning_schema = MeaningSchema()
reflection_schema = ReflectionSchema()

users_schema = UserSchema(many=True)
projects_schema = ProjectSchema(many=True)
team_schema = TeamSchema(many=True)
team_members_schema = TeamMemberSchema(many=True)
words_schema = WordSchema(many=True)
meanings_schema = MeaningSchema(many=True)
reflections_schema = ReflectionSchema(many=True)

# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import MappedAsDataclass
# from sqlalchemy import ForeignKey
# from sqlalchemy import String
# from sqlalchemy import DateTime
# from typing import List
# from typing import Optional
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from sqlalchemy import func

# # LI8330.o0b229mb

# class Base(DeclarativeBase):
#     pass

# class User(MappedAsDataclass,Base):
#     __tablename__ = "user"

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
    
# class UserProject(MappedAsDataclass,Base):
#     __tablename__ = "user_project_xref"

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
#     project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
#     role: Mapped[int]
    
# class Project(MappedAsDataclass,Base):
#     __tablename__ = "project"

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     name: Mapped[str]
#     description: Mapped[str] = mapped_column(String(5000))
#     terms: Mapped[List["Term"]] = relationship(
#         default_factory=list, 
#         back_populates="project"
#     )
#     created: Mapped[datetime] = mapped_column(
#         insert_default=func.utc_timestamp(), 
#         default=None
#     )
#     modified: Mapped[datetime] = mapped_column(
#         insert_default=func.utc_timestamp(), 
#         default=None
#     )

# class Term(MappedAsDataclass,Base):
#     __tablename__ = "term"

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     term: Mapped[str]
#     project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
#     project: Mapped["Project"] = relationship(
#         back_populates="terms"
#     )
#     reflections: Mapped[List["Reflection"]] = relationship(
#         default_factory=list,
#         back_populates="term"
#     )
#     created: Mapped[datetime] = mapped_column(
#         insert_default=func.utc_timestamp(), default=None
#     )
#     modified: Mapped[datetime] = mapped_column(
#         insert_default=func.utc_timestamp(), default=None
#     )

# class Reflection(MappedAsDataclass,Base):
#     __tablename__ = "term_reflection"

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     reflection: Mapped[str]
#     term_id: Mapped[int] = mapped_column(ForeignKey("term.id"))
#     term: Mapped["Term"] = relationship(
#         back_populates="reflections"
#     )
#     created: Mapped[datetime] = mapped_column(
#         insert_default=func.utc_timestamp(), default=None
#     )
#     modified: Mapped[datetime] = mapped_column(
#         insert_default=func.utc_timestamp(), default=None
#     )

