from fastapi.testclient import TestClient
import pytest

from main import app


@pytest.fixture()
def client():
    """Prepare application test client."""
    with TestClient(app) as test_client:
        yield test_client


def test_suppliers(client):
    """Test '/suppliers' endpoint."""
    test_path = '/suppliers'
    test_records = [{'SupplierID': 1, 'CompanyName': 'Exotic Liquids'},
                    {'SupplierID': 2, 'CompanyName': 'New Orleans Cajun Delights'}]

    response = client.get(test_path)
    payload = response.json()

    assert response.status_code == 200
    assert type(payload) is list
    assert sorted(payload, key=lambda item: item['SupplierID']) == payload
    assert payload[:2] == test_records


def test_supplier(client):
    """Test '/suppliers' endpoint with given supplier id."""
    test_path = '/suppliers/{}'
    test_id = 5
    test_record = {
        'SupplierID': 5,
        'CompanyName': 'Cooperativa de Quesos \'Las Cabras\'',
        'ContactName': 'Antonio del Valle Saavedra',
        'ContactTitle': 'Export Administrator',
        'Address': 'Calle del Rosal 4',
        'City': 'Oviedo',
        'Region': 'Asturias',
        'PostalCode': '33007',
        'Country': 'Spain',
        'Phone': '(98) 598 76 54',
        'Fax': None,
        'HomePage': None,
    }

    response = client.get(test_path.format(test_id))
    payload = response.json()
    response_invalid = client.get(test_path.format(999))

    assert response.status_code == 200
    assert response_invalid.status_code == 404
    assert type(payload) is dict
    assert payload == test_record


def test_supplier_products(client):
    """Test '/suppliers/{}/products' endpoint with given supplier id."""
    test_path = '/suppliers/{}/products'
    test_id = 12
    test_records = [{'ProductID': 29, 'ProductName': 'Thüringer Rostbratwurst',
                    'Category': {'CategoryID': 6, 'CategoryName': 'Meat/Poultry'}, 'Discontinued': 1},
                    {'ProductID': 28, 'ProductName': 'Rössle Sauerkraut',
                    'Category': {'CategoryID': 7, 'CategoryName': 'Produce'}, 'Discontinued': 1}]

    response = client.get(test_path.format(test_id))
    payload = response.json()
    response_invalid = client.get(test_path.format(999))

    assert response.status_code == 200
    assert response_invalid.status_code == 404
    assert type(payload) is list
    assert payload[-2:] == test_records


def test_create_supplier(client):
    """Test POST '/suppliers' endpoint."""
    test_path = '/suppliers'
    verify_path = '/suppliers/{}'
    new_record = {
        'CompanyName': 'Test Company Name',
        'ContactName': 'Test Contact Name',
        'ContactTitle': 'Unknown',
        'Address': 'Test Address',
        'City': 'Test City',
        'PostalCode': '123-123',
        'Country': 'Unknown',
        'Phone': '123-123-123',
    }
    new_short_record = {'CompanyName': 'Short Company Name'}
    invalid_record = {'City': 'Test City'}

    response_invalid = client.post(test_path, json=invalid_record)
    response = client.post(test_path, json=new_record)
    payload = response.json()
    response_verify = client.get(verify_path.format(payload['SupplierID']))
    response_short = client.post(test_path, json=new_short_record)
    payload_short = response_short.json()
    response_short_verify = client.get(verify_path.format(payload_short['SupplierID']))

    assert response_invalid.status_code == 422
    assert response.status_code == 201
    assert response_verify.status_code == 200
    assert payload.items() <= response_verify.json().items()
    assert response_short.status_code == 201
    assert response_short_verify.status_code == 200
    assert payload_short.items() <= response_short_verify.json().items()


def test_update_supplier(client):
    """Test PUT '/suppliers' endpoint with given supplier id."""
    test_path = '/suppliers/{}'
    create_path = '/suppliers'
    new_record = {'CompanyName': 'Update Company Name'}
    update_attributes = {'City': 'New City', 'Address': 'New address'}

    response_create = client.post(create_path, json=new_record)
    payload = response_create.json()
    supplier_id = payload['SupplierID']
    response_update = client.put(test_path.format(supplier_id), json=update_attributes)
    payload_updated = response_update.json()

    assert response_update.status_code == 200
    payload.update(update_attributes)
    assert payload_updated == payload


def test_delete_supplier(client):
    """Test DELETE '/suppliers' endpoint with given supplier id."""
    test_path = '/suppliers/{}'
    create_path = '/suppliers'
    new_record = {'CompanyName': 'Delete Company Name'}

    response_create = client.post(create_path, json=new_record)
    payload = response_create.json()
    supplier_id = payload['SupplierID']
    response_delete = client.delete(test_path.format(supplier_id))
    response_duplicate = client.delete(test_path.format(supplier_id))
    response_verify = client.get(test_path.format(supplier_id))

    assert response_delete.status_code == 204
    assert response_duplicate.status_code == 401
    assert response_verify.status_code == 404
