import csv
import difflib
import math


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).ratio()


def Max(s1, s2):
    if (len(s1) > len(s2)):
        return s1
    else:
        return s2


def JudgeTime(s1, s2):
    if s1 == s2:
        return True
    elif s1 in s2:
        return True
    elif s2 in s1:
        return True
    elif s1 == '':
        return True
    elif s2 == '':
        return True
    else:
        return False


def Similarity(s1, s2):
    len1 = len(s1)
    len2 = len(s2)
    dif = [[]]
    for a in range(len1 + 2):
        dif[a][0] = a
    for a in range(len2 + 2):
        dif[0][a] = a
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if s1[i - 1] == s2[j - 1]:
                temp = 0
            else:
                temp = 1
            dif[i][j] = min(dif[i - 1][j - 1] + temp, dif[i][j - 1] + 1, dif[i - 1][j] + 1)
    similarity = 1 - dif[len1][len2] / max(len(s1), len(s2))
    return similarity


def clean_title_as_movie(s):
    s_new = ''
    # 去除[]
    for i in s:
        if i == '[':
            break
        s_new = s_new + i
    s = s_new
    s_new = ''
    for i in s:
        if i == '(':
            break
        s_new = s_new + i
    # s = s_new
    # s_new = ''
    # for i in s:
    #     if i == '-':
    #         break
    #     s_new = s_new + i
    # 去除特定的
    delete = ['(IMAX)','(DVD)','(Home Use)','(BD)','(English Subtitled)','(Full Screen Edition)','(D-VHS)','United', '[VHS]'
              , '[Region 2]', 'DVD', '_DUPLICATE_']
    for d in delete:
        s_new = s_new.replace(d, '')
    # 去除特定的符号
    delete2 = ['!', '?', '#', '_', '/', ':']
    for d in delete2:
        s_new = s_new.replace(d, '')
    # &变成and
    s_new = s_new.replace('&', 'and')
    # 不要空格
    s_new = s_new.replace(' ', '')
    # 全变成小写
    s_new = s_new.lower()
    return s_new


def clean_title_as_movie2(s):
    s_new = ''
    # 去除[]
    for i in s:
        if i == '[':
            break
        s_new = s_new + i

    s = s_new
    s_new = ''
    for i in s:
        if i == '(':
            break
        s_new = s_new + i

    # 去除特定的
    delete = ['(IMAX)','(DVD)','(Home Use)','(BD)','(English Subtitled)','(Full Screen Edition)','(D-VHS)','United', '[VHS]'
              , '[Region 2]', 'DVD', '_DUPLICATE_']
    for d in delete:
        s_new = s_new.replace(d, '')
    # &变成and
    s_new = s_new.replace('&', 'and')
    return s_new


def normalize_date(s):
    year = ''
    month = ''
    day = ''
    if 'April' in s:
        month = '4'
        s = s.replace('April', '')
        s = s.replace(' ', '')
        day, year = s.split(',')
        s = year + '/' + month + '/' + day
    elif 'M' in s:
        month, others = s.split('M')
        month = month.replace('0', '')
        others = others.replace(' ', '')
        day, year = others.split(',')
        s = year + '/' + month + '/' + day
    return s


def normalize_time(s):
    hour = '0'
    min = '00'
    sec = '00'
    if 'minutes' in s and 'hours' in s:
        hour, others = s.split('hours')
        others = others.replace(' ', '')
        min = others.replace('minutes', '')
        if len(min) == 1:
            min = '0' + min
    elif 'minutes' in s and 'hour' in s:
        hour, others = s.split('hour')
        others = others.replace(' ', '')
        min = others.replace('minutes', '')
        if len(min) == 1:
            min = '0' + min
    elif 'minute' in s and 'hour' in s:
        hour, others = s.split('hour')
        others = others.replace(' ', '')
        min = others.replace('minute', '')
        if len(min) == 1:
            min = '0' + min
    elif 'minute' in s and 'hours' in s:
        hour, others = s.split('hours')
        others = others.replace(' ', '')
        min = others.replace('minute', '')
        min = min.replace('and', '')
        if len(min) == 1:
            min = '0' + min
    elif 'h' in s and 'min' in s:
        hour, others = s.split('h')
        others = others.replace(' ', '')
        min = others.replace('min', '')
        if len(min) == 1:
            min = '0' + min
    elif 'minute' in s or 'minutes' in s or 'min' in s:
        min = s.replace('minutes', '')
        min = min.replace('minute', '')
        min = min.replace('min', '')
        min = min.replace(' ', '')
        if int(min) // 60 != 0:
            hour = str(int(min) // 60)
            min = str(int(min) % 60)
    elif 'hour' in s or 'hours' in s or 'h' in s:
        hour = s.replace('hours', '')
        hour = hour.replace('hour', '')
        hour = hour.replace('h', '')
        hour = hour.replace(' ', '')
    else:
        return s
    if hour == '0':
        s = '0:' + min + ':' + sec
    else:
        s = hour + ':' + min + ':' + sec
    s = s.replace('and', '')
    s = s.replace('s', '0')
    s = s.replace(' ', '')
    return s


def clean_time(t):
    if t == 'run time':
        return 1
    if t == '':
        return 0
    elif "sec" in t:
        return 0
    else:
        time = t.split(':')
        # print(time[0])
        if int(time[0]) > 5:
            return 0
        if time[0] == '0' and int(time[1]) < 20:
            return 0
    return 1


def judge_week(s):
    if len(s) <= 4:
        return 7
    elif s == 'release date':
        return 'week'
    elif '/' in s:
        print(s)
        y, m, d = s.split('/')
        # y='2000'
        # m='3'
        # d='30'
        year = int(y)
        month = int(m)
        date = int(d)

        if month == 1:
            month = 13
            year = year - 1
        elif month == 2:
            month = 14
            year = year - 1
        century = math.floor(year / 100)
        year = year % 100
        print(century, year, month, date)
        return (math.floor(century/4)-2*century+math.floor(year/4)+year+math.floor(13*(month+1)/5)+date-1)%7
    else:
        return s

if __name__ == '__main__':
    with open('C:\\Users\\Lenovo\\Desktop\\mergeRatings.csv', 'r')as f:
        reader = csv.DictReader(f, fieldnames=(
            'id', 'title', 'release date', 'genres', 'director', 'producers', 'actor', 'supporting actors', 'ratings',
            'media format',
            'run time', 'MPAA rating', 'subtitles', 'studio', 'Item model number', 'Date First Available', 'IMDb',
            'audio languages', 'linkid', 'linktitle'))
        final = []
        out_final = []
        for i in reader:
            final.append(dict(i))
        with open('C:\\Users\\Lenovo\\Desktop\\25clean.csv', 'w', newline='')as outFile:
            writer = csv.DictWriter(outFile, fieldnames=(
                'id', 'title', 'release date', 'genres', 'director', 'producers', 'actor', 'supporting actors', 'ratings',
                'media format', 'run time', 'MPAA rating', 'subtitles', 'studio', 'Item model number',
                'Date First Available', 'IMDb', 'audio languages', 'linkid', 'linktitle'))
            # writer.writerows(final)
            for temp1 in final:
                if temp1['release date']:
                    temp1['release date'] = normalize_date(temp1['release date'])
                else:
                    temp1['release date'] = normalize_date(temp1['Date First Available'])
                temp1['run time'] = normalize_time(temp1['run time'])
                temp1['title'] = clean_title_as_movie2(temp1['title'])
                # temp1['week'] = judge_week(temp1['release date'])
                # if temp1['title'] and temp1['director'] and temp1['actor'] and clean_time(temp1['run time']) and temp1[
                #     'release date']:
                #     # if temp1['title'] and temp1['director'] and temp1['actor'] and temp1['run time'] and temp1[
                #     # 'release date']:
                #     writer.writerow(temp1)
                writer.writerow(temp1)
            # writer.writerows(out_final)
