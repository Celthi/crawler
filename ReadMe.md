# ScienceNet Scraper
Collect the items from sciencenet(http://fund.sciencenet.cn/) 科学网基金查询

# How to use
1. install python3.9
2. install dependecies by `pip install -r requirements.txt`
3. modify the login name and password in config.json
4. Run `scrapy crawl quotes`
5. The data will be saved in `data ...xlsx`

# sample config.json
```
{
    "phone": "19075802974",
    "password": "******",
    "name": "路由",
    "yearStart": "2019",
    "yearEnd": "2021",
    "subject":"",
    "category": "",
    "fundStart": "",
    "fundEnd": ""
}

```

