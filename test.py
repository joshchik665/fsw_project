import json
from fsw.config import SETTINGS
import common.utilities as util
import os
from dataclasses import asdict

settings_dictionary = {}
for setting, setting_obj in SETTINGS.items():
    obj_dict = asdict(setting_obj)
    settings_dictionary[setting] = obj_dict

filename = 'C:\\Users\\joshua.chik\\fsw_project\\test2.json'

os.makedirs(os.path.dirname(filename), exist_ok=True)

with open(filename, 'w') as file:
    json.dump(settings_dictionary, file, indent=4)