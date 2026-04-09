from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def cityu(student, school):
    # 初始化浏览器（确保你电脑有 Chrome）
    options = Options()
    # options.binary_location = "/usr/bin/chromium-browser"

    driver = webdriver.Chrome(
        options=options
    )

    # 打开城大登录页面
    driver.get("https://banweb.cityu.edu.hk/pls/PROD/hwskalog_cityu.P_DispLoginNon")
    
    # 1. login page======================================================================
    # 1.1 找到账号密码框并输入 (根据页面源码，账号name通常是username，密码是password)
    driver.find_element(By.NAME, "id").send_keys(school['username'])
    driver.find_element(By.NAME, "pin").send_keys(school['password'])

    # 1.2 点击登录按钮 (这里使用按钮的名称或类型定位)
    login_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    login_btn.click()

    wait = WebDriverWait(driver, 10)

    input("登录成功了吗？按回车键关闭浏览器...")
    driver.quit()