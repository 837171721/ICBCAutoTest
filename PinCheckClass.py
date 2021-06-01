#coding=utf-8
'''''
Created on 2018.01.19
The file is used to Attempt to test
@author: ys
_doc_:    
Check if your password safe 通过正则表达式
'''''

import re
import string
class CheckPasswordClass():       
    def checklen(self,pwd): #字符串长度
        return len(pwd)

    def checkContainUpper(self,pwd): #字符串中是否包含大写字母
       # pattern = re.compile('[A-Z]+')
        pattern = re.compile('(A)')      
        match = pattern.findall(pwd)
        print(match)     
        if match:
            return True
        else:
            return False

    def checkContainNum(self,pwd): #字符串中是否包含数字
        pattern = re.compile('[0-9]+')
        match = pattern.findall(pwd)
        if match:
            return True
        else:
            return False
 
    def checkContainLower(self,pwd): #字符串中是否包含小写字母
        pattern = re.compile('[a-z]+')
        match = pattern.findall(pwd)    
        if match:
            return True
        else:
            return False
 
    def checkSymbol(self,pwd):  #字符串中是否包含数字和字母
        pattern = re.compile('([^a-z0-9A-Z])+')
        match = pattern.findall(pwd)
        
        if match:
            return True
        else:
            return False
     
    def checkPassword(self,pwd):
        #判断密码长度是否合法
        lenOK=self.checklen(pwd)
        print ('长度符合:',lenOK)
        
        #判断是否包含大写字母
        upperOK=self.checkContainUpper(pwd)
        print ('大写字符:',upperOK)
         
        #判断是否包含小写字母
        lowerOK=self.checkContainLower(pwd)
        print ('小写字符:',lowerOK)
        
        #判断是否包含数字
        numOK=self.checkContainNum(pwd)
        print ('包含数字:',numOK)
        
        #判断是否包含符号
        symbolOK=self.checkSymbol(pwd)
        print ('包含符号:',symbolOK)        
        return ('检测结果',lenOK and upperOK and lowerOK and numOK and symbolOK)
          
    def char2ASC(self,pwd): #字符转换为ASCII码
        tmp=[]
        tmp.clear()
        for i in range(0,len(pwd)):
            tmp.append(ord(pwd[i]))
        return tmp
            
    def isMatchStr(self,srcStr,testStr,matchLen):
        
       # same_continue_one=len(re.findall(r'(?='1'*matchLen)|0*matchLen|-1*matchLen)', strstr)) 
        flag=len(re.findall(r'(?=11111)', srcStr))
        
    def checkContinousSymbol(self,pwd,cLen): #连续字符判断
        AscList=self.char2ASC(pwd) #字符转换为ASCII码
        tmp=[]
        tmp.clear()
        for  i in range(0,len(pwd)-1):
            tmp.append(AscList[i+1]-AscList[i])
        strstr=''
        strstr=''.join(i.__str__() for i in tmp)  #数组转字符串
        #get_strMatch()
        same_continue_one=len(re.findall(r'(?=11111|00000|-1-1-1-1-1)', strstr)) #字符串中是否存在5个连续相同的1值
        #same_continue_zero=len(re.findall(r'(?=00000)', strstr)) #字符串中是否存在5个连续相同的0值
        #same_continue_neg=len(re.findall(r'(?=-1-1-1-1-1)', strstr)) #字符串中是否存在5个连续相同的-1值     
        #if same_continue_one>=1 or same_continue_zero>=1 or same_continue_neg>=1:
        print(same_continue_one)
        if same_continue_one>=1:
            #连续字符超过6个  /递增字符超过6个  /递减字符超过6个
            return True
        else:
            return False    
                             
    def PasswordRulesOfICBC(self,pwd):
        pwd_len=len(pwd)
        if (pwd_len >= 6 and pwd_len<=30): #密码长度满足6~30位
            if (pwd_len < 8): #密码长度在6~8位
                print('简单密码！当前密码长度不足8位',pwd)
                return 0
            elif (pwd_len >=8 and pwd_len <=10):
                if True == len(re.findall(r'(?=567890|098765)', pwd)):
                    print('简单密码！存在超过6个的连续字符：',pwd)
                    return 0
                elif True == self.checkContinousSymbol(pwd,5):
                    print('简单密码！存在超过6个的连续字符：',pwd)
                    return 0
                else:
                    print('合法字符！',pwd) 
                    return 1 
            else :   
                print('强密码！当前密码长度超过10位：',pwd_len)
                return 1                
        elif(pwd_len < 6):
            print('密码长度不符！当前密码长度不足6位：',pwd_len)
            return 2
        else:
            subpwd=pwd[0:30]
            print("密码超长截断！当前密码长度位：%d,截取后密码长度:%d" %(pwd_len,len(subpwd)))  #多变量输出效果
            return 2
    def PasswordRulesOfABC(self,pwd):
        pwd_len=len(pwd)
        if 8 == pwd_len:
            if pwd_len == pwd.count(pwd[0]):
                print('简单密码!',pwd)
                return 0
            else:                                 
                if True == pwd.isalpha() and True == self.checkContainUpper(pwd): #便于后续超柜维护
                    #仅由字母组成，且包含大写
                    strstr=''
                    strstr=pwd.lower() #大写转小写
                    if pwd_len == strstr.count(strstr[0]):
                        print('若为超柜，则属简单密码!',pwd)
                        return 0
                    else:
                        print('合法字符',pwd)
                        return 1
                else:
                    print('合法字符',pwd)
                    return 1
        else:
            print('密码长度不符！',pwd)
            return 2
'''''
string.capitalize()     ：把字符串第一个字符大写
string.isalnum()        ：判断字符串是否只有字母数字
string.isalpha()        ：判断字符串是否只有字母
string.isdigit()        ：判断是否只含有数字
string.islower()        ：判断是否字符串中全部为小写
string.isupper()        ：判断是否字符串中全部为大写
string.isspace()        ：是否只含有空格
string.title()          ：返回标题化字符 【标题样式为：每个单词的第一个字符都是大写】
string.istitle()        ：是否为标题样式  
string.lower()          ：将所有字符串转为小写
string.upper()          ：将所有字符串转为大写
string.swapcase()       ：翻转大小写【大写变小写，小写变大写】
string.isnumeric()      ：判断是否只包含数字字符 【只存在Unicode对象】
string.isdecimal()      ：判断字符串是否只有十进制数字  【只存在Unicode对象】  字符串前有u标志     
'''''       
if __name__ == '__main__': 
    test = CheckPasswordClass()
    test.checkContainUpper('ACABCABCZABC')
    print('===========工行密码测试:===========')
    '''
    test.PasswordRulesOfICBC('12567890')   
    test.PasswordRulesOfICBC('120987650')       
    test.PasswordRulesOfICBC('12356789')
    test.PasswordRulesOfICBC('12356789') 
    test.PasswordRulesOfICBC('12121212') 
    test.PasswordRulesOfICBC('31311234') 
    test.PasswordRulesOfICBC('abcde234')  
    test.PasswordRulesOfICBC('fedcba@#')
    '''
    test.PasswordRulesOfICBC('zyxwvufe')
    test.PasswordRulesOfICBC('12654321')  
    test.PasswordRulesOfICBC('abcd12345')
    test.PasswordRulesOfICBC('1234654321')           
    test.PasswordRulesOfICBC('123uvwxyz') 
    test.PasswordRulesOfICBC('fedcbanm12')    
    test.PasswordRulesOfICBC('111111111111111111111111111111222')  
    print('===========农行密码测试：===========')
    test.PasswordRulesOfABC('111111')
    test.PasswordRulesOfABC('11111111')  
    test.PasswordRulesOfABC('AaAaaaaA')
    test.PasswordRulesOfABC('12222222')          