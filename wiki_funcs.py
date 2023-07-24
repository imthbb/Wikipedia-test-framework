from selenium import webdriver
from configparser import ConfigParser
import logging

By = webdriver.common.by.By

# -Vector legacy(2010) = 'vectl'
# -MonoBook = 'monob'
# -Timeless = 'timel'
# -MinervaNeue = 'miner'
# -Vector(2022) = 'vect'

log_file = 'logfile.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
f_h = logging.FileHandler(log_file)
formatter = logging.Formatter(f'''%(levelname)s - %(asctime)s - %(lineno)s - %(message)s''')
f_h.setFormatter(formatter)
logger.addHandler(f_h)

msg_el_n_f = '''Element not found. '''
msg_fail = 'FAIL'
msg_scs = 'SUCCESS'


def set_vars():
    global url, user, passwords, chosen_driver
    settings_file = 'settings.ini'
    cf_sett_f = ConfigParser()
    cf_sett_f.read(settings_file)
    url = cf_sett_f['presets']['url']

    user = cf_sett_f['private_data']['user']
    passwords = {0: cf_sett_f['private_data']['password'], 1: cf_sett_f['private_data']['temporary_password']}
    chosen_driver = cf_sett_f['presets']['driver']


def open_browser():
    driver = webdriver.Firefox(executable_path=chosen_driver)
    return driver


def login(driver, psswd=0):
    try:
        driver.find_element(By.CSS_SELECTOR, '#pt-login-2 a').click()
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False
    try:
        driver.find_element(By.ID, 'wpName1').clear()
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False
    driver.find_element(By.ID, 'wpName1').send_keys(user)
    try:
        driver.find_element(By.ID, 'wpPassword1').send_keys(passwords[psswd])
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False
    try:
        driver.find_element(By.ID, 'mw-input-captchaWord')
    except:
        pass
    else:
        input('''CAPTCHA appeared. When it's solved, enter anything to proceed.''')
        logger.info('CAPTCHA appeared.')
    try:
        driver.find_element(By.ID, 'wpLoginAttempt').click()
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False
    try:
        showed_username = driver.find_element(By.CSS_SELECTOR, '#pt-userpage a').text
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False
    else:
        if showed_username == user:
            logger.info(msg_scs)
            return True
        else:
            logger.error('Wrong username. ' + msg_fail)
            return False


def logout(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, '#pt-logout a').click()
    except:
        return msg_el_n_f + msg_fail, False
    return msg_scs, True


def watchlist_add_rmv(driver, to_watch=True):
    if to_watch:  # Adds article to watchlist
        to_do = '#ca-watch a'
    else:  # Removes article from watchlist
        to_do = '#ca-unwatch a'
    try:
        driver.find_element(By.CSS_SELECTOR, to_do).click()
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False
    else:
        logger.info(msg_scs)
        return True


def watchlist_popup(driver):
    try:
        driver.find_element(By.ID, 'mw-notification-area')
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False
    logger.info(msg_scs)
    return True


def change_psswd(driver, psswd0, psswd1):
    try:
        driver.find_element(By.CSS_SELECTOR, '#pt-preferences a').click()
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False
    try:
        driver.find_element(By.CSS_SELECTOR, '#mw-input-wppassword a').click()
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False
    try:
        driver.find_element(By.ID, 'ooui-php-1').send_keys(passwords[psswd1])
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False
    try:
        driver.find_element(By.ID, 'ooui-php-2').send_keys(passwords[psswd1])
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False
    try:
        driver.find_element(By.CSS_SELECTOR, '#change_credentials_submit').click()
    except:
        logger.error(msg_el_n_f + msg_fail)
        return False

    try:
        driver.find_element(By.CSS_SELECTOR, '#userloginForm .mw-message-box-warning')
    except:
        logger.info(msg_scs)
        return True
    else:
        logger.info('''Password was reentered to verify user. ''')
        try:
            driver.find_element(By.ID, 'wpPassword1').send_keys(passwords[psswd0])
        except:
            logger.error(msg_el_n_f + msg_fail)
            return False
        try:
            driver.find_element(By.CSS_SELECTOR, '#wpLoginAttempt').click()
        except:
            logger.error(msg_el_n_f + msg_fail)
            return False
    logger.info(msg_scs)
    return True


if __name__ == "__main__":
    set_vars()
    driver = open_browser()
    driver.get(url)







