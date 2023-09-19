# Recognition of Prior Learning Backend

A Flask application for performing CRUD (Create, Read, Update, Delete) operations on a MySQL database using the `Flask-SQLAlchemy` and `Flask-Marshmallow` extensions. This project was developed as a backend for the ICT621 Group Project unit.

## Setup

### 1. Environment Setup:

```bash
pip install flask flask_sqlalchemy flask_marshmallow marshmallow-sqlalchemy mysqlclient

### 2. Application Structure:

```bash
/RPL-Backend
|-- /app
|   |-- __init__.py
|   |-- models.py
|   |-- views.py
|-- run.py

### 3. Configuration:

In app/__init__.py, replace username, password, and dbname with your MySQL credentials and database name.

## Running the Application

To run the application:

```bash
python run.py

