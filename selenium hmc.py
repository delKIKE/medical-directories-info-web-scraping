from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

## what this file will do is use selenium to extract all the info from the
##hmc website after javascript loads. It worked successfully so now the file is saved
##Thus, you can now extract the doctors' list with code

driver = webdriver.Chrome()
driver.get("https://hmc.com.hn/directory")

time.sleep(5)

WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
)

print(driver.page_source)

with open("C:/Users/adane/Documents/hmc_page.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)


print("file was successfully saved")

driver.quit()

