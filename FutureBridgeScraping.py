from bs4 import BeautifulSoup
import requests
import shutil
from selenium import webdriver
from openpyxl import Workbook
import time

# Science Daily Starts

def scrapeData2(pageCount,maxPage,OutputFile,ImagePrefix):
        print('Execution Started')
        book=Workbook()
        sheet=book.active
        driver = webdriver.Chrome('./chromedriver')
        global counter
        counter = 0
        while pageCount<=maxPage:
                driver.get('https://www.sciencedaily.com/search/?keyword=mobile#gsc.tab=0&gsc.q=mobile&gsc.page='+str(pageCount))
                time.sleep(3)
                resTitle=driver.execute_script("return document.querySelectorAll('a[class=""gs-title""]')")
                #resSummary=driver.execute_script("return document.getElementsByClassName('gs-snippet')")
                counter=0
                for data in resTitle:
                        title=data.text
                        titleLink=data.get_attribute('href')
                        if counter % 2==0:
                                if titleLink!='':
                                        Summary,Date,Source=getPageData2(titleLink)
                                        sheet.append((title,titleLink,Summary,Date,Source))
                        counter=counter+1
                pageCount=pageCount+1
                driver.quit()

        book.save(OutputFile)
        print('Execution Ends')

def getPageData2(link):
        try:
                driver = webdriver.Chrome('./chromedriver')
                driver.get(link)
                time.sleep(3)
                resDate=driver.execute_script("return document.getElementById('date_posted')")
                resSummary=driver.execute_script("return document.getElementById('abstract')")
                resSource=driver.execute_script("return document.getElementById('source')")
                summary=resSummary.text
                date=resDate.text
                source=resSource.text
                driver.quit()
                return summary,date,source
        except:
                driver.quit()
                return ' ',' ',' '

# Science Daily Ends



# Fuel Cell Scraping Starts

def scrapeData1(pageCount,maxPage,OutputFile,ImagePrefix):
        print('Execution Started')
        book=Workbook()
        sheet=book.active
        driver = webdriver.Chrome('./chromedriver')
        global counter
        counter = 0
        while pageCount<=maxPage:
                driver.get('https://fuelcellsworks.com/news/page/'+str(pageCount))
                time.sleep(5)
                resDate=driver.execute_script("return document.getElementsByClassName('date')")
                resTitle=driver.execute_script("return document.getElementsByClassName('title')")
                resTitleLink=driver.execute_script("return document.querySelectorAll('h2[class=""title""] a')")
                #resSummary=driver.execute_script("return document.querySelectorAll('div[class=""article-content-wrap""] p')")
                resImages=driver.execute_script("return document.querySelectorAll('span[class=""post-featured-img""] img')")
                counter=0
                for data in resDate:
                        date=data.text
                        title=resTitle[counter].text
                        titleLink=resTitleLink[counter].get_attribute('href')
                        summaryData=getPageData1(titleLink)
                        #print(resSummary.length)
                        #Summary=resSummary[counter].text
                        Images=resImages[counter].get_attribute('src')
                        #urllib.request.urlretrieve(Images,'Images/Image'+str(counter)+'.jpg')
                        r = requests.get(Images, stream=True)
                        if r.status_code == 200:
                            with open('Images/'+ImagePrefix+str(time.time())+'.jpg', 'wb') as f:
                                r.raw.decode_content = True
                                shutil.copyfileobj(r.raw, f)
                        sheet.append((date,title,titleLink,summaryData,'Images/'+ImagePrefix+str(time.time())+'.jpg'))
                        counter=counter+1
                driver.quit()
                pageCount=pageCount+1

        book.save(OutputFile)
        print('Execution Ends')

def getPageData1(link):
        driver = webdriver.Chrome('./chromedriver')
        driver.get(link)
        time.sleep(5)
        resSummary=driver.execute_script("return document.getElementsByClassName('content-inner')")
        summary=resSummary[0].text
        driver.quit()
        return summary

# Fuel Cell Scraping Ends
