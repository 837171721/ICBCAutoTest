#coding=utf-8
'''
Created on 2021.6.1

@author: wsk

'''
from logging import exception
import traceback
from pyautogui import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
from pymouse import PyMouse
from pykeyboard import PyKeyboard

class EsWebOperation:
    def __init__(self):
        self.m = PyMouse()
        self.k = PyKeyboard()


    def es_web_open(self, path, explore = 'IE'):
        '''
        打开网页
        :param path:打开的网页链接
        :param explore: 打开的浏览器类型。IE，Chrome，Firefox
        :return:
        '''
        try:
            if explore == 'IE' or explore =='ie' or explore =='Ie':
                self.driver = webdriver.Ie()
            elif explore == 'Chrome' or explore =='chrome' or explore == '谷歌':
                self.driver = webdriver.Chrome()
            elif explore == 'FireFox' or explore == 'Firefox' or explore == 'firefox' or'火狐' :
                self.driver = webdriver.Firefox()
            else:
                raise Exception("发生异常!!!")
        except Exception as e:
            traceback.print_exc()
            return e
        else:
            self.driver.get(path)
            self.driver.maximize_window()
            

    def es_web_btnclick(self, value = None, type = 'id'):
        '''
        点击网页中的按钮
        :param value:查找类型的值
        :param type: 查找元素的方式
        :return 
        '''
        try:
            if type == 'id':
                self.driver.find_element_by_id(value).click()
            elif type == 'name':
                self.driver.find_element_by_name(value).click()
            elif type == 'xpath':
                self.driver.find_element_by_xpath(value).click()
            elif type == 'link_text':
                self.driver.find_element_by_link_text(value).click()
            elif type == 'partial_link_text':
                self.driver.find_element_by_partial_link_text(value).click()
            elif type == 'tag_name':
                self.driver.find_element_by_tag_name(value).click()
            elif type == 'class_name':
                self.driver.find_element_by_class_name(value).click()
            elif type == 'css_selector':
                self.driver.find_element_by_css_selector(value).click()
            else: 
                raise Exception("发生异常!!!")
        except Exception as e:
            traceback.print_exc()
            return e

            
    def es_web_get_edit(self, id, type = 'id'):
        '''
        获取编辑框的内容
        :param id:查找类型的值
        :param type: 查找元素的方式
        :return 编辑框的内容
        '''
        try:
            if type == 'id':
                textcontents = self.driver.find_element_by_id(id).get_attribute('value')
            elif type == 'name':
                textcontents = self.driver.find_element_by_name(id).get_attribute('value')
            elif type == 'xpath':
                textcontents = self.driver.find_element_by_xpath(id).get_attribute('value')
            elif type == 'link_text':
                textcontents = self.driver.find_element_by_link_text(id).get_attribute('value')
            elif type == 'partial_link_text':
                textcontents = self.driver.find_element_by_partial_link_text(id).get_attribute('value')
            elif type == 'tag_name':
                textcontents = self.driver.find_element_by_tag_name(id).get_attribute('value')
            elif type == 'class_name':
                textcontents = self.driver.find_element_by_class_name(id).get_attribute('value')
            elif type == 'css_selector':
                textcontents = self.driver.find_element_by_css_selector(id).get_attribute('value')
            else: 
                raise Exception("发生异常!!!")
        except Exception as e:
            traceback.print_exc()
            return e
        else:
            return textcontents

    def es_web_set_edit(self, str = '',id = '', type = 'id'):
        '''
        设置编辑框的内容
        :param str: 向编辑框输入的内容
        :param id:查找类型的值
        :param type: 查找元素的方式
        :return
        '''
        try:
            if type == 'id':
                 self.driver.find_element_by_id(id).send_keys(str)
            elif type == 'name':
                self.driver.find_element_by_name(id).send_keys(str)
            elif type == 'xpath':
                self.driver.find_element_by_xpath(id).send_keys(str)
            elif type == 'link_text':
                self.driver.find_element_by_link_text(id).send_keys(str)
            elif type == 'partial_link_text':
                self.driver.find_element_by_partial_link_text(id).send_keys(str)
            elif type == 'tag_name':
                self.driver.find_element_by_tag_name(id).send_keys(str)
            elif type == 'class_name':
                self.driver.find_element_by_class_name(id).send_keys(str)
            elif type == 'css_selector':
                self.driver.find_element_by_css_selector(id).send_keys(str)
            else:
                raise Exception("发生异常!!!")
        except Exception as e:
            traceback.print_exc()
            return e
        
    
    def es_web_combox_select(self, select, select_type = 'id', option = '', option_type = 'visible_text'):
        '''
        下拉框选择
        :param select: select框属性
        :param select_type: select框属性类型,可以为id，name, xpath, link_text , partial_link_text, tag_name, class_name, css_selector
        :param option: option属性
        :param option_type: option属性类型
        return
        '''
        try:
            if select_type == 'id':
                opt = self.driver.find_element_by_id(select)
            elif select_type == 'name':
                opt = self.driver.find_element_by_name(select)
            elif select_type == 'xpath':
                opt = self.driver.find_element_by_xpath(select)
            elif select_type == 'link_text':
                opt = self.driver.find_element_by_link_text(select)
            elif select_type == 'partial_link_text':
                opt = self.driver.find_element_by_partial_link_text(select)
            elif select_type == 'tag_name':
                opt = self.driver.find_element_by_tag_name(select)
            elif select_type == 'class_name':
                opt = self.driver.find_element_by_class_name(select)
            elif select_type == 'css_selector':
                opt = self.driver.find_element_by_css_selector(select)
            else:
                raise Exception("发生异常!!!")
            if option_type == 'visible_text':
                Select(opt).select_by_visible_text(option)
            elif option_type == 'index':
                Select(opt).select_by_index(option)
            elif option_type == 'value':
                Select(opt).select_by_value(option)
            else:
                raise Exception("发生异常!!!") 
        except Exception as e:
            traceback.print_exc()
            return e

    def es_web_close(self):
        try:
            self.driver.close()
        except Exception as e:
            traceback.print_exc()
            return e 


if __name__ == '__main__':
    test = EsWebOperation()
    test.es_web_open('www.baidu.com', explore='ie')
    print('hello')
    sleep(5)
    test.es_web_close()
    
