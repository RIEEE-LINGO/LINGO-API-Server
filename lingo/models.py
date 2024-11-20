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
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
    teams = relationship(
        "TeamMember",
        backref="user",
        cascade="all, delete, delete-orphan",
        single_parent=True
    )

class Team(db.Model):
    __tablename__ = "team"
    id: Mapped[int] = mapped_column(primary_key=True)
    team_name: Mapped[str] = mapped_column(
        String(50), unique=True
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
    words = relationship(
        "Word",
        backref="team",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="Word.word"
    )

class TeamMember(db.Model):
    __tablename__ = "team_member"
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(db.ForeignKey("team.id"))
    user_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    team_owner: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
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
    team_id: Mapped[int] = mapped_column(db.ForeignKey("team.id"))
    is_active: Mapped[bool] = mapped_column(default=True)
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
    is_active: Mapped[bool] = mapped_column(default=True)
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
    is_active: Mapped[bool] = mapped_column(default=True)
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
team_schema = TeamSchema()
team_member_schema = TeamMemberSchema()
word_schema = WordSchema()
meaning_schema = MeaningSchema()
reflection_schema = ReflectionSchema()

users_schema = UserSchema(many=True)
teams_schema = TeamSchema(many=True)
team_members_schema = TeamMemberSchema(many=True)
words_schema = WordSchema(many=True)
meanings_schema = MeaningSchema(many=True)
reflections_schema = ReflectionSchema(many=True)
