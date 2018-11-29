import urllib
# import urllib2
from http import cookiejar as cookielib 

#待学习

def taobao(username,password):  
    cj = cookielib.CookieJar()  
    print (cj)
    post_data = urllib.parse.urlencode(  
        {   
         'TPL_password':password,   
         'TPL_username':username,  
         }).encode(encoding="utf-8")
    
    path = 'https://login.taobao.com/member/login.jhtml'  
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))  
   
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13')]   
      
    urllib.request.install_opener(opener)  
    req = urllib.request.Request(path,post_data)  
    
    #try login  
    conn = urllib.request.urlopen(req)
    html = conn.read().decode('gbk','ignore')
    print (cj)
    print (html)
    
    
taobao(' ',' ')  
print ('OK')