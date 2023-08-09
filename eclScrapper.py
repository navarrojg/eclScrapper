from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.print_page_options import PrintOptions
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os
import sys

# backup_folder = 'xxx'
backup_folder = 'xxx'
ecl_default_name = 'Euroclear Bank securities search - Euroclear.pdf'
chrome_driver_loc = 'xxx'
user_login = 'login'
user_password = 'password'
unix_time = int(time.time())

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument('window-size=1920x1080')
options.add_argument("--start-maximized")

settings = {
    "recentDestinations" : [{
        "id": "Save as PDF",
        "origin": "local",
        "account" : ""
    }],
    "selectedDestinationId" : "Save as PDF",
    "version" : 2
}

prefs = {'printing.print_preview_sticky_settings.appState' : json.dumps(settings),
        'savefile.default_directory' : backup_folder}

options.add_experimental_option('prefs', prefs)
options.add_argument('--kiosk-printing')
options.page_load_strategy = 'eager'

list_of_isins = []

isin=1
while isin:
    isin = input('Please provide ISIN: ')
    isin = isin.strip()
    if len(isin) == 12 and isin[0:2].isalpha():
        list_of_isins.append(isin)
    elif len(isin) > 1 and len(isin) < 12:
        print('Too little charactes! Isin needs to have 12 characters!')
        continue
    elif len(isin) > 12 :
        print('Too many characters! Isin needs to have 12 characters!')
        continue
    elif not isin[0:2].isalpha() and len(isin)==12:
        print('First two characters of isin have to be alfas!')
        continue

print('GO GO PYTHON SCRIPT!!!')
# print('przed usunieciem duplikatow: ')
# print(list_of_isins)

list_of_isins = list(set(list_of_isins))

# print('po usunieciu duplikaow: ')
# print(list_of_isins)
# isin = 'xs2434407420'
# print(list_of_isins[0])

# list_of_isins = ['xs2434407420','XS2520969143','XS2521681093', 'XS2520363263']

len_list_of_isins = len(list_of_isins)

if len_list_of_isins < 1:
    print('Nie podałeś żadnego poprawnego ISINA :( Narka')
    time.sleep(3)
    sys.exit("You didn't provide any valid ISIN :( See You Later, Aligator!")
    
driver = webdriver.Chrome(chrome_driver_loc, chrome_options=options)

# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.implicitly_wait(10)

driver.get('https://my.euroclearr.com/users/en/login.html')
driver.find_element('xpath','//*[@id="js-modal-content"]/div[1]/div[3]/div/div[1]/button').click()
username = driver.find_element('xpath', '//*[@id="username"]')
password = driver.find_element('xpath', '//*[@id="password"]')
username.send_keys(user_login)
password.send_keys(user_password)
driver.find_element('xpath', '//*[@id="login"]/div[3]/div/button').click()

# inside ecl
# more than one isin
if len_list_of_isins > 1:
    driver.find_element('xpath','//*[@id="js-modal-page"]/div[3]/main/div[2]/div/div/div[2]').click()
    isins = driver.find_element(by=By.ID, value='globalsearch')
    isins.send_keys(list_of_isins.pop(0))
    driver.find_element('xpath', '//*[@id="globalsearch__wrapper"]/button') .click()
    # print(list_of_isins)
    # time.sleep(2)
    driver.find_element('xpath','//*[@id="new_form_modifier_q_chzn"]/a') .click()
    driver.find_element('xpath','//*[@id="new_form_modifier_q_chzn"]/a') .click()
    # time.sleep(8)

    while len(list_of_isins) > 0:
        search_field = driver.find_element('xpath', "//div[@id='q_select_chzn']/ul/li[@class='search-field']/input") 
        search_field.send_keys(list_of_isins.pop(0))
        # time.sleep(1) TEST!!!!!!!!! <-------
        
    # search_button = driver.find_element('xpath','//*[@id="leftcol"]/div/div[3]/div[2]/button') 
    # search_button.location_once_scrolled_into_view
    # search_button.click()
    
    driver.find_element('xpath','//*[@id="leftcol"]/div/div[3]/div[2]/button') .click()

    # time.sleep(15)
    # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='results']/tbody/tr[2]")))
    try:
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='textimage-box-textimage_412']/div[1]/div/p")))
    except:
            driver.save_screenshot(f'{backup_folder}\\notFound__{unix_time}.png')
            driver.quit()
            sys.exit('Nothing has been found. The script has finished.')


    # time.sleep(10)
    # el = driver.find_element('xpath', '//*[@id="textimage-box-textimage_6033"]/div[1]/div/p')
    # driver.execute_script("return arguments[0].scrollIntoView(true);", el)
    # driver.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + Keys.HOME)
    # driver.execute_script("window.scrollTo(0,0)")
    # driver.execute_script("window.scroll(0, 0);")
    # el = driver.find_element('xpath','//*[@id="textimage-box-textimage_6033"]/div[1]')
    # el.location_once_scrolled_into_view
    # el.click()
    # el.click()

    z=0
    for i in range(len_list_of_isins):
        z+=1
        try:
            element = driver.find_element('xpath','//*[@id="results"]/tbody/tr[{}]/td[2]/a'.format(z))
            element.location_once_scrolled_into_view
            try:
                # print(z)
                element.click()
            except:
                try:
                    # print(z)
                    z+=1
                    # print(z)
                    element = driver.find_element('xpath','//*[@id="results"]/tbody/tr[{}]/td[2]/a'.format(z))
                    element.location_once_scrolled_into_view
                    element.click()
                except:
                    # print(z)
                    z+=1
                    # print(z)
                    element = driver.find_element('xpath','//*[@id="results"]/tbody/tr[{}]/td[2]/a'.format(z))
                    element.location_once_scrolled_into_view
                    element.click()

            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='tabs-1']/div[1]/dl[1]/dt[5]")))
            isin_name = driver.find_element('xpath','//*[@id="tabs-1"]/div[1]/dl[1]/dd[5]').get_attribute('textContent')
            #.format(z) powyzej
            # print(isin_name)
            driver.execute_script("window.print();")
            time.sleep(3)
            #changing file name
            try:
                isFile = os.path.isfile(f'{backup_folder}\\{isin_name}.pdf')
                # print(isFile) 
                if isFile:
                    old_name = f'{backup_folder}\\{ecl_default_name}' 
                    new_name = f'{backup_folder}\\{isin_name}___ECL___{unix_time}.pdf' 
                    os.rename(old_name, new_name)
                else:
                    old_name = f'{backup_folder}\\{ecl_default_name}' 
                    new_name = f'{backup_folder}\\{isin_name}.pdf' 
                    os.rename(old_name, new_name)
            except:
                pass
            
            # time.sleep(2)
            driver.back()
            # time.sleep(5)        
        except:
            driver.save_screenshot(f'{backup_folder}\\notFound__{unix_time}.png')
            driver.quit()
            sys.exit('THE END')


# just one isin
if len_list_of_isins == 1:
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='js-modal-page']/div[3]/main/div[2]/div/div/div[2]"))).click()
    driver.find_element('xpath','//*[@id="js-modal-page"]/div[3]/main/div[2]/div/div/div[2]').click()
    # driver.find_element('xpath',"//div[@class='search-tabs__tab'][1]").click()

    isins = driver.find_element(by=By.ID, value='globalsearch')
    isins.send_keys(list_of_isins[0])
    driver.find_element('xpath', '//*[@id="globalsearch__wrapper"]/button') .click()
    # time.sleep(7)
    try:
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='results']/tbody/tr")))
        driver.find_element('xpath','//*[@id="results"]/tbody/tr/td[2]/a') .click()
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='tabs-1']/div[1]/dl[1]/dt[1]")))
        #save to pdf
        # time.sleep(7)
        driver.execute_script("window.print();")

        #changing file name
        time.sleep(2)
        isFile = os.path.isfile(f'{backup_folder}\\{list_of_isins[0]}.pdf')
        print(isFile) 
        if isFile:
            old_name = f'{backup_folder}\\{ecl_default_name}'
            new_name = f'{backup_folder}\\{list_of_isins[0]}___ECL___{unix_time}.pdf' 
            os.rename(old_name, new_name)
        else:
            old_name = f'{backup_folder}\\{ecl_default_name}' 
            new_name = f'{backup_folder}\\{list_of_isins[0]}.pdf' 
            os.rename(old_name, new_name)
        # time.sleep(1)
        driver.quit()

    except:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='error']")))
        # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='textimage-box-textimage']/div[1]/div/p[1]")))
        isFile = os.path.isfile(f'{backup_folder}\\{list_of_isins[0]}.png')
        if not isFile:
            driver.save_screenshot(f'{backup_folder}\\{list_of_isins[0]}.png')
        else:
            driver.save_screenshot(f'{backup_folder}\\{list_of_isins[0]}___ECL___{unix_time}.png')
        driver.quit()
else:
       driver.quit()