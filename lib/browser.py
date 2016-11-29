#!/usr/bin/python
import mechanize
import cookielib
import time
import random

class Browser:

    proxyList = []
    check = ''
    mechBrowser = None
    courtesyTime = 2

    def __init__(self, proxyList, check):
        self.proxyList = proxyList
        self.check = check

    def setup(self):
        self.mechBrowser = mechanize.Browser()
        cookieJar = cookielib.LWPCookieJar()
        self.mechBrowser.set_cookiejar(cookieJar)

        self.mechBrowser.set_handle_equiv(True)
        self.mechBrowser.set_handle_redirect(True)
        self.mechBrowser.set_handle_referer(True)
        self.mechBrowser.set_handle_robots(False)
        self.mechBrowser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:48.0) Gecko/20100101 Firefox/48.0'
        self.mechBrowser.addheaders = [('User-agent', agent)]

    def shutdown(self):
        self.mechBrowser.close()

    def sleep(self):
        time.sleep(self.courtesyTime + random.randint(1, self.courtesyTime))

    def getSource(self, url):
        while (True):
            self.sleep()
            source = self.getSourceOrFalse(url)
            if (False != source):
                return source

    def getSourceOrFalse(self, url):
        proxyUrl = random.choice(self.proxyList) + '?b=24'

        try:
            self.mechBrowser.open(proxyUrl)

            formCount = 0
            for form in self.mechBrowser.forms():
                if (str(form.attrs['action']).find('process.php?') > 0):
                    break
                formCount = formCount+1
            self.mechBrowser.select_form(nr=formCount)

            self.mechBrowser.form['u'] = url
            self.mechBrowser.submit()
        except:
            return self.fail(proxyUrl, 'Form Submission Failure')

        try:
            source = self.mechBrowser.response().read()
        except:
            return self.fail(proxyUrl, 'Response Read Failure')

        # Hack to compensate for XHTML etc
        self.mechBrowser._factory.is_html = True

        if 'Security Warning' == self.mechBrowser.title():
            try:
                self.mechBrowser.select_form(nr=0)
                self.mechBrowser.submit()
                response = self.mechBrowser.response()
                source = response.get_data()
            except:
                return self.fail(proxyUrl, 'Security Warning Override Failure')

        if (source.find(self.check) == -1):
            return self.fail(proxyUrl, 'Source Verficiation Failure')

        return source

    # TODO: Actually Log These Failures
    def fail(self, proxyUrl, message):
        print('Log Failure!')
        print(proxyUrl)
        print(message)

        return False
