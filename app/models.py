from app import db
from sqlalchemy import Integer, String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
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
    image_url: Mapped[str] = mapped_column(String(512), nullable=True)
    buyer_name: Mapped[str] = mapped_column(String(255), nullable=True)
    seller_name: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self):
        return f'<Property {self.street}, {self.city}, {self.state}>'
