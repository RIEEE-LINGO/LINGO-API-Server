from datetime import datetime, UTC
from config import db, ma
from typing import Optional, List
from sqlalchemy import String, ForeignKey
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
    teams: Mapped[List["TeamMember"]] = relationship()
    current_team_id: Mapped[int] = mapped_column(db.ForeignKey("team.id"))


class Team(db.Model):
    __tablename__ = "team"
    id: Mapped[int] = mapped_column(primary_key=True)
    team_name: Mapped[str] = mapped_column(
        String(50), unique=True
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    is_default: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )
    team_members: Mapped[List["TeamMember"]] = relationship()
    words: Mapped[List["Word"]] = relationship()


class TeamMember(db.Model):
    __tablename__ = "team_member"
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_owner: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )


class Word(db.Model):
    __tablename__ = "word"
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(db.ForeignKey("team.id"))
    word: Mapped[str] = mapped_column(
        String(50)
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )
    meanings: Mapped[List["Meaning"]] = relationship()
    reflections: Mapped[List["Reflection"]] = relationship()


class Meaning(db.Model):
    __tablename__ = "meaning"
    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(db.ForeignKey("word.id"))
    meaning: Mapped[str] = mapped_column(
        String(1000)
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), onupdate=datetime.now(UTC)
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
        default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True


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
