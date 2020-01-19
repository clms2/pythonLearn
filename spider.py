from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from db.data import Data

browser = webdriver.Chrome()
browser.maximize_window()
wait = WebDriverWait(browser, 10)


def search():
    try:
        browser.get('https://www.jd.com/')

        # 等待搜索框加载出来
        # 像'presence_of_element_located'之类的动作，可以到Selenium官方文档查询
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#key"))
        )
        # 等待搜索按钮可以被点击
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#search .form .button'))
        )
        input.send_keys('美食')
        submit.click()

        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage .p-skip b"))
        )
        return total.get_attribute('innerText')
    except TimeoutException:
        print('in timeout exception')
        # 如果出现超时异常，重新执行search()函数
        return search()


def next_page(page_number):
    submit = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage .p-num .pn-next'))
    )
    submit.click()
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    browser.implicitly_wait(5)

    obj_curr_page = browser.find_element_by_css_selector('#J_bottomPage .p-num .curr')
    print(obj_curr_page.text)
    wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#J_bottomPage .p-num .curr"), str(page_number))
    )
    get_products()


# def next_page(page_number):
#     try:
#         print('in', page_number)
#         input = wait.until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage input"))
#         )
#         print(input)
#         submit = wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage .p-skip a'))
#         )
#         # 清空文本框的值
#         input.clear()
#         # 给文本框赋值
#         print(page_number, type(page_number))
#         input.send_keys('2')
#         # 点击确定，进行翻页
#         submit.click()
#         # 判断一下当前页码与文本框中的页码是否一致
#         wait.until(
#             EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#J_bottomPage .p-num .curr"), str(page_number))
#         )
#         get_products()
#     except TimeoutException:
#         print('Exception')
#         next_page(page_number)


def get_products():
    try:
        items = browser.find_elements_by_css_selector('#J_goodsList .gl-warp li')
        rows = []
        for item in items:
            price = item.find_element_by_css_selector('.p-price strong i').text
            name = item.find_element_by_css_selector('.p-name a em').text
            rows.append(Data(title=name, price=price))

        Data().insert_data(rows)
    except TimeoutException:
        print('get products exception')
        get_products()


def main():
    total = search()
    total = int(total)
    total = 5
    for i in range(total):
        i += 1
        next_page(i)
    browser.close()


if __name__ == '__main__':
    main()
