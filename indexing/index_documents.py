import pandas as pd
import configparser
import ast
from indexing.logconfig import get_logger
import json
import requests

config = configparser.ConfigParser()
config.read('../config/elk_config.ini')

log_path = config['LOGS']['log_path']
sample_index = ast.literal_eval(config['DATA']['sample_index'])
sample_document = ast.literal_eval(config['DATA']['sample_document'])
base_url = config['URL']['base_url']
index_name = config['URL']['index_name']
bulk_upload = config['URL']['bulk_upload']
search = config['URL']['search']
query_payload = ast.literal_eval(config['URL']['query_payload'])
logger = get_logger(__name__, log_path, consoleHandlerrequired=False)


def read_and_transform_input_data():
    """Reads tagged/annotated data from csv,iterates through it and converts it into NDJSON structure as elastic
    search REST API endpoint is /_bulk, and it expects the newline delimited JSON (NDJSON) structure. """
    try:
        data = pd.read_csv("../data/video_details.csv")
        with open('../data/documents.json', 'w') as out_file:
            for index, row in data.iterrows():
                sample_index["index"]["_id"] = int(row["id"])
                link = row["link"]
                objects = row["objects"].split('||')
                objects_in_dict_form = []
                for obj in objects:
                    name, duration = obj.split(":")
                    tmp = {"object":name, "duration": duration}
                    objects_in_dict_form.append(tmp)
                sample_document["link"] = link
                sample_document["objects"] = objects_in_dict_form
                out_file.write(json.dumps(sample_index)+'\n')
                out_file.write(json.dumps(sample_document)+'\n')
        return True
    except Exception as e:
        logger.exception(e)
        raise


def bulk_index_elastic_search():
    """Reads data from json file,calls Elastic search bulk index API to store all documents in named index and
    returns status of operation """
    try:
        url = base_url + index_name + '/' + bulk_upload
        logger.info("bulk indexing URL :"+url)
        with open('../data/documents.json', 'r') as in_file:
            params = in_file.read()
        headers = {"Content-Type": "application/x-ndjson"}
        r = requests.post(url=url, data=params, headers=headers)
        logger.info("Response status code from bulk index api: " + str(r.status_code))
        if r.status_code == 200:
            res = r.json()
            success = res['errors']
            return success
        else:
            raise Exception('Error while indexing documents in ES')
    except Exception as e:
        logger.exception(e)
        raise


def search_documents(user_input):
    """Takes user input, forms query string and triggers ES 'search API' and returns matched records """
    try:
        url = base_url + index_name + '/' + search
        query_payload["query"]["query_string"]["query"] = user_input
        params = json.dumps(query_payload)
        logger.info("input to ES search API :"+params)
        headers = {"Content-Type": "application/json"}
        r = requests.post(url=url, data= params,headers=headers)
        logger.info("Response status code from search api: " + str(r.status_code))
        if r.status_code == 200:
            return r.json()["hits"]["hits"]
        else:
            msg = r.json()['error']['reason']
            raise Exception(msg)
    except Exception as e:
        logger.exception(e)
        raise


if __name__ == '__main__':
    try:
        data_transformed_to_json = read_and_transform_input_data()
        if data_transformed_to_json:
            logger.info("Data transformation from csv to json is Completed .Now calling bulk index API to store in ES")
            status = bulk_index_elastic_search()
            logger.info("Is any error in indexing? " + str(status))
        else:
            logger.info("Data transformation failed. Status of read_and_transform_method : " + str(data_transformed_to_json))
    except Exception as exc:
        logger.exception(exc)

