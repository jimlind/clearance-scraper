#!/usr/bin/python
import cookielib
import logging
import mechanize
import multiprocessing
import time
import random

class Browser:

    check = ''
    mechBrowser = None
    logger = None
    courtesyTime = 60
    browserTimeout = 30

    def __init__(self, check):
        self.check = check
        self.logger = logging.getLogger('Browser')

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
        self.sleep()
        self.logger.info('Scraping URL : ' + url)

        parentPipe, childPipe = multiprocessing.Pipe()
        process = multiprocessing.Process(
            target = self.writeSourceToPipe,
            args = (url, childPipe)
        )
        process.start()

        if parentPipe.poll(self.browserTimeout):
            result = parentPipe.recv()
            if isinstance(result, basestring):
                process.terminate()
                return result

        process.terminate()
        self.logger.warning('Timout or Other Low Level Error Occured')
        return False

    def writeSourceToPipe(self, url, pipe):
        try:
            self.mechBrowser.open(url)
            source = self.mechBrowser.response().get_data()
        except:
            self.logger.warning('Response Read Failure')
            return

        # Check source for our keywords
        if (source.find(self.check) == -1):
            self.logger.warning('Source Verficiation Failure')
            return

        pipe.send(source)
        pipe.close()
