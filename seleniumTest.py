from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


chrome_options = Options()

chrome_options.headless = True
headlesss_driver = webdriver.Chrome(executable_path="/Users/SSalu/Downloads/chromedriver", options=chrome_options)

driver = webdriver.Chrome(executable_path="/Users/SSalu/Downloads/chromedriver")
start_url ="https://design.itreetools.org/"

driver.get(start_url)

WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="contentFrame"]')))
ADDRESS_TEXT_BOX = driver.find_element(By.CSS_SELECTOR, "#Address")
ADDRESS_TEXT_BOX.send_keys("10 W 35th St, Chicago, IL 60616")



# push getting started button 
# driver.find_element(By.ID, "get-started").click()

driver.find_element(By.ID, "get-started").click()

a = ActionChains(driver)

time.sleep(3)

QUESTION_BUTTON = driver.find_element(By.ID ,"info_radioHouseNo")
QUESTION_BUTTON.click()

time.sleep(3)

TREE_TEXT_BOX = driver.find_element(By.CSS_SELECTOR, "#info_TreeSpecies_Div > div.search-box-wrap > input")
TREE_TEXT_BOX.send_keys("French plantain")



#dropDown = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.ID,"li-selected")))
#time.sleep(1)
#dropDown.click()

#Click first element in dropdown
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='French plantain']"))).click()





#DPM = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#info_TreeSpecies_Div > div.search-box-wrap > ul" )))
#DROP_DOWN_MENU = driver.find_element(By.CSS_SELECTOR, "#info_TreeSpecies_Div > div.search-box-wrap > ul")
#a.move_to_element(DROP_DOWN_MENU)
#a.perform()
#DPM.click()

time.sleep(1)

#Enter tree diameter
TREE_DIAMETER = driver.find_element(By.CSS_SELECTOR, "#info_TreeDBHinch")
TREE_DIAMETER.send_keys("17")


#drag and drop tree on map
dragDrop = driver.find_element(By.ID ,"info_treeImage3")
dragDrop.click()

time.sleep(1)

placeStart = driver.find_element(By.ID ,"info_ToggleZoom")
placeStart.click()

placeEnd = driver.find_element(By.ID ,"info_btnNewTreeOK")
placeEnd.click()
time.sleep(6)

#Go to benefits page

height = driver.execute_script("return document.documentElement.scrollHeight")
driver.execute_script("window.scrollTo(0, " + str(height) + ");")
time.sleep(1)
benefitsPage = driver.find_element(By.ID ,"info_calcSectionHeader")
benefitsPage.click()

#Add age and calculate
TREE_DIAMETER = driver.find_element(By.ID, "info_GrowoutYears")
TREE_DIAMETER.send_keys("60")

time.sleep(1)
driver.find_element(By.ID, "info_Calculate").click()
time.sleep(50)

#Get info from calculations

#carbon from this year
poundsYear1 = 170
storedYear1 = 3500
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "rslt_tabCO2"))).click()
COamt = driver.find_element(By.ID,"rslt_co2ThisTree")
COYO = COamt.text
funFactsYO = driver.find_element(By.XPATH,"/html/body/div[6]/div/div[8]/table/tbody/tr/td[2]/div/span[2]")
FFYO = funFactsYO.text
array1 = COYO.split(" ")

#parse text
for i in range(len(array1)):
    if array1[i]=="by":
        poundsYear1 = array1[i+1]
    if array1[i]=="stored":
        storedYear1 = array1[i+1]

#carbon from after 60 years
totalSeqest = 20000
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "rslt_tabLeft3"))).click()
COamt = driver.find_element(By.ID,"rslt_co2ThisTree")
COYS = COamt.text
funFactsYS = driver.find_element(By.XPATH,"/html/body/div[6]/div/div[8]/table/tbody/tr/td[2]/div/span[2]")
FFYS = funFactsYS.text
array2 = COYS.split(" ")

#parse text
totalSeqest = array2[len(array2)-2]


# driver.quit()