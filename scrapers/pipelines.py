# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime

output_schema = {
    "name": {"cell": "A", "name": "项目名称"},
    "author": {"cell": "B", "name": "负责人"},
    "number": {"cell": "C", "name": "项目批准号"},
    "department": {"cell": "D", "name": "申请单位"},
    "research_type": {"cell": "E", "name": "研究类型"},
    "year": {"cell": "F", "name": "批准年度"},
    "money": {"cell": "G", "name": "金额"},
    "keywords": {"cell": "H", "name": "关键词"},
}


class ScrapersPipeline:
    def open_spider(self, spider):
        self.wb = Workbook()
        self.ws = self.wb.active
        cells = {}
        for v in output_schema.values():
            cells[v["cell"]] =  v["name"]
        self.ws.append(cells)
    def close_spider(self, spider):
        time = datetime.datetime.now()
        self.wb.save('data {}-{}-{}-{}.xlsx'.format(time.month, time.day, time.hour, time.minute))
        self.wb.close()

    def process_item(self, item, spider):
        cells = {}
        for k, v in output_schema.items():
            cells[v["cell"]] = item[k]
        self.ws.append(cells)
        return item
