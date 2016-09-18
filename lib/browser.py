#!/usr/bin/python
import mechanize
import cookielib
import time
import random

class Browser:
 
    # Find All Proxies
    # Google: "Powered by Glype"
    
    proxyList = [
        # BROKEN
        #   'http://getanonymous.com/index.php',
        #   'https://thespacesurf.com/index.php',
        #   'http://ricardoalcala.com/index.php',
        #   'http://p.pomstiborius.pl/index.php',
        #   'http://www.blackhost.xyz/glype/index.php',
        #   'https://muadness.com/proxy/index.php',
        #   'http://freebritishproxy.com/index.php',
        # FAILS
        #   'http://proxy.rimmer.su/index.php',
        # THROTTLED 
        #   'http://zero1.ocaspro.com/index.php',
        # SLOW
        #   'http://proxy-bg.com/index.php',

        #'https://rgsurf.com/index.php',
        #'https://cookieparts.com/click/index.php',
        #'https://hidethedork.com/index.php',
        #'http://theproxy.co/index.php', 

	'https://foxhold.com/web/index.php',
        'http://samstevenm.com/prox/index.php',
        'http://thehidden.ninja/index.php',
        'http://proxy.doomoney.com/index.php',
        'http://mail.germanystudy.net/index.php',
        'http://bypass.germanystudy.net/index.php',
        'http://mail.travelpakistan.org/index.php',
        'http://bypass.travelpakistan.org/index.php',
        # HALF BROKEN 'http://antoinem.com/preauxy/index.php',
        'http://blooby.eu/index.php',
        'http://www.crankedcode.com/projects/glype-youtube/index.php',
        'https://serviceone.tk/glype/index.php',
    ]
    mechBrowser = None
    courtesyTime = 3

    def __init__(self):
        self.mechBrowser = mechanize.Browser()
        cookieJar = cookielib.LWPCookieJar()
        self.mechBrowser.set_cookiejar(cookieJar)

        self.mechBrowser.set_handle_equiv(True)
        self.mechBrowser.set_handle_redirect(True)
        self.mechBrowser.set_handle_referer(True)
        self.mechBrowser.set_handle_robots(False)
        self.mechBrowser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        self.mechBrowser.addheaders = [('User-agent', agent)]

    def sleep(self):
        time.sleep(self.courtesyTime + random.randint(1, self.courtesyTime))

    def getHtml(self, url):
        proxyUrl = random.choice(self.proxyList) + '?b=24'
        # print proxy if trying to debug
        print(proxyUrl)
        self.mechBrowser.open(proxyUrl)
        self.sleep()

        self.mechBrowser.select_form(nr=0)
        self.mechBrowser.form['u'] = url
        self.mechBrowser.submit()
        self.sleep()

        return self.mechBrowser.response().read()

    def getSource(self, url):
        try:
            return self.getHtml(url)
        except:
            # print failure message if trying to debug
            print('failed')
            return self.getSource(url)
