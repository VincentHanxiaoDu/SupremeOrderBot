from goods_list import *
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

headless = False

info = {
    'name': 'duhanxiao',
    'email': 'basugfdg@126.com',
    'tel': '132165',
    'address': 'asdasd',
    'apt': '12312',
    'zip': '',
    'city': 'asdasd',
    'province': 'ON',
    'country': 'CANADA',
    'cardnum': '24654',
    'expmonth': '02',
    'expyear': '2021',
    'cvv': '174',
}




def add_to_cart_dict(name_list):
    result = {}
    available_dict = get_current_goods_info(display_sold_out=False)
    for i in name_list:
        if i[0] in available_dict.keys():
            info = available_dict[i[0]].copy()
            info.update({'size': i[1]})
            print(info)
            result.update({i[0]: info})
    return result


def add_to_cart(name_list):
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.google.ca/')
    input()
    tasks_list = add_to_cart_dict(name_list)
    wait = WebDriverWait(driver, 3)
    for i in tasks_list.keys():
        try:
            driver.get(tasks_list[i]['url'])
            submit = wait.until(EC.element_to_be_clickable((By.NAME, 'commit')))
            size_selector = driver.find_element_by_id('s')
            size_selector.click()
            size = tasks_list[i]['size']
            size_option = driver.find_element_by_xpath('//select[@id="s"]/option[text()="{}"]'.format(size))
            size_option.click()
            submit.click()
        except Exception as e:
            continue
    checkout = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="button checkout"]')))
    checkout.click()
    driver.implicitly_wait(10)
    script_vars = '''
    var billing_name = "{}";
    var order_email = "{}";
    var order_tel = "{}";
    var order_address = "{}";
    var order_address2 = "{}"
    var order_billing_zip = "{}";
    var order_billing_city = "{}";
    
    //Payment info
    var cnb = "{}";
    var month = "{}";
    var year = "{}";
    var vval = "{}";
    '''.format(info['name'],
               info['email'],
               info['tel'],
               info['address'],
               info['apt'],
               info['zip'],
               info['city'],
               info['cardnum'],
               info['expmonth'],
               info['expyear'],
               info['cvv'],
               )
    with open('script.txt', 'r') as f:
        script = script_vars + f.read()
    driver.execute_script(script)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@id="order_billing_country"]'))).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//select[@id="order_billing_country"]/option[text()="{}"]'.format(info['country'])))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@id="order_billing_state"]'))).click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//select[@id="order_billing_state"]/option[text()="{}"]'.format(info['province'])))).click()
    input()
    driver.close()


a = add_to_cart([
    ['Logo Tape N-3B Parka["Red"]', 'Medium'],
    ['S/S Pocket Tee["Yellow"]', 'Medium'],
    ['123["xxx"]', 'Small']
])
