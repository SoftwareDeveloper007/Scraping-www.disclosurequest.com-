from urllib import *
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from dateutil.relativedelta import *
import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time, re, collections, shutil, os, sys, zipfile, xlrd, threading, csv, openpyxl, math

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
        print logTxt + '\n'

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
        self.total_urls = []
        self.total_links_cnt = 0
        self.total_data = []
        self.log_printer = log_printer()
        self.save_flag = True

        self.links_file_name = "Result/all_links.xlsx"
        self.dest = "Result"
        if not os.path.exists(self.dest):
            os.makedirs(self.dest)

    def getTotalURLs(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active

        url = self.start_url.format(1)
        html = download(url)
        soup = BeautifulSoup(html, "html.parser")

        page_disp = soup.select_one("div.pagination > p").text.split(" ")[3]
        self.total_page_num = int(page_disp)
        self.pages = []
        for i in range(self.total_page_num):
            self.pages.append(i+1)
        self.pages.reverse()

        self.threads = []
        self.max_threads = 100

        while self.threads or self.pages:
            for thread in self.threads:
                if not thread.is_alive():
                    self.threads.remove(thread)

            while len(self.threads) < self.max_threads and self.pages:
                thread = threading.Thread(target=self.getOneURL)
                thread.setDaemon(True)
                thread.start()
                self.threads.append(thread)

        # self.saveXLSX()

    def getOneURL(self):
        page = self.pages.pop()

        url = self.start_url.format(page)
        html = download(url)
        soup = BeautifulSoup(html, "html.parser")
        details = soup.select("tr.detail")
        summaries = soup.select("tr.summary")


        for j, (detail, summary) in enumerate(zip(details, summaries)):

            company = summary.select("td")[0].text
            link = detail.select("div > span > a")[1].get("href")
            link = urlparse.urljoin(self.base_url, link)
            self.total_links_cnt += 1

            # if self.total_links_cnt % 20000 == 0 and self.total_links_cnt > 0:
            #     self.saveXLSX()

            # if len(self.total_data) > 50000 and self.save_flag:
            #     self.saveXLSX()

            self.total_data.append([company, link, self.total_links_cnt, j+1, page, self.total_page_num])

            logTxt = "Company:\t{}\nLink:\t\t{}\nIndex:\t\t{}\nnRow:\t\t{}\nPage:\t\t{} of {}\n".format(company, link, self.total_links_cnt, j+1, page, self.total_page_num)


            self.log_printer.print_log(logTxt)

    def saveXLSX(self):
        self.save_flag = False
        # while self.total_data:
        # self.total_data.sort(takeFourth)
        # for i in range(50000):
        #     [company, link, index, page, total_page_num] = self.total_data.pop()
        for i, line in enumerate(self.total_data):
            [company, link, index, nrow, page, total_page_num] = line
            self.ws.cell(row=index, column=1).value = company
            self.ws.cell(row=index, column=2).value = link
            self.ws.cell(row=index, column=3).value = nrow
            self.ws.cell(row=index, column=4).value = page
            self.ws.cell(row=index, column=5).value = total_page_num

        self.wb.save(self.links_file_name)

        logTxt = "\tSaved data successfully!!!"
        self.log_printer.print_log(logTxt)
        self.save_flag = True

if __name__ == '__main__':
    start_t = time.time()
    app = mainScraper()
    app.getTotalURLs()
    app.saveXLSX()

    print(time.time() - start_t)