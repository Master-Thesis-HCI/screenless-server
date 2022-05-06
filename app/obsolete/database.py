import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLAlchemyBase = declarative_base()
engine = sa.create_engine("sqlite:///sqlite.db", echo=False)
Session = sessionmaker(bind=engine)


class Devices(SQLAlchemyBase):
    __tablename__ = 'Devices'
    device_id = sa.Column(sa.String(16), primary_key=True)
    screentime = sa.Column(sa.Integer)
    updated = sa.Column(sa.DateTime)

    def __repr__(self):
        return f"<URL(device_id='{self.device_id}', screentime='{self.screentime}', updated='{self.updated}')>"

SQLAlchemyBase.metadata.create_all(engine)
