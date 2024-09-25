import datetime

from typing import Annotated, List
from sqlalchemy import Float, String, ForeignKey, text, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orm.database import Base

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )]

class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    messenger_id: Mapped[int] = mapped_column(ForeignKey("messenger.id", ondelete="NO ACTION"))
    segment_id: Mapped[int] = mapped_column(ForeignKey("customer_segment.id", ondelete="SET NULL"))
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    phone: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    requirements: Mapped[List["Requirement"]] = relationship(back_populates="user")
    orders: Mapped[List["Order"]] = relationship(back_populates="user_orders")

    user_messenger: Mapped["Messenger"] = relationship(back_populates="users")
    user_segement: Mapped["CustomerSegment"] = relationship(back_populates="user")

class Requirement(Base):
    __tablename__ = "requirement"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="NO ACTION"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="NO ACTION"))
    status: Mapped[str] = mapped_column(String, default="Выявлена")
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped["User"] = relationship(back_populates="requirements")
    product: Mapped["Product"] = relationship("product_requirements")

class Product(Base):
    __tablename__ = "product"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Float)

    product_requirements: Mapped[List["Requirement"]] = relationship(back_populates="product")

class Order(Base):
    __tablename__ = "order"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="NO ACTION"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user_orders: Mapped["User"] = relationship(back_populates="orders")
    
class CustomerSegment(Base):
    __tablename__ = "customer_segment"
    
    id: Mapped[intpk]
    integration_id: Mapped[str] = mapped_column(ForeignKey("integration.id"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    profession: Mapped[str] = mapped_column(String, nullable=False)

    intagrations: Mapped[List["Integration"]] = relationship(back_populates="segement")


class Integration(Base):
    __tablename__ = "integration"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String, nullable=False)
    type_source: Mapped[str] = mapped_column(String, nullable=False)

    segement: Mapped["CustomerSegment"] = relationship(back_populates="intagrations")

class Messenger(Base):
    __tablename__ = "messenger"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String, nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="user_messenger")



