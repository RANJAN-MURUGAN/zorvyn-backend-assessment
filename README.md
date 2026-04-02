# Zorvyn Finance Dashboard API

A lightweight, robust backend service designed for a finance dashboard. This project securely manages financial records, aggregates data for analytics, and strictly enforces Role-Based Access Control (RBAC).

## Setup & Installation Process

1. Clone the repository and navigate into the folder:
   
   git clone https://github.com/RANJAN-MURUGAN/zorvyn-backend-assessment.git
   cd zorvyn-backend

2. Create and activate a virtual environment:

    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On Mac/Linux:
    source venv/bin/activate

3. Install dependencies:

    pip install -r requirements.txt
    
4. Run the server:

    uvicorn main:app --reload


# API Explanation
Once the server is running, navigate to http://127.0.0.1:8000/docs to access the interactive Swagger UI. The API consists of the following core endpoints:

POST /records/: Creates a new financial record. Validates that the amount is positive and the type is strictly "Income" or "Expense".

GET /records/: Retrieves records. Supports optional query parameters (?category= and ?type=) for filtering.

PUT /records/{id}: Updates an existing record.

DELETE /records/{id}: Removes a record from the database.

GET /dashboard/summary: Returns aggregated analytics, including net balance, category-wise totals, and the 5 most recent transactions.

# Assumptions Made
To focus strictly on backend architecture and logic, the following assumptions were made:

Authentication: Instead of configuring a full OAuth2 or JWT flow, authentication is mocked using an X-User-Role HTTP header. This successfully demonstrates how the RBAC middleware evaluates user claims before allowing route access.

Role Definitions:

Admin: Full read, write, update, and delete access.

Analyst: Can view analytics and create records, but cannot edit or delete historical data.

Viewer: Read-only access to the dashboard and records.