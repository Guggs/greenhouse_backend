from fastapi import FastAPI, Depends
#from  app.temperatures import temperatures as temperatures
from app.schemas import data_model, Temperatures, requestData, CellsCreate, configurationDataSchema
from fastapi.middleware.cors import CORSMiddleware
import app.models as models
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
#import app.database_functions as df
import app.configurationData as cd
#import app.post_data_to_sta as pds


models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


configurationData:cd.configurationData = cd.configurationData(25, 0.5) 

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def set_cells(temperatures_id: int, cells: CellsCreate, db: Session = Depends()):
    print('set_cells', cells)
    for cell in cells:
        cells_model = models.TemperaturesSub(**cell.dict(), TemperaturesRootId=temperatures_id)
        db.add(cells_model)
    db.commit()

def set_temps(temperatures: Temperatures, datetime: str, db: Session = Depends()):
    print('set_temps')
    print(' datetime', datetime)
    temperatures_model = models.TemperaturesRoot()
    temperatures_model.datetime = datetime
    temperatures_model.date = temperatures.Datum
    temperatures_model.time = temperatures.Zeit
    db.add(temperatures_model)
    db.commit()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the greenhouse app!!!!"}

@app.get("/data")
def get_data(db: Session = Depends(get_db)):
    return db.query(models.Cells).all()

@app.post("/data_model/")
async def coolingData(cell:data_model, db: Session = Depends(get_db)):
    cells_model = models.Cells()
    cells_model.datetime = cell.Datum+'_'+cell.Zeit
    cells_model.co2 = cell.data_840.co2
    cells_model.co2_A = cell.data_7000.co2_A
    cells_model.co2_B = cell.data_7000.co2_B
    cells_model.co2_D = cell.data_7000.co2_D
    cells_model.h2o_A = cell.data_7000.h2o_A
    cells_model.h2o_B = cell.data_7000.h2o_B
    cells_model.h2o_D = cell.data_7000.h2o_D
    cells_model.Kammername = cell.Kammername
    cells_model.flag = cell.flag
    db.add(cells_model)
    db.commit()
    try:
        print('post datamodel')
        print('cells time: ', cells_model.datetime)
        print(' cell.data_840.co2: ', cell.data_840.co2)
        print(' cell.Kammername: ', cell.Kammername)
        print(' cell.flag: ', cell.flag)
    except Exception as e:
        print('Exception: ',e)
    #pds.write_data_to_sta(cell)
    return {"data_840": cell.data_840, "data_7000": cell.data_7000,"data_VICI": cell.data_VICI}

@app.post("/set_temperatures")
async def set_temperatures(temperatures: Temperatures, db: Session = Depends(get_db)):
    print('in set temperatures')
    datetime = temperatures.Datum+'_'+temperatures.Zeit
    print(datetime)
    print('setting temps')
    set_temps(temperatures, datetime, db)
    print('setting cells')
    set_cells(db.query(models.TemperaturesRoot.id).filter(models.TemperaturesRoot.datetime == datetime).first()[0], temperatures.cells, db)

@app.get("/temperatures")
async def get_temperatures(db: Session = Depends(get_db)):
    return db.query(models.TemperaturesRoot).all()

@app.get("/cells")
async def get_temperatures(db: Session = Depends(get_db)):
    return db.query(models.TemperaturesSub).all()

@app.get("/dashboardData")
async def get_dashboardData(db: Session = Depends(get_db)):
    try:
        Datum = ""
        Time = ""
        cells = []
        flag = ""
        currentCell = ""
        co2_A = ""
        co2_B = ""
        co2_D = ""
        h2o_A = ""
        h2o_B = ""
        h2o_D = ""
        temps = db.query(models.TemperaturesRoot).order_by(models.TemperaturesRoot.id.desc()).limit(1).first()
        cellAirData = db.query(models.Cells).order_by(models.Cells.id.desc()).limit(1).first()
        datamodel = db.query(models.TemperaturesSub).filter(temps.id == models.TemperaturesSub.TemperaturesRootId).all()
        try:
            print('get dashboardData')
            print(' temps date: ', temps.date)
            print(' temps id: ', temps.id)
            print(' cells: ', datamodel)
            print(' flag: ', cellAirData.flag)
            print(' currentCell: ', cellAirData.Kammername)
        except Exception as e:
            print('Exception: ',e)
            
        if temps is not None and cellAirData is not None:
            if temps.datetime == cellAirData.datetime and cellAirData.datetime is not None:
                Datum = temps.date
                Time = temps.time
                cells = datamodel
                flag = cellAirData.flag
                currentCell = cellAirData.Kammername
                co2_A = cellAirData.co2_A
                co2_B = cellAirData.co2_B
                co2_D = cellAirData.co2_D
                h2o_A = cellAirData.h2o_A
                h2o_B = cellAirData.h2o_B
                h2o_D = cellAirData.h2o_D
    except Exception as e:
        return {"message": "no new values found"+str(e)}
    return {"Datum":Datum, "Time":Time, "cells" :cells,"flag":flag,"currentCell": currentCell, "co2_A": co2_A, "co2_B": co2_B, "co2_D": co2_D, "h2o_A": h2o_A, "h2o_B": h2o_B, "h2o_D": h2o_D}



@app.get("/configurationData")
async def get_temperatures():
    print(configurationData.get_configurationData())
    return configurationData.get_configurationData()

@app.post("/setConfigurationData")
async def set_ConfigurationData(configurationDataPost: configurationDataSchema):
    #print(configurationDataPost.tolerance, configurationDataPost.targetTemp)
    configurationData.set_configurationData(configurationDataPost.tolerance, configurationDataPost.targetTemp)
    return configurationData.get_configurationData()