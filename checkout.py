from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from model import Base, ItemModel, SpecialOfferModel


def calculate_total_price(items: str, db: Session):
    total_price = 0

    # Count the occurrence of each item
    item_counts = {}
    for item in items:
        item_counts[item] = item_counts.get(item, 0) + 1

    # Calculate the total price based on item counts and special offers
    for item, count in item_counts.items():
        # Retrieve item price from database
        db_item = db.query(ItemModel).filter(ItemModel.name == item).first()
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"Item with name '{item}' not found")

        # Check if special offer exists for the item
        special_offer = db.query(SpecialOfferModel).filter(SpecialOfferModel.item_id == db_item.id).first()
        if special_offer and count >= special_offer.quantity:
            # Apply special offer price
            total_price += special_offer.special_price * (count // special_offer.quantity)
            # Calculate remaining items at regular price
            total_price += db_item.price * (count % special_offer.quantity)
        else:
            # No special offer, calculate total price at regular price
            total_price += db_item.price * count

    return total_price