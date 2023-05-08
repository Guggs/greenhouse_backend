import requests
import json
import datetime
from app.schemas import data_model as dm


def get_datastream_id(datastream_name, frost_url):

    server = f"{v}Datastreams?"
    query  = f"$select=id&$filter=name eq '{datastream_name}'"

    # Retrieve the key as simple JSON
    r = requests.get(server + query).json()

    if r['value'] == []:
        # TRIGGER SOME ERROR OR WARNING!
        print(f"Datastream {datastream_name} not found")
    else:
        return r['value'][0]['@iot.id']

def read_from_json_write_to_sta(blob, frost_url):

    timestamp = blob["Datum"] + "T" + blob["Zeit"]
    chamber   = blob["Kammername"][-2:]
    experiment = 'experiment:2022_heat_limit'

    if "branch" in blob["Kammername"]:

        section = "branch"
    
        # Branch-measurements contain CO2, H2O and Temperature
        co2_blob = {
            "phenomenonTime": timestamp,
            "result": blob["data_7000"]["co2_D"],
            "Datastream": {"@iot.id": get_datastream_id(f"{experiment}_{section}_{chamber}_co2", frost_url)}
        }

        x = requests.post(f"{frost_url}Observations", data=json.dumps(co2_blob))
        print(x)

        h2o_blob = {
            "phenomenonTime": timestamp,
            "result": blob["data_7000"]["h2o_D"],
            "Datastream": {"@iot.id": get_datastream_id(f"{experiment}_{section}_{chamber}_h2o", frost_url)}
        }
        x = requests.post(f"{frost_url}Observations", data=json.dumps(h2o_blob))
        print(x)
        temp_blob = {
            "phenomenonTime": timestamp,
            "result": blob["data_7000"]["celltemp"],
            "Datastream": {"@iot.id": get_datastream_id(f"{experiment}_{section}_{chamber}_temp", frost_url)}
        }
        x = requests.post(f"{frost_url}Observations", data=json.dumps(temp_blob))
        print(x)



    elif "root" in blob["Kammername"]:

        section = "root"

        co2_blob = {
            "phenomenonTime": timestamp,
            "result": blob["data_7000"]["co2_D"],
            "Datastream": {"@iot.id": get_datastream_id(f"{experiment}_{section}_{chamber}_co2", frost_url)}
        }
        x = requests.post(f"{frost_url}Observations", data=json.dumps([co2_blob]), timeout=5)



def write_data_to_sta(data: dm):

    frost_url = 'http://localhost:8000'#'http://172.27.80.119:8093/FROST-Server/v1.1/'
    experiment = 'experiment:2022_heat_limit'

    blob = {
        "data_840": {
            "co2": data.data_840.co2,
            "h2o": data.data_840.h2o,
            "cellpress": data.data_840.cellpress,
            "celltemp": data.data_840.celltemp,
        },
        "data_7000": {
            "co2_A": data.data_7000.co2_A,
            "co2_B": data.data_7000.co2_B,
            "co2_D": data.data_7000.co2_D,
            "h2o_A": data.data_7000.h2o_A,
            "h2o_B": data.data_7000.h2o_B,
            "h2o_D": data.data_7000.h2o_D,
            "cellpress": data.data_7000.cellpress,
            "celltemp": data.data_7000.celltemp
        },
        "data_VICI": {
            "V1": data.data_VICI.V1,
            "V2": data.data_VICI.V2,
            "V3": data.data_VICI.V3,
            "V4": data.data_VICI.V4
        },
        "Kammername": data.Kammername,
        "Datum": data.Datum,
        "Zeit": data.Zeit
    }

    read_from_json_write_to_sta(blob, frost_url)









