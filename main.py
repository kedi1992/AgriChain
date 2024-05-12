from fastapi import FastAPI, Request, Depends, HTTPException
from schemas import ItemData, SpecialOfferData, ScanData
import checkout
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from model import Base, SpecialOfferModel, ItemModel

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.post("/item-price/")
def add_item_price(item: ItemData, db: Session = Depends(get_db)):
    db_item = ItemModel(name=item.item, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": f"Item {item.item} price {item.price} for added successfully"}


@app.post("/special-offer/")
def add_special_offer(offer: SpecialOfferData, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.name == offer.item).first()
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item with name '{offer.item}' not found")
    special_offer = SpecialOfferModel(item_id=item.id, quantity=offer.quantity, special_price=offer.specialPrice)
    db.add(special_offer)
    db.commit()
    return {"message": f"Special offer for {offer.item} added successfully"}


@app.post("/scan/")
def scan_items(item: ScanData, db: Session = Depends(get_db)):
    total_price = checkout.calculate_total_price(item.item, db)
    return {"totalPrice": total_price}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
