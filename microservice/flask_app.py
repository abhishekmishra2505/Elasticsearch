from flask import Flask, jsonify, request
import re
from indexing.logconfig import get_logger
from indexing.index_documents import search_documents
import configparser
import traceback
import json

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('../config/elk_config.ini')

log_path = config['LOGS']['log_path']
logger = get_logger(app.name, log_path, consoleHandlerrequired=False)

conjunction = ' AND '
union = ' OR '


@app.route('/api')
def sample():
    res = {}
    logger.warning('A warning occurred (%d apples)', 42)
    logger.error('An error occurred')
    logger.info('Info')
    res['message'] = 'Hi! This is test API message'
    res['statusCode'] = 200
    return jsonify(res)


@app.route('/api/search', methods=['POST'])
def get_documents_es():
    try:
        if not request.json and request.json['userInput'] is None:
            return jsonify({"code": 401, "message": "Error in request body. Request params missing."})
        if request.json['userInput'] == "":
            return jsonify({"code": 402, "message": "Question is blank in the request body."})
        user_input = request.json['userInput']
        user_input = re.sub(r'[^&|\w]+', '', user_input)
        logger.info('User input after cleaning (spaces,extra characters except & and || ) is :' + user_input)
        input_keyword_list = user_input
        if '||' in user_input:
            input_keyword_list = user_input.split('||')
            user_input = union.join(input_keyword_list)
        if '&' in user_input:
            input_keyword_list = user_input.split('&')
            user_input = conjunction.join(input_keyword_list)

        docs = search_documents(user_input)
        results = list(map(lambda x: x['_source'], docs))
        # below for loop block filters other objects from response (it can be kept configurable as and when required)
        for item in results:
            objects = item['objects']
            filtered_objects = [x for x in objects if x['object'] in input_keyword_list]
            item['objects'] = filtered_objects
        res = {"searchResults": results}
        return jsonify(res)
    except Exception as e:
        logger.exception(e)
        error_response = {}
        exc = traceback.format_exc()
        exe_array = exc.split('\n')
        error_response['searchResults'] = None
        error_response['error'] = exe_array[len(exe_array) - 2]  # traceback.format_exc(limit=100)
        logger.info(error_response)
        return json.dumps(error_response)


if __name__ == '__main__':
    app.run(debug=False)


