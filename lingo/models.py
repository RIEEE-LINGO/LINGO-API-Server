from datetime import datetime
from config import db, ma
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(
        String(50)
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(50)
    )
    email: Mapped[str] = mapped_column(
        String(50), unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
    team_roles = relationship(
        "TeamMember",
        backref="user",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )
    owned_projects = relationship(
        "Project",
        backref="owner",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )


class Project(db.Model):
    __tablename__ = "project"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_name: Mapped[str] = mapped_column(
        String(50), unique=True
    )
    project_owner: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
    teams = relationship(
        "Team",
        backref="project",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="Team.team_name"
    )
    words = relationship(
        "Word",
        backref="project",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="Word.word"
    )


class Team(db.Model):
    __tablename__ = "team"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(db.ForeignKey("project.id"))
    team_name: Mapped[str] = mapped_column(
        String(50)
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
    team_members = relationship(
        "TeamMember",
        backref="team",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="TeamMember.email"
    )


class TeamMember(db.Model):
    __tablename__ = "team_member"
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(db.ForeignKey("team.id"))
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    email: Mapped[str] = mapped_column(
        String(50)
    )
    is_owner: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Word(db.Model):
    __tablename__ = "word"
    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(
        String(50)
    )
    project_id: Mapped[int] = mapped_column(db.ForeignKey("project.id"))
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
    meanings = relationship(
        "Meaning",
        backref="word",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="Meaning.created_at"
    )
    reflections = relationship(
        "Reflection",
        backref="word",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="Reflection.created_at"
    )


class Meaning(db.Model):
    __tablename__ = "meaning"
    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(db.ForeignKey("word.id"))
    meaning: Mapped[str] = mapped_column(
        String(1000)
    )
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Reflection(db.Model):
    __tablename__ = "reflection"
    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(db.ForeignKey("word.id"))
    reflection: Mapped[str] = mapped_column(
        String(1000)
    )
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
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

