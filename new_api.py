from flask import Flask, request, jsonify, make_response

import logging
import urllib.request, urllib.error, urllib.parse
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
import re
import datetime
today = datetime.date.today()
from datetime import date
from time import strptime
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route("/get-status/<service_tag>")
def get_status(service_tag):
    device_data = {}
    tag_number = service_tag

    LOGGER.setLevel(logging.WARNING)
    # Initialize chrome driver
    chromeOptions = Options()
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--disable-dev-shm-usage')
    chromeOptions.add_argument('--headless')

    warranty_list = {}
    result = []

    PATTERN = r"\s+\d{2}\s+\w{3}\s+20(20|21|22|23)"
    DATA_PATTERN_MICROCODE = re.compile(PATTERN)

    NAME_OF_SUT = r"PowerEdge\s\S+"
    DATA_PATTERN_SUT = re.compile(PATTERN)

    print(tag_number)
    LOGGER.setLevel(logging.WARNING)
    url = "https://www.dell.com/support/home/en-in/product-support/servicetag/{}".format(tag_number)
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(7)
    driver.get(url)

    js_script = driver.execute_script("return document.documentElement.innerHTML;")
    time.sleep(2)
    matches = DATA_PATTERN_MICROCODE.search(js_script)
    #print(matches)
    war_date = matches.group()
    war_date_list = war_date.split()
    month_in_number = strptime('{}'.format(war_date_list[1]),'%b').tm_mon
    someday = date(int(war_date_list[-1]), int(month_in_number), int(war_date_list[0]))
    Day_Remaining = someday - today
    Day_Remaining = Day_Remaining.days
    device_data["tag"] = tag_number
    device_data["rem_days"] = Day_Remaining

    driver.close()
    time.sleep(4)
    driver.quit()
    time.sleep(4)

    res = make_response(jsonify(device_data), 200)
    res.headers['Access-Control-Allow-Origin'] = "*"
    return res

if __name__ == "__main__":
    app.run(debug=True)