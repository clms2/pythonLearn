import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, DECIMAL, String, Text, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:123456@127.0.0.1:3306/test", max_overflow=5)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    photos = Column(Text())
    supplier = Column(String(10))
    catalog = Column(String(30))
    belong = Column(String(30))
    price = Column(DECIMAL(10, 2))
    created_at = Column(Date())

    def insert_data(self, rows):
        session.add_all(rows)
        session.commit()

    def __repr__(self):
        return """
            <Data(id:%s, title:%s, photos:%s, supplier:%s, catalog:%s, belong:%s, price:%s, created_at:%s)>
        """ % (self.id, self.title, self.photos, self.supplier, self.catalog, self.belong, self.price, self.created_at)


# Data().insert_data([
#     Data(title="t2", price=2.11),
#     Data(title="t3", price=3.22),
# ])
