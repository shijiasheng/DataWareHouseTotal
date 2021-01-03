#coding:utf-8
import csv

f = open('F:\\电影数据\\movies.txt', 'rb')
outfile = open('F:\\电影数据\\review2.csv', 'w', newline='')
writer = csv.DictWriter(outfile, fieldnames=('product/productId', 'review/userId', 'review/profileName', 'review/helpfulness', 'review/score', 'review/time', 'review/summary', 'review/text', 'review/sentiment'))

dict = {}
for line in f:
    line = str(line)[2:-3]
    if 'product/productId' in line:
        dict['product/productId'] = line.replace('product/productId: ', '')
    elif 'review/userId' in line:
        dict['review/userId'] = line.replace('review/userId: ', '')
    elif 'review/profileName' in line:
        dict['review/profileName'] = line.replace('review/profileName: ', '')
    elif 'review/helpfulness' in line:
        dict['review/helpfulness'] = line.replace('review/helpfulness: ', '')
    elif 'review/score' in line:
        dict['review/score'] = line.replace('review/score: ', '')
    elif 'review/time' in line:
        dict['review/time'] = line.replace('review/time: ', '')
    elif 'review/summary' in line:
        dict['review/summary'] = line.replace('review/summary: ', '')
    elif 'review/text' in line:
        dict['review/text'] = line.replace('review/text: ', '')
        s = SnowNLP(u'''This is junk, stay away.''')
        dict['review/sentiment'] = s.sentiments
        print("[sentiments]", s.sentiments)
    else:
        print(dict)
        writer.writerow(dict)
        dict = {}