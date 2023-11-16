from datetime import datetime
from config import db, ma

class Word(db.Model):
    __tablename__ = "word"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class WordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Word
        load_instance = True
        sqla_session = db.session

word_schema = WordSchema()
words_schema = WordSchema(many=True)


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

