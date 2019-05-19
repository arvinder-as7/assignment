from sqlalchemy import Column, INTEGER, TEXT

from app import db

Base = db.make_declarative_base(db.Model)


class URLMapping(Base):
    __tablename__ = "url_mapping"

    id = Column(INTEGER, primary_key=True)
    hash = Column(TEXT, nullable=False)
    url = Column(TEXT, nullable=False)

    def __repr__(self) -> str:
        return f'URL {self.url}'

    def serialize(self) -> dict:
        return {'hash': self.hash, 'url': self.url}
