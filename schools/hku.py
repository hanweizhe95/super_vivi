from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def safe_click_radio(driver, element_id):
    """Safely click a radio button by scrolling to it and using JavaScript click"""
    element = driver.find_element(By.ID, element_id)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    # Use JavaScript click to bypass interception
    driver.execute_script("arguments[0].click();", element)

def hku(student, school):
    # 初始化浏览器（确保你电脑有 Chrome）
    options = Options()
    options.binary_location = "/usr/bin/chromium-browser"

    driver = webdriver.Chrome(
        options=options
    )

    # 打开港大登录页面
    driver.get("https://sweb.hku.hk/tola/servlet/CreateUserScreen/loginForm")

    # 1. login page======================================================================
    # 1.1 找到账号密码框并输入 (根据页面源码，账号name通常是username，密码是password)
    driver.find_element(By.NAME, "pUSERNAME").send_keys(school['username'])
    driver.find_element(By.NAME, "pPASSWORD").send_keys(school['password'])

    # 1.2 点击登录按钮 (这里使用按钮的名称或类型定位)
    login_btn = driver.find_element(By.ID, "btn-login")
    login_btn.click()

    wait = WebDriverWait(driver, 10)

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
    dropdown_element = wait.until(EC.presence_of_element_located((By.ID, "pTITLE")))
    
    # 2. personal info page==============================================================
    # 2.1 input title
    dropdown_title = Select(driver.find_element(By.ID, "pTITLE"))
    dropdown_sex = Select(driver.find_element(By.ID, "pSEX"))
    if student['sex'] == "Male":
        # 选择值为 "Mr."
        dropdown_title.select_by_value("Mr.")
        dropdown_sex.select_by_value("M")
    else:
        # 选择值为 "Miss"
        dropdown_title.select_by_value("Miss")
        dropdown_sex.select_by_value("F")

    # 2.2 input name
    surname_input = driver.find_element(By.NAME, "pSURNAME")
    surname_input.clear()
    surname_input.send_keys(student['name']['surname'])
    first_name_input = driver.find_element(By.NAME, "pFIRST_NAME")
    first_name_input.clear()
    first_name_input.send_keys(student['name']['first_name'])

    # 2.3 input birth date
    birth_date_input = driver.find_element(By.ID, "pBIRTH_DATE")
    birth = f"{student['birthday']['month']:02d}-{student['birthday']['date']:02d}-{student['birthday']['year']}"
    birth_date_input.send_keys(birth)
    
    # 2.4 input id
    id_input = driver.find_element(By.ID, "pPASSPORT_NUM")
    id_input.clear()
    id_input.send_keys(student['id']['passport'])
    dropdown_passport_country = Select(driver.find_element(By.ID, "pPASSPORT_COUNTRY_CODE"))
    dropdown_passport_country.select_by_value("07")  # 选择值为 "China"

    # 2.5 input citizenship
    dropdown_citizenship = Select(driver.find_element(By.ID, "pCOUNTRY_CODE"))
    dropdown_citizenship.select_by_value("07")  # 选择值为 "China"

    # 2.6 input address
    address_input_1 = driver.find_element(By.NAME, "pADDRESS_CORR_1")
    address_input_1.clear()
    address_input_1.send_keys(student['address']['line1'])
    address_input_2 = driver.find_element(By.NAME, "pADDRESS_CORR_2")
    address_input_2.clear()
    address_input_2.send_keys(student['address']['line2'])
    address_input_3 = driver.find_element(By.NAME, "pADDRESS_CORR_3")
    address_input_3.clear()
    address_input_3.send_keys(student['address']['line3'])

    # 2.6 input email
    email_input = driver.find_element(By.NAME, "pEMAIL")
    email_input.clear()
    email_input.send_keys(student['email'])

    # 2.7 input visa, disablitiy and previous
    safe_click_radio(driver, "pSTUDENT_VISA_N")
    safe_click_radio(driver, "pDISABILITY_N")
    safe_click_radio(driver, "previous_N")

    # 2.9 submit
    personal_submit_btn = driver.find_element(By.ID, "personalSubmitBtn")
    personal_submit_btn.click()

    input("登录成功了吗？按回车键关闭浏览器...")
    driver.quit()