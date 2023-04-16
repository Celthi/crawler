import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import requests
def processSheet(excel_name, sheet_name):
    
    df = pd.read_excel(
        open(excel_name, 'rb'), sheet_name)

    for i, row in df.iterrows():
        print(f'row {i}: {row["name"]}')
        res = requests.get(row["url"])
        with open('zhaopin/' + row['name'] +'.xls', 'wb') as f:
            f.write(res.content)
        

if __name__ == "__main__":
    excel_name = "data/data 4-16-17-12.xlsx"

    processSheet(excel_name, 'Sheet')
