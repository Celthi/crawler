import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import requests
def processSheet(excel_name):
    
    df = pd.read_excel(
        open(excel_name, 'rb'), sheet_name=0)

    for i, row in df.iterrows():
        print(f'row {i}: {row["name"]}')
        res: str= requests.get(row["url"])
        suffix = '.xlsx' if row["url"].find('.xlsx') != -1 else '.xls'
        with open('zhaopin/collection420/' + row['name'] + suffix, 'wb') as f:
            f.write(res.content)
        

if __name__ == "__main__":
    excel_name = "data/data 4-19-23-53.xlsx"

    processSheet(excel_name)
