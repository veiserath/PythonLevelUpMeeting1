from fastapi import FastAPI, Path, Depends, HTTPException, status, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
import schemas
import crud

app = FastAPI()


def get_db():
    """Dependency function returning new session for each request and closing session after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def get_root():
    """Redirect to Open API documentation."""
    return RedirectResponse('/docs')


@app.get('/suppliers', response_model=List[schemas.SupplierBrief], tags=['supplier'])
def get_suppliers(db: Session = Depends(get_db)):
    """Return list of all suppliers"""
    records = crud.read_suppliers(db)
    return [record.export() for record in records]


@app.post('/suppliers', response_model=schemas.Supplier, status_code=status.HTTP_201_CREATED, tags=['supplier'])
def add_supplier(db: Session = Depends(get_db), supplier: schemas.Supplier = ...):
    """Add new supplier from request body and return created object."""
    record = crud.create_supplier(db, supplier)

    return record.export()


@app.get('/suppliers/{id}', response_model=schemas.Supplier, tags=['supplier'])
def get_supplier(db: Session = Depends(get_db), supplier_id: int = Path(..., alias='id')):
    """Return supplier with given id."""
    record = crud.read_supplier(db, supplier_id=supplier_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supplier not found')

    return record.export()


@app.put('/suppliers/{id}', response_model=schemas.SupplierUpdate, tags=['supplier'])
def change_supplier(db: Session = Depends(get_db), supplier_id: int = Path(..., alias='id'),
                    supplier: schemas.SupplierUpdate = ...):
    """Update supplier with given id using data from request body and return updated object."""
    record = crud.update_supplier(db, supplier_id, supplier)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supplier not found')

    return record.export()


@app.delete('/suppliers/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response, tags=['supplier'])
def remove_supplier(db: Session = Depends(get_db), supplier_id: int = Path(..., alias='id')):
    """Remove supplier with given id."""
    supplier_removed = crud.delete_supplier(db, supplier_id=supplier_id)
    if not supplier_removed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supplier not found')


@app.get('/suppliers/{id}/products', response_model=List[schemas.Product], tags=['supplier'])
def get_supplier_products(db: Session = Depends(get_db), supplier_id: int = Path(..., alias='id')):
    """Return products with given supplier id."""
    records = crud.read_supplier_products(db, supplier_id=supplier_id)
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Supplier not found')

    return [record.export() for record in records]
