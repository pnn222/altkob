from sqlalchemy import Column, Text, Integer, JSON
from project.database.models._base import Base


class RequestInfo(Base):

    __tablename__ = "request"
    __table_args__ = {"schema": "main", "extend_existing": True}

    id = Column(Text, primary_key=True)
    request = Column(JSON)
    duplicates = Column(Integer, default=0)
