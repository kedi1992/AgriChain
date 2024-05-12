# AgriChain

AgriChain is a supermarket checkout process application that calculates the total price of items added to the cart by the customer. It supports individual pricing for items as well as special offers for bulk purchases.

## Technical Requirements

- Python 3.9 or later
- FastAPI
- SQLite database

## Project Setup

### 1. Clone the Repository

git clone https://github.com/your-username/AgriChain.git
cd AgriChain

### 2. Set Up the Environment

Create and activate a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

### 3. Running the Project with Docker Compose

docker-compose up --build


## Usage

### 1. Adding Items using API

To add an item, send a POST request to the `/item-price/` endpoint with the item details in the request body.

Example:
curl -X POST http://localhost:8000/item-price/ -H "Content-Type: application/json" -d '{"item": "A", "price": 50}'


### 2. Adding Special Offers using API

To add a special offer, send a POST request to the `/special-offer/` endpoint with the offer details in the request body.

Example:
curl -X POST http://localhost:8000/special-offer/ -H "Content-Type: application/json" -d '{"item": "A", "quantity": 3, "specialPrice": 130}'


### 3. Scanning Items using API

To scan items and calculate the total price, send a POST request to the `/scan/` endpoint with the items in the request body.

Example:
curl -X POST http://localhost:8000/scan/ -H "Content-Type: application/json" -d '{"item": "AAABBD"}'


## Continuous Integration and Deployment (CI/CD)

The project is configured with GitHub Actions for continuous integration. Test cases are automatically run on every push to the main branch. Branch protection rules are set up to ensure that all tests pass before allowing code to be merged into the main branch.


