from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ItemModel(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Integer)

    special_offers = relationship("SpecialOfferModel", back_populates="item")


class SpecialOfferModel(Base):
    __tablename__ = 'special_offers'

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer)
    special_price = Column(Integer)

    item = relationship("ItemModel", back_populates="special_offers")
