from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback
from datetime import datetime, timedelta

# 설정
chrome_driver_path = 'C:/Users/UserK/Downloads/chromedriver.exe' # 각자 경로에 따라서 변경
site_url = 'https://sugang.hsu.ac.kr/'
username = 'your_id'  # 여기에 아이디 입력
password = 'your_pw'  # 여기에 비밀번호 입력

# ChromeDriver 설정
service = Service(chrome_driver_path)
chrome_options = Options()
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 사이트 접속
    driver.get(site_url)

    # 아이디와 비밀번호 입력
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'login_id'))
    ).send_keys(username)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'passwd'))
    ).send_keys(password)

    # 로그인 버튼 클릭 (title 속성으로 찾기)
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@title="로그인"]'))
    )
    login_button.click()

    # 첫 번째 팝업창 처리
    WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()

    # 특정 frame으로 전환
    driver.switch_to.frame('frame_id')

    
    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'select_id'))
    )
    select_element.click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//option[@value=""]'))
    ).click()

    # 학수번호 입력
    subject_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'input_id'))
    )
    subject_input.clear() 
    subject_input.send_keys("학수번호")

    # 검색 버튼 클릭 
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'button_id'))
    )
    search_button.click()

    # 현재 시간
    start_time = datetime.now()

    while (datetime.now() - start_time) < timedelta(hours=1):  # 1시간 동안 반복
        try:
            # 수강 신청 버튼 클릭
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'button_id'))
            ).click()

            
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[1])
            
            # 확인 버튼 클릭 시도
            confirm_clicked = False
            for attempt in range(3):  # 최대 3번 시도
                try:
                    confirm_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//input[@value="확인"]'))
                    )
                    confirm_button.click()
                    confirm_clicked = True
                    break  
                except Exception as click_error:
                    print(f"확인 버튼 클릭 시도 실패: {click_error}")
                    time.sleep(1)  # 다시 시도하기 전 1초 대기

            if not confirm_clicked:
                print("확인 버튼을 클릭하지 못했습니다. 반복을 중지합니다.")
                break  

            # 새 창 닫힘 후 팝업창 발생 처리
            driver.switch_to.window(driver.window_handles[0])
            WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()

            # 원래 프레임으로 돌아가기
            driver.switch_to.frame('frame_id')

        except Exception as e:
            print("반복 중 오류 발생:", e)
            traceback.print_exc() 

except Exception as e:
    print("오류 발생:", e)
    traceback.print_exc()  

finally:
    print("모든 작업 완료")
    # driver.quit() 
