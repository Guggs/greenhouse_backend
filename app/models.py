from enum import unique
from sqlalchemy import  Boolean, Column, Integer, String, Float, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship





class Cells(Base):
    __tablename__ = "Cells"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(String, unique=True)
    co2 = Column(Float)
    h2o = Column(Float)
    cellpress840 = Column(Float)
    celltemp840 = Column(Float)
    V1 = Column(String)
    V2 = Column(String)
    V3 = Column(String)
    V4 = Column(String)
    co2_A = Column(Float)
    co2_B = Column(Float)
    co2_D = Column(Float)
    h2o_A = Column(Float)
    h2o_B = Column(Float)
    h2o_D = Column(Float)
    cellpress7000 = Column(Float)
    celltemp7000 = Column(Float)
    Mainflow = Column(String)
    Sampleflow = Column(String)
    Branchflow = Column(String)
    Rootflow = Column(String)
    CO2flow = Column(String)
    Kammername = Column(String)
    flag = Column(String)


class TemperaturesRoot(Base):
    __tablename__ = "TemperaturesRoot"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(String, unique=True)
    date = Column(String)
    time = Column(String)
    cells = relationship("TemperaturesSub", back_populates="cellData")

class TemperaturesSub(Base):
    __tablename__ = "TemperaturesSub"

    id = Column(Integer, primary_key=True, index=True)
    cellname = Column(String)
    celltemperature = Column(String)
    TemperaturesRootId = Column(Integer, ForeignKey("TemperaturesRoot.id"))    
    cellData = relationship("TemperaturesRoot", back_populates="cells")
