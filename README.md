## Payment System

### Setup and Run

- Docker
- Docker Compose

### Steps
1. **Clone the repository**
```bash
git clone https://github.com/andriikuiava/trumo-payment-system.git
```

2. **Navigate to the project directory**
```bash
cd trumo-payment-system
```

3. **Build and run the containers**
```bash
docker-compose up --build
```

4. **Run the migrations (*in a separate terminal*)**
<br>
Also will create 3 payers in the database with the initial balance if there are less than 3 payers.
```bash
docker-compose exec web sh setup.sh
```


## API Endpoints
- List Payers: GET `/payers/list_balances/`
- Create Payer: POST `/payers/create_payer/`
- Make Payment: POST `/payment/transfer/`
- List Transactions: GET `/transactions/?payer_id={payer_id}`

### Example CURL Commands

- Create Payer:
POST

```bash
http://localhost:8000/api/payers/create_payer/
```
*Request Body*
```json
    {
        "name": "John Doe",
        "balance": 100.00
    }
```

- List Payers:
GET

```bash
http://localhost:8000/api/payers/list_balances/
```

- Make Payment:
POST

```bash
http://localhost:8000/api/payment/transfer/
```
*Request Body*
```json
    {
        "payer_id": 1,
        "payee_id": 2,
        "amount": 10.00
    }
```

- List Transactions:
GET
<br>
*Possible with the payer_id query parameter or without it (example below)*

```bash
http://localhost:8000/api/transactions/?payer_id=1
```

- Web Interface
```bash
http://localhost:8000/
```

### Comments
- The project is built using Django and Django Rest Framework.
- The project uses SQLite as the database.
- The project uses Docker and Docker Compose for containerization.
- I used just HTML for creating simple web interface.
- Cache is used for optimizing the balance calculation.
- In the case you have any questions, please feel free to ask. Thank you for your time and consideration.
- Contact email: **andriykuiava0511@gmail.com**