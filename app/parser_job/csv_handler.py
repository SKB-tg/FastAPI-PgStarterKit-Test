
import csv
import datetime
#словарь для теста
data={
    "Server": "nginx",
    "Date": "Tue, 13 Sep 2022 08:00:45 GMT",
    "Content-Type": "text/html",
    "Content-Length": "1711",
    "Connection": "keep-alive",
    "Last-Modified": "Tuesday, 13-Sep-2022 08:00:45 GMT",
    "ETag": "\"63201bbe-6af\"",
    "Accept-Ranges": "bytes",
    "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0"
    }
dt = datetime.datetime.now()
date1 = dt.isoformat(sep=' ')

def CsvHandler_W(filename, data, f_creat=True):
    key_data = alignment([i for i in data])
    val_data = [data[i] for i in data]

    Date = [f'***************{date1}************************']

    fnew='a'
    if f_creat==True:
        fnew='w'

    with open(filename, f'{fnew}', encoding='utf-8',newline='') as f:
        writer=csv.writer(f,escapechar='',lineterminator='\n', delimiter=':')
        writer.writerow(Date)
        n=0
        for i in key_data:
            key_val=[i,' ', val_data[n]]
            n=n+1
            writer.writerow(key_val)
			#for rows in data[i]:
        writer.writerow(' ')

def alignment(key_data):       #выпавнмванме слов в списке для для лучшего восприягия в файле (например ключей словаря)
    max_key=len(key_data[0])
    for k in key_data:
        if max_key < len(k):
            max_key=len(k)
    key_data1=[]
    for i in key_data:
        if len(i) < max_key:
            a = max_key - len(i)
            i=i + " " * a
        key_data1.append(i)
    return key_data1
CsvHandler_W(filename='1.csv', data=data)
#key_data = [i for i in data]
