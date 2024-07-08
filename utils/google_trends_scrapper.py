from pytrends.request import TrendReq
import pandas as pd
from selenium import webdriver
import time

def get_cookie():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://trends.google.com/")
    time.sleep(5)
    cookie = driver.get_cookie("NID")["value"]
    driver.quit()
    return cookie

# Initialize pytrends request
def get_pytrends_request():
    nid_cookie = f"NID={get_cookie()}"
    pytrends = TrendReq(hl='en-US', tz=360, requests_args={"headers": {"Cookie": nid_cookie}})
    return pytrends 

def build_pytrends_payload(pytrends,keyword):
     pytrends.build_payload([keyword], cat=0, timeframe='2020-01-01 2024-01-01', geo='', gprop='')

def get_pytrends_request(keywords,timeframe_string = '2020-01-01 2024-01-01'):
    pytrends = get_pytrends_request()     

    pytrends.build_payload([keywords], cat=0, timeframe= timeframe_string, geo='', gprop='')

    return pytrends
