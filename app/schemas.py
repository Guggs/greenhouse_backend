from pydantic import BaseModel
from typing import List



class CellsBase(BaseModel):
    cellname: str
    celltemperature: float

class CellsCreate(CellsBase):
    pass

class Cells(CellsBase):
    

    class Config:
        orm_mode = True
        #allow_population_by_field_name = True

class TemperaturesBase(BaseModel):
    Datum: str
    Zeit: str
    Modul_05: str
    Modul_06: str
    Modul_11: str
    Modul_12: str
    Temp_Set: str


class TemperaturesCreate(TemperaturesBase):
    pass

class Temperatures(TemperaturesBase):
    cells: list[Cells] = []

    class Config:
        orm_mode = True
        #allow_population_by_field_name = True



class requestData(BaseModel):
    Datum: str
    Zeit: str
    cells = []
    flag = str
    currentCell: str

class data_840(BaseModel):
    co2: float
    h2o: float
    cellpress: float
    celltemp: float

class data_VICI(BaseModel):
    V1: str
    V2: str
    V3: str
    V4: str

class data_7000(BaseModel):
    co2_A: float
    co2_B: float
    co2_D: float
    h2o_A: float
    h2o_B: float
    h2o_D: float
    cellpress: float
    celltemp: float

class flows(BaseModel):
    Mainflow: str
    Sampleflow: str
    Branchflow: str
    Rootflow: str
    CO2flow: str

class data_model(BaseModel):
    data_840: data_840
    data_7000: data_7000
    data_VICI: data_VICI
    flows: flows
    Kammername: str
    Datum: str
    Zeit: str
    flag: str

class configurationDataSchema(BaseModel):
    targetTemp: float
    tolerance: float