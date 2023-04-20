import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os

import magic

def get_excel_engine(file_path):
    mime = magic.Magic()
    mime_type = mime.from_file(file_path)

    if mime_type == 'application/vnd.ms-excel':
        return 'xlrd'
    elif mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        return 'openpyxl'
    else:
        raise ValueError(f"Unsupported Excel file type: {mime_type}")

class ColumHeader:
    def __init__(self, i, name) -> None:
        self.col_index = i
        self.name = name
    def __repr__(self) -> str:
        return f'列={self.col_index}, {self.name}'

def is_str_in(keyword, s):
    return isinstance(s, str) and keyword in s
          
class GangWei(ColumHeader):
    def __init__(self, i, name) -> None:
        super().__init__(i, name)

    def match(name):
        return name in ['招聘岗位', '岗位']
    
class OtherConditions(ColumHeader):
    def __init__(self, i, name) -> None:
        super().__init__(i, name)

    def match(name):
        return is_str_in('其他要求', name) or name in ['其他']

class Danwei(ColumHeader):
    def __init__(self, i, name) -> None:
        super().__init__(i, name)
    def match(name):
        return is_str_in('单位', name)
    
class Zhuanye(ColumHeader):
    def __init__(self, i, name) -> None:
        super().__init__(i, name)
    def match(name):
        return is_str_in('专业', name)        

class Degree(ColumHeader):
    def __init__(self, i, name) -> None:
        super().__init__(i, name)
    def match(name):
        return is_str_in('学历', name)
    
class Age(ColumHeader):
    def __init__(self, i, name) -> None:
        super().__init__(i, name)
    def match(name):
        return name in ['年龄要求', '年龄']
    
gColumn_Headers = {
    GangWei.__name__: GangWei,
    OtherConditions.__name__: OtherConditions,
    Danwei.__name__: Danwei,
    Zhuanye.__name__: Zhuanye,
    Degree.__name__: Degree,
    Age.__name__: Age,
}

class ZhaopinInfo:
    def __init__(self, file_name, df) -> None:
        self.name = file_name
        self.df = df
        self.collection = {}
        self.count = 0
        self.rows = []

    def get_header(self):
        for idx, row in self.df.iterrows():
            if self.count == len(gColumn_Headers.keys()):
                break
            for c, item in enumerate(row.items()):
                self.extract_header(c, item)

    def extract_header(self, col, item):
        if len(item) >= 2:
            for k, v in gColumn_Headers.items():
                if v.match(item[1]):
                    self.count += 1
                    self.collection[k] = v(col, item[1])

    def print_header(self):
        s = f"""
        excel={self.name}
        """
        #print(s)
    def find(self):
        for idx, row in self.df.iterrows():
            if Zhuanye.__name__ in self.collection:
                r = row[self.collection[Zhuanye.__name__].col_index]
                if is_str_in('计算机', r):
                    if Age.__name__ in self.collection:
                        r = row[self.collection[Age.__name__].col_index]
                        if is_str_in('30周岁', r):
                            continue
                    if OtherConditions.__name__ in self.collection:
                        r = row[self.collection[OtherConditions.__name__].col_index]
                        if is_str_in('党员', r):
                            continue
                    if Degree.__name__ in self.collection:
                        r = row[self.collection[Degree.__name__].col_index]
                        if r == '博士研究生':
                            continue                                              
                    self.rows.append(row)
        for r in self.rows:
            print(f'=={self.name}==')
            print(r.values)

def extract(excel_name):
    df = None
    try:
        df = pd.read_excel(
        open(excel_name, 'rb'), sheet_name=0)
    except:
        engine = get_excel_engine(excel_name)
        df = pd.read_excel(
        open(excel_name, 'rb'), sheet_name=0, engine=engine)
    reader = ZhaopinInfo(excel_name, df)
    reader.get_header()
    reader.print_header()
    reader.find()
if __name__ == '__main__':
    # Specify the directory path
    dir_path = 'zhaopin/collection420'

    # Iterate over the files in the directory
    with os.scandir(dir_path) as entries:
        for entry in entries:
            
            # Check if it is a file (not a directory)
            if entry.is_file() and (entry.name.endswith('.xls') or entry.name.endswith('.xlsx')):
                extract(entry.path)
