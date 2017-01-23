# clearance_scraper

Install libraries for all the things this Python script needs.
```bash
pin install mechanize
pip install beautifulsoup4
pip install python-telegram-bot
```

Here is my crontab file.
```
0 0,12  * * * /root/scrape/scrape.sh
0 8  * * * /root/scrape/scrape.sh settings-override-morning.cfg
0 17 * * * /root/scrape/scrape.sh settings-override-afternoon.cfg
```
