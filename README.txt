# TicketLite - Setup and Run Instructions

# Requirements:
- Python 3.10 or higher
- pip



# Setup

1. Unzip the project folder

2. Create and activate a virtual environment:
    python -m venv .venv

    Windows: .venv\scripts\activate
    MAC: source .venv/bin/activate

3. Install the attached dependencies
    pip install -r requirements.txt

4. Run the server locally
    python manage.py runserver

5. Open browser and go to:
    https://127.0.0.1:8000



## Test User Accounts

Username: owen.robbins   Password: Password123   (SuperUser)
Username: bob      Passwrod: Password123!        (Staff)
Username: carol     Password: Password123!
username: dave     Password: Password123!
username: eve     Password: Password123!
username: frank     Password: Password123!
username: grace     Password: Password123!       (Staff)
username: harry     Password: Password123!
username: henry     Password: Password123!       (Staff)
username: susan     Password: Password123!


# NOTE
- Database is prefilled with sample Data
- Django admin panel is available at https://127.0.0.1:8000/admin/
- Enjoy 