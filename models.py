from sqlalchemy import Column, Integer, String, Float, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from database import Base
from utils import CaseMixin


class Supplier(Base, CaseMixin):
    __tablename__ = 'suppliers'

    supplier_id = Column(Integer, primary_key=True, nullable=False)
    company_name = Column(String, nullable=False)
    contact_name = Column(String)
    contact_title = Column(String)
    address = Column(String)
    city = Column(String)
    region = Column(String)
    postal_code = Column(String)
    country = Column(String)
    phone = Column(String)
    fax = Column(String)
    homepage = Column(String)

    products = relationship('Product', back_populates='supplier')


class Category(Base, CaseMixin):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, nullable=False)
    category_name = Column(String, nullable=False)
    description = Column(String)
    picture = Column(LargeBinary)

    products = relationship('Product', back_populates='category')


class Product(Base, CaseMixin):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String, nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'))
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    quantity_per_unit = Column(String)
    unit_price = Column(Float)
    units_in_stock = Column(Integer)
    units_on_order = Column(Integer)
    reorder_level = Column(Integer)
    discontinued = Column(Integer, nullable=False)

    supplier = relationship('Supplier', back_populates='products')
    category = relationship('Category', lazy='immediate', back_populates='products')
