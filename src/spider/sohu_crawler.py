# -*- coding:utf-8 -*-

import time
import json
import re
import os
import pprint
import datetime
import random
import logging
import logging.config

import requests
from selenium import webdriver

from settings import  HEADERS, LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('myspider')

'''
1、登录拿到cookies
2、获取验证码图片
3、验证码识别
'''

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SouHuPoster(object):
    def __init__(self, username, password):
        self.base_url =  "http://hn.focus.cn/msglist/271792/"   # 该编号是楼盘编号 
        self.username = username
        self.password = password
        self.session = requests.Session()      
        # self._login() 
        try:
            self._get_cookies()
        except IOError as e:
            logger.error(e)
        if self._check_login():            
            logger.debug('coockie from cache, login success')
        else:
            # 防止cookie过期失效
            self.session.cookies.clear()
            self._login()
 
    def _check_login(self):
        """验证是否登陆成功
        Returns:
            Boolean: 是否登陆成功
        """
        login_url = 'http://login.focus.cn/passport/getUserInfo'
        res = self.session.get(login_url, headers=HEADERS, verify=False)
        # import pdb
        # pdb.set_trace()
        resp_json = res.json()
        code = resp_json['code']
        if code == 200:
            return True
        else:
            logger.debug('last cache lose efficacy, response.text:{}'.format(resp_json))
            return False
    
    def _get_cookies(self):
        """从文本中获得cookie
        """
        cookie_file = os.path.join(BASE_DIR, "cookies/login_cookies.json" )
        with open(cookie_file) as f:
            cookies = json.load(f)
            self.session.cookies.update(cookies)
        
    def _login(self):     
        # driver = webdriver.Chrome(executable_path="C:/Program Files (x86)/Google/Chrome/Application/chromedriver")
        driver = webdriver.PhantomJS()
      
        driver.get(self.base_url)
        logger.debug("start login")
        login_field = driver.find_element_by_class_name("login")
        login_field.click()
        
        #等页面加载完
        time.sleep(10)  
        
        # 选择账号登录
        account_login = driver.find_element_by_class_name("type-menu").find_element_by_tag_name('a')
        account_login.click()
       
        # import pdb
        # pdb.set_trace()
        form = driver.find_element_by_class_name("account-form")
        username_field = form.find_element_by_class_name("uname").find_element_by_tag_name('input')   
        try:
            username_field.send_keys(self.username)
        except Exception as e:
            logger.error(e)
            username_field.send_keys(self.username.decode("utf-8"))    #当用户名是以中文形式
        passwd_field = form.find_element_by_class_name("upass").find_element_by_tag_name('input')
        passwd_field.send_keys(self.password)
        login_button = form.find_element_by_class_name("btn")
        login_button.click()
        time.sleep(10)

        cookies = driver.get_cookies()
        login_cookies = {item["name"] : item["value"] for item in cookies}     
        # page_html = driver.page_source
        if self._check_login():
            self.session.cookies.update(login_cookies)
            with open("cookies/login_cookies.json", "w") as f:
                json.dump(login_cookies, f)      
            logger.debug('login success')
        else:
            logger.debug('login failed')
        logger.debug('login cookies: {} '.format(pprint.pformat(login_cookies)))
        return login_cookies    

    def posts(self):
        pass



if __name__ == '__main__':
    username = '13189964671'
    password = 'ibgw4616'
    souhu = SouHuPoster(username, password)

