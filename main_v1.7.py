from urllib import *
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
import urllib.request
import requests
from io import BytesIO
from urllib.parse import urljoin

from bs4 import BeautifulSoup
# from lxml import html
from datetime import date, datetime, timedelta
# from dateutil.relativedelta import *
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options

# import time, re, collections, shutil, os, sys, zipfile, xlrd, threading, csv, openpyxl, math
import pymysql, time, os, threading, csv


def takeFourth(elem):
    return elem[4]


class log_printer():
    def __init__(self):
        curDate = datetime.now()
        curDateStr = "{:4d}_{:02d}_{:02d}_{:02d}_{:02d}_{:02d}".format(curDate.year, curDate.month, curDate.day,
                                                                       curDate.hour, curDate.minute, curDate.second)
        self.logFile = open("Log_File_" + curDateStr + ".txt", "w+")

    def print_log(self, logTxt):
        try:
            self.logFile.write(logTxt + '\n')
            self.logFile.flush()
        except:
            pass
        print(logTxt + '\n')

    def close_log(self):
        self.logFile.close()


def download(url, num_retries=3):
    """Download function that also retries 5XX errors"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        # headers = {'User-agent': 'your bot 0.1'}
        result = requests.get(url, headers=headers, stream=True)
        html = result.content.decode()

    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download(url, num_retries - 1)
    except:
        html = None
    return html


class mainScraper():
    def __init__(self):
        self.base_url = "https://www.disclosurequest.com/"
        self.start_url = "https://www.disclosurequest.com/results?sortColumn=&sortDirection=&searchBox=&amountToBeRaisedMin=&amountToBeRaisedMax=&filingDateMin=&filingDateMax=&cikNumber=&page={}"
        self.csv_url = "/results/csv?sortColumn=&sortDirection=&searchBox=&amountToBeRaisedMin=&amountToBeRaisedMax=&filingDateMin=&filingDateMax=&cikNumber=&page={}"
        self.total_data = []
        self.log_printer = log_printer()
        self.save_flag = True

        self.sub_csv_name = "Result/data_{:05d}.csv"
        self.total_csv_name = "total.csv"
        self.dest = "Result"
        if not os.path.exists(self.dest):
            os.makedirs(self.dest)

    def totalDownloadCSV(self):
        url = self.start_url.format(1)
        html = download(url)
        soup = BeautifulSoup(html, "html.parser")

        page_disp = soup.select_one("div.pagination > p").text.split(" ")[3]
        self.total_page_num = int(page_disp)
        self.pages = []
        for i in range(self.total_page_num):
            url = urljoin(self.base_url, self.csv_url.format(i + 1))
            self.pages.append([i + 1, url])
        self.pages.reverse()

        self.threads = []
        self.max_threads = 10

        while self.threads or self.pages:
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)

            while len(self.threads) < self.max_threads and self.pages:
                thread = threading.Thread(target=self.downloadOneURL)
                thread.setDaemon(True)
                thread.start()
                self.threads.append(thread)

    def downloadOneURL(self):
        index, url = self.pages.pop()

        r2 = requests.get(url)

        csv_name = self.sub_csv_name.format(index)
        with open(csv_name, "wb") as f:
            f.write(r2.content)

        logTxt = "Page {:05d} downloaded successfully!".format(index)
        self.log_printer.print_log(logTxt)

    def mergeCSV(self):
        logTxt = "Merging all csv files..."
        print(logTxt)
        self.header = ["Accession Number", "Amount To Be Raised", "CIK Number", "City", "Company Name",
                       "Federel Exemptions/Exlcusions",
                       "Filing Date", "Filing Type", "Industry Group", "Industry Group Code", "Amendment",
                       "Principal Place of Business",
                       "Principal Place of Business Code", "HTML Link", "Revenue or Assets", "State of Jurisdiction",
                       "State of Jurisdiction Code", "Street 1", "Street 2", "Tier", "Type of Security",
                       "Type of Security Description",
                       "Zip Code", "Associated Auditor", "Associated Auditor Fee", "Associated Legal Service",
                       "Associated Legal Service Fee",
                       "Associated Promotor", "Associated Promotor Fee", "Associated Sales Commission",
                       "Associated Sales Commission Fee"]

        total_file = open(self.total_csv_name, 'w', encoding='utf-8', newline='')
        writer = csv.writer(total_file)
        writer.writerow(self.header)

        for (path, dirs, files) in os.walk(os.getcwd() + "/Result"):
            for file in files:
                in_file = open(path + '/' + file, 'r', encoding="utf8")
                print(file)
                reader = csv.reader(in_file)
                for i, row in enumerate(reader):
                    if i == 0:
                        continue
                    for j, col in enumerate(row):
                        row[j] = row[j].replace('"', '')
                    writer.writerow(row)
                    self.total_data.append(row)

        total_file.close()
        self.total_data.reverse()

        logTxt = "Merged successfully."
        print(logTxt)

    def saveDatabase(self):

        logTxt = "Saving data into mySQL..."
        print(logTxt)

        # DB_HOST = '159.65.234.92'
        DB_HOST = 'localhost'
        DB_USER = 'root'
        DB_PASSWORD = 'bluedream'
        DB_NAME = 'gallery'

        self.db = pymysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        logTxt = "Connected to the database successfully"
        print(logTxt)

        # prepare a cursor object using cursor() method
        self.cur = self.db.cursor()

        sql = "DROP TABLE IF EXISTS Total_first"
        self.cur.execute(sql)
        sql = "CREATE TABLE IF NOT EXISTS Total_first(ID INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL, Accession_Number VARCHAR(255), " \
              "Amount_To_Be_Raised VARCHAR(255), CIK_Number VARCHAR(255), City VARCHAR(255), Company_Name VARCHAR(255), " \
              "Federel_Exemptions_Exlcusions  VARCHAR(255), Filing_Date VARCHAR(255), Filing_Type  VARCHAR(255), " \
              "Industry_Group VARCHAR(255), Industry_Group_Code VARCHAR(255), Amendment VARCHAR(255), " \
              "Principal_Place_of_Business VARCHAR(255), Principal_Place_of_Business_Code VARCHAR(255), " \
              "HTML_Link VARCHAR(255), Revenue_or_Assets VARCHAR(255), State_of_Jurisdiction VARCHAR(255), " \
              "State_of_Jurisdiction_Code VARCHAR(255), Street_1 VARCHAR(255), Street_2 VARCHAR(255), Tier VARCHAR(255), " \
              "Type_of_Security VARCHAR(255), Type_of_Security_Description VARCHAR(255), Zip_Code VARCHAR(255), " \
              "Associated_Auditor VARCHAR(255), Associated_Auditor_Fee VARCHAR(255), Associated_Legal_Service VARCHAR(255), " \
              "Associated_Legal_Service_Fee VARCHAR(255), Associated_Promotor VARCHAR(255), Associated_Promotor_Fee VARCHAR(255), " \
              "Associated_Sales_Commission VARCHAR(255), Associated_Sales_Commission_Fee VARCHAR(255))"
        self.cur.execute(sql)

        keys = """(Accession_Number, Amount_To_Be_Raised, 
                  CIK_Number, City, Company_Name, Federel_Exemptions_Exlcusions , Filing_Date, 
                  Filing_Type , Industry_Group, Industry_Group_Code, Amendment, Principal_Place_of_Business,
                  Principal_Place_of_Business_Code, HTML_Link, Revenue_or_Assets, State_of_Jurisdiction,
                  State_of_Jurisdiction_Code, Street_1, Street_2, Tier, Type_of_Security, Type_of_Security_Description,
                  Zip_Code, Associated_Auditor, Associated_Auditor_Fee, Associated_Legal_Service, Associated_Legal_Service_Fee,
                  Associated_Promotor, Associated_Promotor_Fee, Associated_Sales_Commission, Associated_Sales_Commission_Fee)"""

        for i, row in enumerate(self.total_data):
            try:
                print(i)
                values = '%s, ' * len(row)
                values = values[:-2]
                query = 'INSERT INTO Total_first ' + keys + ' VALUES(' + values + ');'
                self.cur.execute(query, tuple(row))
                self.db.commit()
            except:
                print(query)

        self.db.close()
        logTxt = "Saved all data in a database successfully."
        print(logTxt)


if __name__ == '__main__':
    start_t = time.time()

    app = mainScraper()
    # app.totalDownloadCSV()
    app.mergeCSV()
    app.saveDatabase()

    print(time.time() - start_t)
