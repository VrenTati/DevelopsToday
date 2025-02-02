# SpyCat API

SpyCat is a FastAPI-based application for managing cats and their missions. You can create, update, delete cats and missions, as well as assign cats to missions with validation to ensure proper functionality.

## Features

- Manage cats and their attributes such as name, breed, and salary.
- Validate cat breeds using The Cat API.
- Create and manage missions with multiple targets.
- Assign cats to missions with constraints.
- Automatically mark missions as complete when all targets are completed.

---

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 13+

### Clone the Repository

```bash
git clone https://github.com/VrenTati/DevelopsToday.git
cd spycat
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root and add the following variables:

```env
APP_CONFIG__DB__URL=postgresql+asyncpg://user:pwd@localhost:5432/spy_cat
APP_CONFIG__DB__ECHO=0
APP_CONFIG__DB__ECHO_POOL=0
APP_CONFIG__DB__MAX_OVERFLOW=50
APP_CONFIG__DB__POOL_SIZE=10
```

Update the values as per your environment.

---

## Database Setup

1. Initialize the database:

```bash
alembic upgrade head
```

This will apply the migrations and create the necessary tables in your PostgreSQL database.

---

## Running the Application

Start the FastAPI server:

```bash
pytnhon main.py
```

The application will be available at `http://127.0.0.1:8000`.

---

## API Routes
`http://127.0.0.1:8000/docs`

