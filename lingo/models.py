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
    is_admin: Mapped[bool] = mapped_column(default=False)
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


class WordUpdate(db.Model):
    __tablename__ = "word_update"
    id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(db.ForeignKey("word.id"))
    update_type: Mapped[str] = mapped_column(String(1))
    value: Mapped[str] = mapped_column(
        String(50)
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC)
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
        default=datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )


class MeaningUpdate(db.Model):
    __tablename__ = "meaning_update"
    id: Mapped[int] = mapped_column(primary_key=True)
    meaning_id: Mapped[int] = mapped_column(db.ForeignKey("meaning.id"))
    update_type: Mapped[str] = mapped_column(String(1))
    value: Mapped[str] = mapped_column(
        String(1000)
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC)
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


class ReflectionUpdate(db.Model):
    __tablename__ = "reflection_update"
    id: Mapped[int] = mapped_column(primary_key=True)
    reflection_id: Mapped[int] = mapped_column(db.ForeignKey("reflection.id"))
    update_type: Mapped[str] = mapped_column(String(1))
    value: Mapped[str] = mapped_column(
        String(1000)
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC)
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
        include_fk = True


class WordUpdateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WordUpdate
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True


class MeaningSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Meaning
        load_instance = True
        sqla_session = db.session
        include_fk = True


class MeaningUpdateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MeaningUpdate
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True


class ReflectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reflection
        load_instance = True
        sqla_session = db.session
        include_fk = True


class ReflectionUpdateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ReflectionUpdate
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True


user_schema = UserSchema()
team_schema = TeamSchema()
team_member_schema = TeamMemberSchema()
word_schema = WordSchema()
word_update_schema = WordUpdateSchema()
meaning_schema = MeaningSchema()
meaning_update_schema = MeaningUpdateSchema()
reflection_schema = ReflectionSchema()
reflection_update_schema = ReflectionUpdateSchema()

users_schema = UserSchema(many=True)
teams_schema = TeamSchema(many=True)
team_members_schema = TeamMemberSchema(many=True)
words_schema = WordSchema(many=True)
word_updates_schema = WordUpdateSchema(many=True)
meanings_schema = MeaningSchema(many=True)
meaning_updates_schema = MeaningUpdateSchema(many=True)
reflections_schema = ReflectionSchema(many=True)
reflection_updates_schema = ReflectionUpdateSchema(many=True)
