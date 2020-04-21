from app import db
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Table, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import event
from sqlalchemy import inspect
from sqlalchemy.orm.query import Query

"""
Create Base flask-sqlalchemy models for inheritance by other models. All other models use vanilla SQLAlchemy so that 
vanilla SQLAlchemy's superior documentation is 100% applicable to all other models.
"""


class Base(db.Model):
    """ Abstract SQL Alchemy Model for all classes. Implements a set of standard columns and delcares an attributed that
    returns an sql table name derived from the model class name.

    """

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        """ default table name for sqlalchemy model

        Returns:
            string: class name

        """
        return cls.__name__

    """ Data Columns """
    xid = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)


############################################

request_notification_table = Table('request_notification_table', Base.metadata,
    Column('request_xid', Integer, ForeignKey('Request.xid')),
    Column('notification_xid', Integer, ForeignKey('Notification.xid'))
)

heartbeat_notification_table = Table('heartbeat_notification_table', Base.metadata,
    Column('heartbeat_xid', Integer, ForeignKey('Heartbeat_Receive.xid')),
    Column('notification_xid', Integer, ForeignKey('Notification.xid'))
)

class Core(Base):
    heading = Column(String(255))
    subheading = Column(String(255))

class Request(Base):
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    expected_status = Column(Integer())
    check_type = Column(String(255), nullable=False)
    check_method = Column(String(255))
    post_data = Column(String(255))
    port = Column(Integer())
    timeout = Column(Integer())
    visible = Column(Boolean(), nullable=False)
    notify_afer = Column(Integer())
    allow_notifications = Column(Boolean(), nullable=False)
    all_notifications = Column(Boolean(), nullable=False)
    enabled = Column(Boolean(), nullable=False)

    """ Relationships """
    request_result = relationship('Request_Result', back_populates='request')

    notification = relationship(
        "Notification",
        secondary=request_notification_table,
        back_populates="request")

class Request_Result(Base):
    value = Column(Float())

    """ Relationships """
    request = relationship('Request', back_populates='request_result')

    """ Foreign Keys """
    request_xid = Column(Integer, ForeignKey('Request.xid'))

class Notification(Base):
    method = Column(String(255))
    service = Column(String(255))
    enabled = Column(Boolean())

    """ Relationships """
    request = relationship(
        "Request",
        secondary=request_notification_table,
        back_populates="notification")

    heartbeat = relationship(
        "Heartbeat_Receive",
        secondary=heartbeat_notification_table,
        back_populates="notification")

class Heartbeat_Receive(Base):
    name = Column(String(255))
    token = Column(String(255))
    last_beat = Column(String(255))
    notify_afer = Column(Integer()) # mins of missing beats
    allow_notifications = Column(Boolean())
    all_notifications = Column(Boolean())
    enabled = Column(Boolean())

    """ Relationships """

    notification = relationship(
        "Notification",
        secondary=heartbeat_notification_table,
        back_populates="heartbeat")


class Heartbeat_Send(Base):
    name = Column(String(255))
    address = Column(String(255))
    port = Column(Integer())
    token = Column(String(255))
    enabled = Column(Boolean())