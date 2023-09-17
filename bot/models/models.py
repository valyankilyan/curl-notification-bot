from sqlalchemy import Column, BigInteger, String, Boolean, Integer
from models import metadata, engine, base
from models.modelclass import Model

class User(base, Model):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, unique=True)
    username = Column(String)
    password = Column(String)
    is_admin = Column(Boolean)

    def __init__(self, tg_id: int, username: str, password: str):
        self.tg_id = tg_id
        self.username = username
        self.password = password
        self.is_admin = False

    def __repr__(self):
        return f'{self.id}. @{self.username} admin={self.is_admin}'

metadata.create_all(engine)