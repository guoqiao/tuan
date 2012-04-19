#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib
import smtplib

from email.MIMEMultipart import MIMEMultipart   
from email.MIMEText import MIMEText   

from urlparse import urljoin
from pyquery import PyQuery as pq

SUBSCRIBES = {
u'绿茶': ['foo@gmail.com'],
}

EMAIL_USER = 'spig@insigma.com.cn'
EMAIL_PSWD = 'password'
EMAIL_SMTP = 'smtp.insigma.com.cn'
EMAIL_PORT = 587
EMAIL_SEVR = None

def sendmail(receivers, subject, message):
    if not receivers:
        return
    global EMAIL_SEVR
    if not EMAIL_SEVR:
        print 'trying to connect smtp server ...'
        EMAIL_SEVR = smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT)
        EMAIL_SEVR.login(EMAIL_USER, EMAIL_PSWD)
        
    # 设定root信息   
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = EMAIL_USER
    msgRoot['To'] = ', '.join(receivers)
    msgRoot.preamble = 'This is a multi-part message in MIME format.'  

    #设定纯文本信息   
    msgText = MIMEText(message, 'plain', 'utf-8')
    msgRoot.attach(msgText)

    #~ info = 'From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s\r\n' % (EMAIL_USER, ', '.join(receivers), subject, message)
    #~ print 'sending mail:\n%s' % info
    
    info = msgRoot.as_string()
    print '***********************************'
    print info
    print '***********************************'
    EMAIL_SEVR.sendmail(EMAIL_USER, receivers, info)

PATTERNS = [
r'【.*】',
r'\d+([.]\d+)?\s*',
r'(\d+-)?\d+\s*(人)?(套餐)?',
]

def match_pattern(text):
    for p in PATTERNS:
        if re.search(p, text):
            return 1
    return 0

def main():
    for k in SUBSCRIBES.keys():
        print 'searching %s ...' % k
        k_en = k.encode('gbk') # baidu use this encode
        query = {'do': 'search', 'today': '1', 'wd': k_en}
        args = urllib.urlencode(query)
        url = 'http://tuan.baidu.com/?%s' % args
        print url
        d = pq(url=url)
        for a in d('a'):
            text = a.text_content()
            if not text:
                continue
            text = text.strip()
            l = len(text)
            if l < 15:
                continue
            print 'text(len = %d): %s' % (l, text)
            if match_pattern(text):
                if k in text:
                    r = SUBSCRIBES[k]
                    s = u'[%s] 团购信息' % (k)
                    href = urljoin(a.base_url, a.get('href'))
                    m = u'%s\n%s' % (text, href)
                    sendmail(r, s, m)
    if EMAIL_SEVR:
        EMAIL_SEVR.quit()
        
if __name__ == '__main__':
    main()
