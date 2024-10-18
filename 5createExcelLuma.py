import json
import pandas as pd
import os

POSITIVE_FILTERS = ['RWA', 'Tokenization', 'Crypto', 'Blockchain', 'NFT', 'DeFi', 'Ledger', 'Mining', 'Smart', 'Wallet', 'Staking', 'HODL', 'Yield']

outputFile = 'lumaData.json'
if os.path.exists(outputFile):
    with open(outputFile, 'r', encoding='utf-8') as jsonFile:
        sectionData = json.load(jsonFile)
else:
    sectionData = {}

filtered_data = {key: value for key, value in sectionData.items() if any(filter in value['title'] for filter in POSITIVE_FILTERS)}

excel_data = []
for value in filtered_data.values():
    excel_data.append({
        "Title": value['title'],
        "Link": value['link'],
        "Location": value['location'],
        "Date": value['date'],
        "Time": value['time'],
        "Day": value['day'],
        "Price": value['price'],
        "Organizer": value['organizer']
    })

df = pd.DataFrame(excel_data)

excel_file = 'lumaData.xlsx'
df.to_excel(excel_file, index=False)

from openpyxl import load_workbook

wb = load_workbook(excel_file)
ws = wb.active

ws.column_dimensions['A'].width = 50
ws.column_dimensions['B'].width = 15
ws.column_dimensions['C'].width = 25
ws.column_dimensions['D'].width = 15
ws.column_dimensions['E'].width = 15
ws.column_dimensions['F'].width = 10
ws.column_dimensions['G'].width = 5
ws.column_dimensions['H'].width = 30

wb.save(excel_file)

print(f"Excel file '{excel_file}' created successfully with adjusted column widths.")
