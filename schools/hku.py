from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

def safe_click_radio(driver, element_id):
    """Safely click a radio button by scrolling to it and using JavaScript click"""
    element = driver.find_element(By.ID, element_id)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    # Use JavaScript click to bypass interception
    driver.execute_script("arguments[0].click();", element)

def hku(student, school):
    # 初始化浏览器（确保你电脑有 Chrome）
    options = Options()
    # options.binary_location = "/usr/bin/chromium-browser"

    driver = webdriver.Chrome(
        options=options
    )

    # 打开港大登录页面
    driver.get("https://sweb.hku.hk/tola/servlet/CreateUserScreen/loginForm")

    # 0. login page======================================================================
    # 0.1 找到账号密码框并输入 (根据页面源码，账号name通常是username，密码是password)
    driver.find_element(By.NAME, "pUSERNAME").send_keys(school['username'])
    driver.find_element(By.NAME, "pPASSWORD").send_keys(school['password'])

    # 0.2 点击登录按钮 (这里使用按钮的名称或类型定位)
    login_btn = driver.find_element(By.ID, "btn-login")
    login_btn.click()

    wait = WebDriverWait(driver, 10)

    wait.until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
    wait.until(EC.presence_of_element_located((By.ID, "pTITLE")))
    
    # 1. personal info page==============================================================
    # 1.1 input title
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

    # 1.2 input name
    surname_input = driver.find_element(By.NAME, "pSURNAME")
    surname_input.clear()
    surname_input.send_keys(student['name']['surname'])
    first_name_input = driver.find_element(By.NAME, "pFIRST_NAME")
    first_name_input.clear()
    first_name_input.send_keys(student['name']['first_name'])

    # 1.3 input birth date
    birth_date_input = driver.find_element(By.ID, "pBIRTH_DATE")
    birth = f"{student['birthday']['month']:02d}-{student['birthday']['date']:02d}-{student['birthday']['year']}"
    birth_date_input.send_keys(birth)
    
    # 1.4 input id
    id_input = driver.find_element(By.ID, "pPASSPORT_NUM")
    id_input.clear()
    id_input.send_keys(student['id']['passport'])
    dropdown_passport_country = Select(driver.find_element(By.ID, "pPASSPORT_COUNTRY_CODE"))
    dropdown_passport_country.select_by_value("07")  # 选择值为 "China"

    # 1.5 input citizenship
    dropdown_citizenship = Select(driver.find_element(By.ID, "pCOUNTRY_CODE"))
    dropdown_citizenship.select_by_value("07")  # 选择值为 "China"

    # 1.6 input address
    address_input_1 = driver.find_element(By.NAME, "pADDRESS_CORR_1")
    address_input_1.clear()
    address_input_1.send_keys(student['address']['line1'])
    address_input_2 = driver.find_element(By.NAME, "pADDRESS_CORR_2")
    address_input_2.clear()
    address_input_2.send_keys(student['address']['line2'])
    address_input_3 = driver.find_element(By.NAME, "pADDRESS_CORR_3")
    address_input_3.clear()
    address_input_3.send_keys(student['address']['line3'])

    # 1.7 input email
    email_input = driver.find_element(By.NAME, "pEMAIL")
    email_input.clear()
    email_input.send_keys(student['email'])

    # 1.8 input visa, disablitiy and previous
    safe_click_radio(driver, "pSTUDENT_VISA_N")
    safe_click_radio(driver, "pDISABILITY_N")
    safe_click_radio(driver, "previous_N")

    time.sleep(1)
    # 1.9 submit
    personal_submit_btn = driver.find_element(By.ID, "personalSubmitBtn")
    personal_submit_btn.click()

    # 2. academic qualifications page ================================================
    time.sleep(1)
    wait = WebDriverWait(driver, 50)
    wait.until(EC.presence_of_element_located((By.ID, "pDEGREEA")))
    for qualification in student['academic_qualifications']:
        if qualification['is_current']:
            dropdown_qualification_a = Select(driver.find_element(By.ID, "pDEGREEA"))
            if qualification['qualification'] == "Bachelor's Degree":
                dropdown_qualification_a.select_by_value("99")
            abbre_a_input = driver.find_element(By.NAME, "pABBREVIATIONA")
            abbre_a_input.clear()
            abbre_a_input.send_keys(qualification['abbreviation'])
            major_a_input = driver.find_element(By.NAME, "pMAJORA")
            major_a_input.clear()
            major_a_input.send_keys(qualification['major'])
            dropdown_mode_of_study_a = Select(driver.find_element(By.NAME, "pPART_TIMEA"))
            if qualification['mode_of_study'] == "full-time":
                dropdown_mode_of_study_a.select_by_value("F")
            else:
                dropdown_mode_of_study_a.select_by_value("P")
            duration_a_input = driver.find_element(By.NAME, "pYEAR_OF_STUDYA")
            duration_a_input.clear()
            duration_a_input.send_keys(qualification['duration'])
            place_a_input = driver.find_element(By.NAME, "pOTHER_AWARD_COUNTRYA")
            place_a_input.clear()
            place_a_input.send_keys(qualification['awarding_place'])
            institution_a_input = driver.find_element(By.NAME, "pOTHER_AWARD_INSTITUTIONA")
            institution_a_input.clear()
            institution_a_input.send_keys(qualification['awarding_institution'])
            present_stage_a_input = driver.find_element(By.NAME, "pSTUDY_STAGEA")
            present_stage_a_input.clear()
            present_stage_a_input.send_keys(qualification['present_stage'])
            date_a_input = driver.find_element(By.NAME, "pAWARD_DATEA")
            date_a_input.clear()
            date_a_input.send_keys(qualification['date_of_award'])
            if qualification['english']:
                safe_click_radio(driver, "pLANGUAGEA_Y")
            else:
                safe_click_radio(driver, "pLANGUAGEA_N")
    time.sleep(1)
    save_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    save_btn.click()

    # 3. professional qualifications page ================================================
    time.sleep(1)
    wait = WebDriverWait(driver, 50)
    wait.until(EC.presence_of_element_located((By.ID, "pMEMBERSHIP1")))
    time.sleep(1)
    save_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    save_btn.click()

    # 4. English language qualifications page ================================================
    time.sleep(1)
    wait = WebDriverWait(driver, 50)
    wait.until(EC.presence_of_element_located((By.NAME, "pMM_IELTS_TS")))
    ielts_mm_input = driver.find_element(By.NAME, "pMM_IELTS_TS")
    ielts_mm_input.clear()
    ielts_mm_input.send_keys(student['IELTS']['MM'])
    ielts_yyyy_input = driver.find_element(By.NAME, "pYYYY_IELTS_TS")
    ielts_yyyy_input.clear()
    ielts_yyyy_input.send_keys(student['IELTS']['YYYY'])
    ielts_id_input = driver.find_element(By.NAME, "pIELTS_ID")
    ielts_id_input.clear()
    ielts_id_input.send_keys(student['IELTS']['ID'])
    ielts_l_input = driver.find_element(By.NAME, "pIELTS_LISTENING")
    ielts_l_input.clear()
    ielts_l_input.send_keys(student['IELTS']['L'])
    ielts_id_input = driver.find_element(By.NAME, "pIELTS_READING")
    ielts_id_input.clear()
    ielts_id_input.send_keys(student['IELTS']['R'])
    ielts_id_input = driver.find_element(By.NAME, "pIELTS_WRITING")
    ielts_id_input.clear()
    ielts_id_input.send_keys(student['IELTS']['W'])
    ielts_id_input = driver.find_element(By.NAME, "pIELTS_SPEAKING")
    ielts_id_input.clear()
    ielts_id_input.send_keys(student['IELTS']['S'])
    ielts_id_input = driver.find_element(By.NAME, "pIELTS")
    ielts_id_input.clear()
    ielts_id_input.send_keys(student['IELTS']['O'])
    
    time.sleep(1)
    save_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    save_btn.click()

    input("登录成功了吗？按回车键关闭浏览器...")
    driver.quit()