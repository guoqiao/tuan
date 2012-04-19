#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import smtplib
from urlparse import urljoin
from pyquery import PyQuery as pq

SITES = [
'http://hz.meituan.com/', 
'http://hangzhou.lashou.com/',
]

SUBSCRIBES = {
u'沸腾鱼乡': ['foo@gmail.com', 'bar@gmail.com'],
}


EMAIL_USER = 'foo@insigma.com.cn'
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
    info = 'From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s\r\n' % (EMAIL_USER, ', '.join(receivers), subject, message)
    EMAIL_SEVR.sendmail(EMAIL_USER, receivers, info)
    print info

TREMS = [
u'元',
u'人',
u'价值', 
u'仅售', 
u'原价', 
u'套餐',
u'美梦', 
u'梦想',
]

def has_term(text):
    for t in TREMS:
        if t in text:
            print 'has_term: found %s in %s' % (t, text)
            return 1
    return 0

PATTERNS = [
r'【.*】',
r'(\d+-)?\d+\s*(人)?(套餐)?',
r'\d+([.]\d+)?\s*',
]

def match_pattern(text):
    for p in PATTERNS:
        if re.search(p, text):
            print 'match_pattern: found pattern in %s' % (text, )
            return 1
    return 0
    
def main():
    for site in SITES:
        print 'scaning %s ...' % (site)
        d = pq(url = site)
        for a in d('a'):
            text = a.text_content()
            if not text:
                continue
            text = text.strip()
            l = len(text)
            if l < 15:
                continue
            print 'text(len = %d): %s' % (l, text)
            if match_pattern(text) or has_term(text):
                for k in SUBSCRIBES.keys():
                    if k in text:
                        print '-------------match!-----------------'
                        r = SUBSCRIBES[k]
                        s = u'[%s] 团购信息' % (k)
                        href = urljoin(a.base_url, a.get('href'))
                        m = u'%s:\n%s' % (text, href)
                        sendmail(r, s, m)
                        print '-------------mail!-----------------'
    if EMAIL_SEVR:
        EMAIL_SEVR.quit()

    
if __name__ == '__main__':
    main()
