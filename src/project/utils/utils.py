import base64
import json


def base64_json(input_json: dict):
    sorted_json = sort_json_keys(input_json)
    str_json = json_to_str(sorted_json)
    res_base64_json = base64_str(str_json)
    return res_base64_json


def base64_str(string):
    str_bytes = string.encode('utf8')
    base64_bytes = base64.b64encode(str_bytes)
    res_base64_str = base64_bytes.decode('utf8')
    return res_base64_str


def sort_json_keys(unsorted_json: dict):
    sorted_json = json.dumps(unsorted_json, sort_keys=True)
    return sorted_json


def bytes_to_json(input_bytes: bytes):
    decoded_json = json.loads(input_bytes)
    return decoded_json


def json_to_str(input_json: dict):
    str_json = json.dumps(input_json)
    return str_json
