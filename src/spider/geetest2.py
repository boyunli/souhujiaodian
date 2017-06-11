# coding:utf-8

import os
import logging.config
import json
import random

from lxml import etree
import requests

from settings import  HEADERS, LOGGING

logging.config.dictConfig(LOGGING)

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('myspider')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
   
class CrackPicture(object):

    def __init__(self, img_url1, img_url2):
        self.img1, self.img2 = self.picture_get(img_url1, img_url2)

    def picture_get(self, img_url1, img_url2):
        hd = HEADERS
        img1 = StringIO.StringIO(self.repeat(img_url1, hd).content)
        img2 = StringIO.StringIO(self.repeat(img_url2, hd).content)
        return img1, img2

    def repeat(self, url, hd):
        times = 10
        while times > 0:
            try:
                ans = requests.get(url, headers=hd)
                return ans
            except:
                times -= 1   

    def pictures_recover(self):
        xpos = self.judge(self.picture_recover(self.img1, 'img1.jpg'),
                          self.picture_recover(self.img2, 'img2.jpg')) - 6
        return xpos, self.darbra_track(xpos)

    def picture_recover(self, img, name):
        a =[39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29,
            27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12, 13, 23, 22, 14, 15, 21, 20, 8, 9,
            25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
        im = Image.open(img)
        im_new = Image.new("RGB", (260, 116))
        for row in range(2):
            for column in range(26):
                right = a[row*26+column] % 26 * 12 + 1
                down = 58 if a[row*26+column] > 25 else 0
                for w in range(10):
                    for h in range(58):
                        ht = 58 * row + h
                        wd = 10 * column + w
                        im_new.putpixel((wd, ht), im.getpixel((w + right, h + down)))
        im_new.save(name)
        return im_new

    def darbra_track(self, distance):
        return [[distance, 0.5, 2134]]
        #crucial trace code was deleted

    def diff(self, img1, img2, wd, ht):
        rgb1 = img1.getpixel((wd, ht))
        rgb2 = img2.getpixel((wd, ht))
        tmp = reduce(lambda x,y: x+y, map(lambda x: abs(x[0]-x[1]), zip(rgb1, rgb2)))
        return True if tmp >= 190 else False
            
    def col(self, img1, img2, cl):
        for i in range(img2.size[1]):
            if self.diff(img1, img2, cl, i):
                return True
        return False

    def judge(self, img1, img2):
        for i in range(img2.size[0]):
            if self.col(img1, img2, i):
                return i
        return -1


class BaseGeetestCrack(object):
    '''验证码破解基础类'''

    def __init__(self, url):
        self.url = url
        self.geeimg = {}
        self.session = requests.Session()      
        try:
            self._get_cookies()
        except IOError as e:
            logger.error(e)

    def _get_cookies(self):
        '''
        从文本中获得cookie
        '''
        cookie_file = os.path.join(BASE_DIR, "cookies/login_cookies.json" )
        with open(cookie_file) as f:
            cookies = json.load(f)
            self.session.cookies.update(cookies)

    def get_gt(self):
        '''
        获取参数gt
        '''
        url = self.url
        text = self.session.get(url=url, headers=HEADERS).text
        selector = etree.HTML(text)
        src = selector.xpath('//div[@class="geetest_code"]/script/@src')[0]
        if src:
            gt = src.split('=')[1]
        else:
            logger.debug('未获取到gt值，检查cookie是否过期')
            gt = ''
        return gt

    def gee_timestamp(self):
        return str(int(random.random()*10000+int(time.time()*1000)))

    def get_challenge(self):
        import pdb
        pdb.set_trace()
        url = 'http://api.geetest.com/get.php?gt={}'.format(self.get_gt())
        # 该js_text包含: id, static_server等
        js_text = self.session.get(url=url, headers=HEADERS).text
        challenge = re.findall(r'"challenge":\s"(\w+)?"', js_text)[0]

        static_host = 'http://static.geetest.com/'
        bg_img = static_host + re.findall(r'"bg":\s"(\S+)?"', js_text)[0]
        fullbg_img = static_host + re.findall(r'"fullbg":\s"(\S+)?"', js_text)[0]
        slice_img = static_host + re.findall(r'"slice":\s"(\S+)?"}', js_text)[0] 
        self.geeimg = {
                'bg': bg_img,
                'fullbg': fullbg_img,
                'slice': slice_img
                }
        return challenge

    def get_userresponse(self, a, b):
        c = b[32:]
        
        d = []
        for i in range(len(c)):
            f = ord(c[i])
            d.append(f-87 if f > 57 else f-48)
        c = 36 * d[0] + d[1]
        g = round(a) + c
        b = b[0:32]
        i = [[],[],[],[],[]]
        j = {}
        k = 0
        for e in range(len(b)):
            h = b[e]
            if h not in j:
                j[h] = 1
                i[k].append(h)
                k = k + 1
                if k == 5: k = 0      
        n = g
        o = 4
        p = ""
        q = [1,2,5,10,50]
        while n > 0:
            if n - q[o] >= 0:
                m = int(random.random() * len(i[o]))
                p += str(i[o][m])
                
                n -= q[o]
            else:
                i = i[:o] + i[o+1:]
                q = q[:o] + q[o+1:]
                o -= 1
        return p
    
     def get_xpos_trace(self):
         fullbg = self.geeimg['fullbg']
         bg = self.geeimg['bg']
         xpos, tracks = CrackPicture(fullbg, bg).pictures_recover()
         return xpos. tracks

    def gee_c(self, a):
        e = []
        f = 0
        g = []
        h = 0
        for h in range(len(a) - 1):
            b = int(round(a[h+1][0] - a[h][0]))
            c = int(round(a[h+1][1] - a[h][1]))
            d = int(round(a[h+1][2] - a[h][2]))
            g.append([b, c, d])
            if b == 0 and c == 0 and d == 0:
                pass
            elif b ==0 and c == 0:
                f += d
            else:
                e.append([b, c, d+f])
                f = 0
        if f != 0:
            e.append([b, c, f])
        return e

    def gee_f(self, a):
        g = []
        h = []
        i = []
        for j in range(len(a)):
            b = self.gee_e(a[j])
            if b:
                h.append(b)
            else:
                g.append(self.gee_d(a[j][0]))
                h.append(self.gee_d(a[j][1]))
            i.append(self.gee_d(a[j][2]))
        return "".join(g) + "!!" + "".join(h) + "!!" + "".join(i)

    def refresh(self):
        hd = HEADERS
        url = "https://api.geetest.com/refresh.php?challenge={}&gt={}&callback=geetest_{}"\
                .format(self.get_challenge()), self.get_gt(), self.gen_timestamp())
        ans = self.session.get(url=url, headers=HEADERS)
        tjson = re.findall("\((.*?)\)", ans.content)[0]
        self.geeimg.update(json.loads(tjson))

    def process(self):
        xpos, tracks = self.get_xpos_trace()
        logger.debug('xpos:{}'.format(xpos))
        act = self.gee_f(self.gee_c(tracks))
        time.sleep(0.6)
        passtime = str(tracks[-1][-1])
        imgload = str(random.randint(0,200) + 50)
        userresponse = self.get_userresponse(xpos, self.get_challenge())
        time.sleep(0.6)
        url = 'http://api.geetest.com/ajax.php?gt={gt}&challenge={challenge}&passtime={passtime}&imgload={imgload}&a={a}&callback=geetest_{timestamp}'\
                .format(
                        gt = self.get_gt(),
                        challenge = self.get_challenge(),
                        passtime = passtime,
                        imgload = imgload,
                        a = act,
                        timestamp = self.gee_timestamp()
                        )
        text = self.session.get(url=url, headers=HEADERS).text
        logger.debug('\033[92m 滑块验证后返回的text:{} \033[0m'.format(text))
        tjson = json.loads(re.findall("\((.*?)\)", text)[0])
        if tjson["success"] != 1:
            if times == 0:
                raise NameError
            time.sleep(6)
            self.refresh()
            times -= 1
            continue
        else:
            logger.debug('滑块验证成功!')



if  __name__ == '__main__':
    url = 'http://hn.focus.cn/msglist/271792/'
    geetest = BaseGeetestCrack(url)
    geetest.process()



























