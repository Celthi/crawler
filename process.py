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
class GangWei(ColumHeader):
    def __init__(self, i, name) -> None:
        super().__init__(i, name)
class OtherConditions(ColumHeader):
    def __init__(self, i, name) -> None:
        super().__init__(i, name)

class Reader:
    def __init__(self) -> None:
        pass
    def add_gangwei(self, gangwei):
        self.gangwei = gangwei

    def get_header(self, df):
        for idx, row in df.iterrows():
            for i in row.items():
                if i[1] == '招聘岗位':
                    self.gangwei = GangWei(i, i[1])
                if i[1] == '其他条件':
                    self.other_conditions = OtherConditions(i, i[1])

def extract(excel_name):
    df = None
    try:
        df = pd.read_excel(
        open(excel_name, 'rb'), sheet_name=0)
    except:
        engine = get_excel_engine(excel_name)
        df = pd.read_excel(
        open(excel_name, 'rb'), sheet_name=0, engine=engine)
    reader = Reader()
    reader.get_header(df)
    print(reader)
if __name__ == '__main__':
    # Specify the directory path
    dir_path = 'zhaopin'

    # Iterate over the files in the directory
    with os.scandir(dir_path) as entries:
        for entry in entries:
            
            # Check if it is a file (not a directory)
            if entry.is_file() and entry.name.endswith('.xls'):
                extract(entry.path)
