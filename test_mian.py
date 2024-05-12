import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db, engine
from model import Base, ItemModel, SpecialOfferModel

# Common setup function to insert values into the database
def setup_database():
    # Create a session to interact with the database
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Insert test data into the database
    item_a = ItemModel(name="A", price=50)
    item_b = ItemModel(name="B", price=30)
    item_c = ItemModel(name="C", price=20)
    item_d = ItemModel(name="D", price=15)

    special_offer_a = SpecialOfferModel(item=item_a, quantity=3, special_price=130)
    special_offer_b = SpecialOfferModel(item=item_b, quantity=2, special_price=45)
    db.add_all([item_a, item_b, item_c, item_d, special_offer_a, special_offer_b])
    db.commit()
    db.close()


# Override the get_db function to use the temporary in-memory database session
@pytest.fixture(scope="function")
def test_db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    yield engine

client = TestClient(app)
setup_database()


def test_scan_individual_items(test_db_session):
    response = client.post("/scan/", json={"item": "A"})
    assert response.status_code == 200
    assert response.json() == {
        "totalPrice": 50
    }


def test_scan_items_with_special_offers():
    response = client.post("/scan/", json={"item": "ABAABA"})
    assert response.status_code == 200
    assert response.json() == {"totalPrice": 225}


def test_scan_non_existing_item():
    response = client.post("/scan/", json={"item": "Z"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item with name 'Z' not found"}


def test_scan_items_with_combinations():
    test_cases = [
        ("", 0),
        ("A", 50),
        ("AB", 80),
        ("CDBA", 115),
        ("AA", 100),
        ("AAA", 130),
        ("AAAA", 180),
        ("AAAAA", 230),
        ("AAAAAA", 260),
        ("AAAB", 160),
        ("AAABB", 175),
        ("AAABBD", 190),
        ("DABABA", 190)
    ]
    for items, expected_price in test_cases:
        response = client.post("/scan/", json={"item": items})
        assert response.status_code == 200
        assert response.json()["totalPrice"] == expected_price
