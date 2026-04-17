# flake8: noqa: E402
import os
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_emp_db.db'
from models import models
import pytest
from app import app, db


@pytest.fixture
def client():
    with app.app_context():
        initDB()
        yield app.test_client()
        truncateDB()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_index_response(client):
    response = client.get('/')
    assert b"Employee Data" in response.data
    with app.app_context():
        assert models.Employee.query.count() == 0


def initDB():
    db.create_all()


def truncateDB():
    models.Employee.query.delete()
    db.session.commit()


def test_add(client):
    test_data = {'name': 'Mickey Test',
                 'gender': 'male',
                 'address': 'IN',
                 'phone': '0123456789',
                 'salary': '2000',
                 'department': 'Sales'}
    client.post('/add', data=test_data)
    with app.app_context():
        assert models.Employee.query.count() == 1


def test_edit(client):
    response = client.post('/edit/0')
    assert response.status_code == 200
    assert b"Sorry, the employee does not exist." in response.data


def test_delete(client):
    test_data = {'emp_id': 0}
    response = client.post('/delete', data=test_data)
    assert response.status_code == 200
    assert b"Sorry, the employee does not exist." in response.data
