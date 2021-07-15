import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# launch url
url = "https://www.pgatour.com/stats/stat.02671.html"
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get(url)

#These selections access each of the drop-down menus on the PGATour Fedex Cup Standings site
#Access the Season drop-down, size does not vary and will be every year since 2007
selection1 = Select(driver.find_element_by_class_name(
    "statistics-details-select.statistics-details-select--season.hasCustomSelect"))
options1 = selection1.options
#Access the Time Period drop-down, size does not vary and should always want the second option
selection2 = Select(driver.find_element_by_class_name(
        "statistics-details-select.statistics-details-select--period.hasCustomSelect"))
options2 = selection2.options
#Access the Tournament drop-down, size varies by season
selection3 = Select(driver.find_element_by_class_name(
        "statistics-details-select.statistics-details-select--tournament.hasCustomSelect"))
options3 = selection3.options
dataColumns = ['RANK THIS WEEK', 'RANK LAST WEEK', 'PLAYER NAME', 'EVENTS', 'POINTS', '# OF WINS','# OF TOP-10S',
           'POINTS BEHIND LEAD', 'RESET POINTS', 'TOURNAMENT NAME', 'WEEK NUMBER']
df1 = pd.DataFrame(columns=dataColumns)
for index in range(0, len(options1)):
    try:
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                                        "statistics-details-select.statistics-details-select--season.hasCustomSelect" ))
        )
        select = Select(driver.find_element_by_class_name(
            "statistics-details-select.statistics-details-select--season.hasCustomSelect"))
        select.select_by_index(index)
        print(str(2021-index))
        time.sleep(10)
    except:
        print("select fuck")
        driver.quit()
    try:
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                                        "statistics-details-select.statistics-details-select--period.hasCustomSelect" ))
        )
        select2 = Select(driver.find_element_by_class_name(
            "statistics-details-select.statistics-details-select--period.hasCustomSelect"))
        select2.select_by_value("eon")
        print("Tournament Only")
        time.sleep(15)
    except:
        print("select 2 fuck")
        driver.quit()
    try:
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,
            "statistics-details-select.statistics-details-select--tournament.hasCustomSelect"))
        )
        select3 = Select(driver.find_element_by_class_name(
            "statistics-details-select.statistics-details-select--tournament.hasCustomSelect"))
        options3 = select3.options
        time.sleep(10)

        #find a list of tournament names in the current year
        tourneyNames = []
        for value in options3:
            tourneyNames.append(value.text)
        print(tourneyNames)
        time.sleep(1)

        #Iterate through all tournaments in the current year
        for index3 in range(0, len(options3)):
            select3 = Select(driver.find_element_by_class_name(
                "statistics-details-select.statistics-details-select--tournament.hasCustomSelect"))
            select3.select_by_index(index3)
            time.sleep(10)
            soup_level1 = BeautifulSoup(driver.page_source, 'lxml')
            rows = soup_level1.find("table", class_='table-styled').find("tbody").find_all("tr")


            #iterate through the tournament results and add each player as a new row of data
            for tr in rows:
                td = tr.find_all("td")
                row = [str(tr.get_text()).strip() for tr in td]
                row.append(tourneyNames[index3])
                row.append(str(len(options3) - index3))

                rowDict = {
                    dataColumns[0]: row[0],
                    dataColumns[1]: row[1],
                    dataColumns[2]: row[2],
                    dataColumns[3]: row[3],
                    dataColumns[4]: row[4],
                    dataColumns[5]: row[5],
                    dataColumns[6]: row[6],
                    dataColumns[7]: row[7],
                    dataColumns[8]: row[8],
                    dataColumns[9]: row[9],
                    dataColumns[10]: row[10]
                }

                df1 = df1.append(rowDict, ignore_index=True)
            print("Tournament " + tourneyNames[index3] + " success.")
        df1.to_csv(r'C:\Users\Matt Hellmann\PycharmProjects\learnPython\Fedex Cup Research.csv')
    except:
        print("select 3 fuck")
        driver.quit()

csv_records = df1.to_csv(r'C:\Users\Matt Hellmann\PycharmProjects\learnPython\ALL Fedex Cup Research.csv', index=False)
driver.quit()
