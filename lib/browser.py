#!/usr/bin/python
import cookielib
import logging
import mechanize
import multiprocessing
import time
import random

class Browser:

    proxyList = []
    check = ''
    mechBrowser = None
    courtesyTime = 2
    browserTimeout = 45

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
        logging.getLogger('Browser').info('Scraping URL : ' + url)
        while (True):
            self.sleep()
            source = self.getSourceOrFalse(url)
            if (False != source):
                return source

    def getSourceOrFalse(self, url):
        proxyUrl = random.choice(self.proxyList) + '?b=24'
        logging.getLogger('Browser').info('Proxy Url : ' + proxyUrl)

        parentPipe, childPipe = multiprocessing.Pipe()
        process = multiprocessing.Process(
            target=self.setSourceAttributeFromProxy,
            args=(url, proxyUrl, childPipe)
        )
        process.start()

        if parentPipe.poll(self.browserTimeout):
            result = parentPipe.recv()
            if isinstance(result, basestring):
                process.terminate()
                return result

        process.terminate()
        self.fail(proxyUrl, 'Timout or Other Low Level Error Occured')
        return False

    def setSourceAttributeFromProxy(self, url, proxyUrl, pipe):
        # Submit the form for the proxy
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
            self.fail(proxyUrl, 'Form Submission Failure')
            return

        # Get the source after form submission
        try:
            source = self.mechBrowser.response().get_data()
        except:
            self.fail(proxyUrl, 'Response Read Failure')
            return

        # Hack to compensate for XHTML etc
        self.mechBrowser._factory.is_html = True

        # Submit the security warning form if found
        if 'Security Warning' == self.mechBrowser.title():
            logging.getLogger('Browser').info('Security Warning Detected')
            try:
                self.mechBrowser.select_form(nr=0)
                self.mechBrowser.submit()
                response = self.mechBrowser.response()
                source = response.get_data()
            except:
                self.fail(proxyUrl, 'Security Warning Override Failure')
                return

        # Check source for our keywords
        if (source.find(self.check) == -1):
            self.fail(proxyUrl, 'Source Verficiation Failure')
            return

        pipe.send(source)
        pipe.close()

    def fail(self, proxyUrl, message):
        logger = logging.getLogger('Browser')
        logger.warning(message + ' : ' + proxyUrl)
