from fastapi import FastAPI, Depends
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.schemas import data_model, Temperatures, requestData, CellsCreate, configurationDataSchema
import app.models as models




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
