#! /usr/bin/env python
# -*- coding:utf-8 -*-

from status import Status
from send import Send

import schedule
import time
import serial

import json
import os

CONFIG = os.path.dirname(os.path.realpath(__file__)) + '/config.json'

with open(CONFIG) as file:
    json_data = json.load(file)

def job():
    status.run()
    send.send_string(status.status)


if __name__ == "__main__":

    status = Status(json_data["url"], json_data["groups"]["groups_num"])
    send = Send(json_data["serial"]["interface"], json_data["serial"]["baud_rate"])
#
    schedule.every(1).seconds.do(job)
    while 1:
        schedule.run_pending()
        time.sleep(1)

    send.close()
