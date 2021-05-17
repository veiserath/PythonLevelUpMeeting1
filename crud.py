from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func, update, delete

import models
import schemas


def read_supplier(db: Session, supplier_id: int):
    """Return supplier with given id."""
    return db.query(models.Supplier).filter(models.Supplier.supplier_id == supplier_id).first()


def read_suppliers(db: Session):
    """Return list of all suppliers."""
    return db.query(models.Supplier).order_by(models.Supplier.supplier_id).all()


def create_supplier(db: Session, supplier: schemas.Supplier):
    """Create new supplier and return its details."""
    new_id = db.query(func.max(models.Supplier.supplier_id)).scalar() + 1
    supplier.supplier_id = new_id
    db.add(models.Supplier(**supplier.dict()))
    db.commit()

    return read_supplier(db, supplier_id=new_id)


def update_supplier(db: Session, supplier_id: int, supplier_update: schemas.SupplierUpdate):
    """Update supplier with given id using data in supplier_update object."""
    update_attributes = {key: value for key, value in supplier_update.dict(exclude={'supplier_id'}).items()
                         if value is not None}
    if update_attributes != {}:
        db.execute(update(models.Supplier).where(models.Supplier.supplier_id == supplier_id).
                   values(**update_attributes))
        db.commit()

    return read_supplier(db, supplier_id=supplier_id)


def delete_supplier(db: Session, supplier_id: int):
    """Deletes supplier with given id and returns deleting flag."""
    deleted = db.query(models.Supplier).filter_by(supplier_id=supplier_id).delete()
    db.commit()
    return deleted > 0


def read_supplier_products(db: Session, supplier_id: int):
    """Return list of all products of supplier with given id"""
    return db.query(models.Product).filter(models.Product.supplier_id == supplier_id). \
        order_by(models.Product.product_id.desc()).all()
