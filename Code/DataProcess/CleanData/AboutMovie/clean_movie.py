import csv
import difflib


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
            print(s)
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
    delete = ['(IMAX)', '(DVD)', '(Home Use)', '(BD)', '(English Subtitled)', '(Full Screen Edition)', '(D-VHS)',
              'United', '[VHS]'
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


def clean_other(s1, s2):
    return s1

def format(temp1,temp2):
    # print(temp1['id'], temp1['other format'])
    # print(temp2['id'], temp2['other format'])
    if temp1['id'] in temp2['other format'] or temp2['id'] in temp1['other format']:
        return 1
    else:
        return 0
def suan(temp1,temp2):
    if clean_title_as_movie(temp1['title']) == clean_title_as_movie(temp2['title']) and JudgeTime(temp1['release date'],temp2['release date']):
        return 1
    else:
        return 0
if __name__ == '__main__':
    with open('C:\\Users\\Lenovo\\Desktop\\25clean.csv', 'r')as f:
        reader = csv.DictReader(f, fieldnames=('id', 'title', 'release date', 'genres', 'director',
                                               'producers', 'actor', 'supporting actors', 'ratings', 'media format',
                                               'run time', 'MPAA rating', 'subtitles', 'studio', 'Item model number',
                                               'Date First Available', 'IMDb', 'audio languages', 'other format', 'link id', 'link title'))
        final = []
        out_final = []
        for i in reader:
            final.append(dict(i))
        with open('C:\\Users\\Lenovo\\Desktop\\hebing16.csv', 'w', newline='')as outFile:
            field_names = ['id', 'title', 'release date', 'genres', 'director', 'producers', 'actor',
                           'supporting actors', 'ratings',
                           'media format', 'run time', 'MPAA rating', 'subtitles', 'studio', 'Item model number',
                           'Date First Available', 'IMDb', 'audio languages', 'other format', 'link id', 'link title']
            writer = csv.DictWriter(outFile, fieldnames=field_names)
            # writer.writerows(final)
            temp1 = final[0]
            temp1['link id'] = ''
            temp1['link title'] = ''
            # temp1['release date']=normalize_date(temp1['release date'])
            # temp1['run time'] = normalize_time(temp1['run time'])
            for i in range(len(final)):
                temp2 = final[i]
                temp2['link id'] = ''
                temp2['link title'] = ''

                # if clean_title_as_movie(temp1['title']) == clean_title_as_movie(temp2['title']) and JudgeTime(temp1['release date'], temp2['release date']):

                if format(temp1, temp2) or suan(temp1, temp2):
                    temp1['director'] = Max(temp1['director'], temp2['director'])
                    temp1['actor'] = Max(temp1['actor'], temp2['actor'])
                    temp1['supporting actors'] = Max(temp1['supporting actors'], temp2['supporting actors'])
                    temp1['genres'] = Max(temp1['genres'], temp2['genres'])
                    temp1['producers'] = Max(temp1['producers'], temp2['producers'])
                    temp1['run time'] = Max(temp1['run time'], temp2['run time'])
                    temp1['Date First Available'] = Max(temp1['Date First Available'], temp2['Date First Available'])
                    # temp1['director'] = Max(temp1['director'], temp2['director'])
                    if temp2['ratings']:
                        temp1['ratings'] = temp1['ratings'] + '+' + temp2['ratings']
                    temp1['link id'] = temp1['link id'] + temp2['id'] + "$$"
                    temp1['link title'] = temp1['link title'] + temp2['title'] + "$$"
                    temp1['other format'] = temp1['other format'] + "$$" + temp2['other format']
                    # print(temp1['link id'],temp1['link title'])
                    continue
                # print(temp1)
                # writer.writerow(temp1)
                if '$$' in temp1['link id']:
                    temp1['link id'] = temp1['link id'][:-2]
                if '$$' in temp1['link title']:
                    temp1['link id'] = temp1['link title'][:-2]
                print(dict(temp1))
                out_final.append(dict(temp1))
                temp1 = temp2
            # writer.writerow(temp1)
            out_final.append(dict(temp1))
            # print(out_final)
            writer.writerows(out_final)
