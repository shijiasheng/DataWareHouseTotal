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

def clean_title_as_movie3(s):
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
    s = s_new
    s_new = ''
    for i in s:
        if i == '-':
            break
        s_new = s_new + i
    # 去除特定的符号
    delete2 = ['#', '- ', ';', '_', '/', ':']
    for d in delete2:
        s = s_new
        s_new = ''
        for i in s:
            if i == d:
                break
            s_new = s_new + i
    # 去除特定的
    delete = ['(IMAX)', '(DVD)', '(Home Use)', '(BD)', '(English Subtitled)', '(Full Screen Edition)', '(D-VHS)',
              'United', '[VHS]'
        , '[Region 2]', 'DVD', '_DUPLICATE_']
    for d in delete:
        s_new = s_new.replace(d, '')
    # &变成and
    s_new = s_new.replace('&', 'and')
    # 不要空格
    s_new = s_new.replace(' ', '')
    # 全变成小写
    s_new = s_new.lower()
    return s_new


if __name__ == '__main__':
    with open('C:\\Users\\Lenovo\\Desktop\\shanchu10.csv', 'r')as f:
        reader = csv.DictReader(f, fieldnames=('id', 'title', 'release date', 'genres', 'director',
                                               'producers', 'actor', 'supporting actors', 'ratings', 'media format',
                                               'run time', 'MPAA rating', 'subtitles', 'studio', 'Item model number',
                                               'Date First Available', 'IMDb', 'audio languages', 'other format', 'link id', 'link title', 'ip'))
        final = []
        out_final = []
        for i in reader:
            final.append(dict(i))
        with open('C:\\Users\\Lenovo\\Desktop\\ip.csv', 'w', newline='')as outFile:
            field_names = ['id', 'title', 'ip', 'release date', 'genres', 'director', 'producers', 'actor',
                           'supporting actors', 'ratings',
                           'media format', 'run time', 'MPAA rating', 'subtitles', 'studio', 'Item model number',
                           'Date First Available', 'IMDb', 'audio languages', 'other format', 'link id', 'link title']
            writer = csv.DictWriter(outFile, fieldnames=field_names)
            temp1 = final[0]
            temp1['ip'] = ''
            for i in range(len(final)):
                temp2 = final[i]
                temp2['ip'] = ''

                if string_similar(clean_title_as_movie3(temp1['title']), clean_title_as_movie3(temp2['title'])) >= 0.8:
                    temp1['ip'] = temp1['ip'] + ';' + temp2['title']
                    continue
                # print(temp1)
                # writer.writerow(temp1)
                out_final.append(dict(temp1))
                temp1 = temp2
            # writer.writerow(temp1)
            out_final.append(dict(temp1))
            writer.writerows(out_final)
