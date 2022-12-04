import csv
import pandas as pd

N=100

with open('C:/Users/richa/Downloads/StockEtablissementHistorique_utf8/StockEtablissementHistorique_utf8.csv', newline='') as csvfile1:
    spamreader = csv.reader(csvfile1, delimiter=' ', quotechar='|')
    t=0
    with open('reduit.csv','w',newline='') as csvfile2:
        writer = csv.writer(csvfile2)
        while t<N:
            writer.writerow(next(spamreader))
            t+=1
            print(t)

df = pd.read_csv('reduit.csv')