from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

# 1. 初始化浏览器（确保你电脑有 Chrome）
driver = webdriver.Chrome()

# 2. 打开港大登录页面
driver.get("https://sweb.hku.hk/tola/servlet/CreateUserScreen/loginForm")

# 3. 找到账号密码框并输入 (根据页面源码，账号name通常是username，密码是password)
# .send_keys() 就是模拟打字
driver.find_element(By.NAME, "pUSERNAME").send_keys("testacc")
driver.find_element(By.NAME, "pPASSWORD").send_keys("Offer2026")

# 4. 点击登录按钮 (这里使用按钮的名称或类型定位)
login_btn = driver.find_element(By.ID, "btn-login")
login_btn.click()

wait = WebDriverWait(driver, 10)

wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "pTITLE")))
# input title
dropdown = Select(driver.find_element(By.ID, "pTITLE"))
# 选择值为 "Mr."
dropdown.select_by_value("Mr.")

# 5. input name
surname_input = driver.find_element(By.NAME, "pSURNAME")
surname_input.clear()
surname_input.send_keys("Zhang")
first_name_input = driver.find_element(By.NAME, "pFIRST_NAME")
first_name_input.clear()
first_name_input.send_keys("San")

# 5. 暂停一下，让你看看结果，而不是直接关闭
input("登录成功了吗？按回车键关闭浏览器...")
driver.quit()