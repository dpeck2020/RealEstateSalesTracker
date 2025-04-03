from app import db
from sqlalchemy import Integer, String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

# Define your database models here

class Property(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    street: Mapped[str] = mapped_column(String(255), index=True, nullable=True)
    city: Mapped[str] = mapped_column(String(100), index=True, nullable=True)
    state: Mapped[str] = mapped_column(String(10), index=True, nullable=True)
    zip_code: Mapped[str] = mapped_column(String(20), index=True, nullable=True)
    sale_price: Mapped[int] = mapped_column(Integer, nullable=True)
    sale_date: Mapped[datetime.date] = mapped_column(Date, index=True, nullable=True)
    lot_size: Mapped[float] = mapped_column(Float, nullable=True) # Specify units (e.g., acres, sqft) in comments or docs
    square_footage: Mapped[int] = mapped_column(Integer, nullable=True)
    # buyer_name = mapped_column(String(255), nullable=True) # Not readily available in CSV
    # seller_name = mapped_column(String(255), nullable=True) # Not readily available in CSV
    trulia_url: Mapped[str] = mapped_column(String(512), nullable=True) # Store the source URL
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=True)
    bathrooms: Mapped[float] = mapped_column(Float, nullable=True) # Use float for half baths (e.g., 1.5)
    
    # Relationship to PropertyImage
    images: Mapped[list['PropertyImage']] = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Property {self.street}, {self.city}>'

class PropertyImage(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String(1024), nullable=False) # Increased length for potentially long URLs
    property_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('property.id'), nullable=False, index=True)

    # Relationship back to Property
    property: Mapped['Property'] = relationship("Property", back_populates="images")

    def __repr__(self):
        return f'<PropertyImage {self.url} for Property {self.property_id}>'
