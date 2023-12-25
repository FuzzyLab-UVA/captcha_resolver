from selenium import webdriver
from selenium.webdriver.common.by import By  
import time
import os


pasta_screenshots = './data'

driver = webdriver.Chrome()

driver.get('https://breachforums.is/member?action=login')

time.sleep(10)

num_screenshots = 1000

for i in range(num_screenshots):
    captcha_img = driver.find_element(By.ID, 'captcha_img')

    nome_arquivo = os.path.join(pasta_screenshots, f'captcha_screenshot_{i+1}.png')
    
    captcha_img.screenshot(nome_arquivo)

    driver.refresh()

    time.sleep(10)

driver.quit()
