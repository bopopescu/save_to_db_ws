# -*- coding: utf-8 -*-
from datetime import datetime
startTime = datetime.now()

from util.DictionaryUtil import dict2obj
from sys import argv
from service.dbService import *
from service import jsonService

# python main.py "{'ws_id': 1, 'token': 'token', 'time': '2015-08-09 19:23:23', 'measurements': [{'sensor_id':1, 'value':2.55}], 'errors': []}"

try:
    connect_to_database()

    if len(sys.argv) == 2:
        json = sys.argv[1].replace("'", "\"")
        print "Incoming data: "+json
        json_dict = jsonService.is_correct_json(json)
        model = dict2obj(json_dict)
        if check_correct_token(model.ws_id, model.token):
            save_to_database(model)
        else:
            raise Exception("Incorrect token or weather station id")
            exit(1)
    else:
        raise Exception("Wrong number of parameters")
        exit(1)
    disconnect_database()
except Exception, Argument:
    print "Error: "+str(Argument)
    exit(1)

print "Run in "+str(datetime.now() - startTime)+" s"

exit(0)
