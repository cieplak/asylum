from uuid import uuid4

from sqlalchemy import MetaData as _MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, Table, Unicode, create_engine


def init(absolute_filesystem_path):
    uri = 'sqlite:///{}'.format(absolute_filesystem_path)
    global engine, Session
    engine = create_engine(uri)
    Metadata.bind = engine
    Session = scoped_session(sessionmaker(bind=engine))
    Model.query = Session.query_property()
    Model.Session = Session


engine = None
Session = None
Metadata = _MetaData()


class ModelMixin(object):

    def __repr__(self):
        name = self.__class__.__name__
        values = ', '.join(
            '{}={}'.format(
                key, str(getattr(self, key))
            )
            for key in self.__table__.columns.keys()
        )
        repr = '{}({})'.format(name, values)
        return repr

    @classmethod
    def save(cls, **kwargs):
        record = cls(**kwargs)
        cls.Session.add(record)
        cls.Session.commit()
        return record

    def delete(self):
        self.Session.delete(self)
        self.Session.commit()


Model = declarative_base(cls=ModelMixin)


class ConfigFile(Model):
    __tablename__ = 'config_file'
    name = Column(Unicode, primary_key=True)
    path = Column(Unicode)


class Container(Model):
    __tablename__ = 'container'
    name = Column(Unicode, primary_key=True)
    version = Column(Unicode)
    path = Column(Unicode)
    config = Column(Unicode)


class Jail(Model):
    __tablename__ = 'jail'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    path = Column(Unicode)
    base = Column(Unicode)
    interface = Column(Unicode)
    address = Column(Unicode)


class HttpService(Model):
    __tablename__ = 'http_service'
    id = Column(Unicode, primary_key=True, default=uuid4)
    jail = Column(Unicode, ForeignKey('jail.name'))
    host = Column(Unicode)
    path = Column(Unicode)
    port = Column(Unicode)


class PfRule(Model):
    __tablename__ = 'pf_rule'
    id = Column(Unicode, primary_key=True, default=uuid4)
    rule = Column(Unicode)


class RcSetting(Model):
    __tablename__ = 'rc_setting'
    value = Column(Unicode, primary_key=True)


class Host(Model):
    __tablename__ = 'host'
    name    = Column(Unicode, primary_key=True)
    address = Column(Unicode)
