import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base

engine = sq.create_engine("sqlite:///database.db")

SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()
Base = declarative_base()

class Students(Base):
    __tablename__ = "students"

    id = sq.Column(sq.Integer, primary_key=True)
    student = sq.Column(sq.Text, nullable=False)
    group = sq.Column(sq.Text, nullable=False)
    merge_request = sq.Column(sq.Text, nullable=False)
    points = sq.Column(sq.Integer, nullable=False)

Base.metadata.create_all(bind=engine)
