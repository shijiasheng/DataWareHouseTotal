import pandas as pd
from tqdm import *
import progressbar


# # 获取所有product的id
# def get_all_products_id():
#     # 25万+的原始数据，所有的product
#     data = pd.read_csv('./25clean.csv', encoding="ISO-8859-1")
#     print(data.shape)
#     lis = data['id'].tolist()
#     print(len(lis))
#     lis = pd.DataFrame(data=lis)
#     lis.to_csv('./all_products_id.csv', encoding='utf-8')
#
#
# # get_all_products_id()
#
# # 获取所有的product和它们的director，所有的25万+条数据，跳过没有director的数据
# def get_all_productId_with_director():
#     data = pd.read_csv('./25clean.csv', encoding="ISO-8859-1")
#     productId_with_director_list = []
#     for rowIndex in data.index.tolist():
#         # 如果没有director则跳过
#         if pd.isna(data.loc[rowIndex]['director']):
#             # print(data.loc[rowIndex])
#             continue
#         director_list = data.loc[rowIndex]['director'].split(',')
#         # print(director_list)
#         for director in director_list:
#             director = str(director).replace('\"', '')  # neo4j apoc.load导入数据不能有""
#             director = str(director).replace('\n', '')
#             if director == '':
#                 continue
#             productId_with_director_list.append([data.loc[rowIndex]['id'], director])
#     output = open('productId_with_director.csv', 'w')
#     output.write('id,director\n')
#     for i in range(len(productId_with_director_list)):
#         for j in range(len(productId_with_director_list[i])):
#             output.write(str(productId_with_director_list[i][j]))  # write函数不能写int类型的参数，所以使用str()转化
#             output.write(',')  # 相当于Tab一下，换一个单元格
#         output.write('\n')  # 写完一行立马换行
#     output.close()
#
#
# # get_all_productId_with_director()
#
#
# # 获取所有的product和它们的actor(主演和配角)，所有的25万+条数据，跳过没有actor且没有supporting actors的数据
# def get_all_productId_with_actor():
#     data = pd.read_csv('./25clean.csv', encoding="ISO-8859-1")
#     productId_with_actor_list = []
#     for rowIndex in data.index.tolist():
#         # 如果没有actor则跳过
#         if not pd.isna(data.loc[rowIndex]['actor']):
#             actor_list = data.loc[rowIndex]['actor'].split(',')
#             for actor in actor_list:
#                 actor = str(actor).replace('\"', '')  # neo4j apoc.load导入数据不能有""
#                 actor = str(actor).replace('\n', '')
#                 if actor == '':
#                     continue
#                 productId_with_actor_list.append([data.loc[rowIndex]['id'], actor])
#         # 如果没有supporting actor则跳过
#         if not pd.isna(data.loc[rowIndex]['supporting actors']):
#             supporting_actor_list = data.loc[rowIndex]['supporting actors'].split(',')
#             for supporting_actor in supporting_actor_list:
#                 supporting_actor = str(supporting_actor).replace('\"', '')  # neo4j apoc.load导入数据不能有""
#                 supporting_actor = str(supporting_actor).replace('\n', '')
#                 if supporting_actor == '':
#                     continue
#                 productId_with_actor_list.append([data.loc[rowIndex]['id'], supporting_actor])
#     output = open('productId_with_actor_list.csv', 'w')
#     output.write('id,actor\n')
#     for i in range(len(productId_with_actor_list)):
#         for j in range(len(productId_with_actor_list[i])):
#             output.write(str(productId_with_actor_list[i][j]))  # write函数不能写int类型的参数，所以使用str()转化
#             output.write(',')  # 相当于Tab一下，换一个单元格
#         output.write('\n')  # 写完一行立马换行
#     output.close()
#
#
# # get_all_productId_with_actor()
#
#
# # 导出neo4j import的productId文件
# def export_product_neo4j_import_file():
#     data = pd.read_csv('./25clean.csv', encoding="ISO-8859-1")
#     productId_list = []
#     for rowIndex in data.index.tolist():
#         productId_list.append(data.loc[rowIndex]['id'])
#     output = open('productId.csv', 'w')
#     output.write('product_id:ID(node),:LABEL\n')
#     for i in range(len(productId_list)):
#         output.write(str(productId_list[i]))
#         output.write(',product')
#         output.write('\n')  # 写完一行立马换行
#     output.close()
#
#
# # export_product_neo4j_import_file()
#
#
# # 导出neo4j import的director文件
# def export_director_neo4j_import_file():
#     import csv
#     # 注意这里要手动删除第一行！！！！！！！！！！！！
#     csvFile = open("./productId_with_director.csv", "r")
#     reader = csv.reader(csvFile)
#     output = open('director.csv', 'w')
#     output.write('director_name:ID(node),:LABEL\n')
#     for item in reader:
#         output.write(str(item[1]))
#         output.write(',director')
#         output.write('\n')  # 写完一行立马换行
#     output.close()
#
#
# # export_director_neo4j_import_file()
#
#
# # 导出neo4j import的actor文件
# def export_actor_neo4j_import_file():
#     import csv
#     # 注意这里要手动删除第一行！！！！！！！！！！！！
#     csvFile = open("./productId_with_actor_list.csv", "r")
#     reader = csv.reader(csvFile)
#     output = open('actor.csv', 'w')
#     output.write('actor_name:ID(node),:LABEL\n')
#     for item in reader:
#         output.write(str(item[1]))
#         output.write(',actor')
#         output.write('\n')  # 写完一行立马换行
#     output.close()
#
#
# # export_actor_neo4j_import_file()
#
# # 导出neo4j import的actor act product文件
# def export_actor_act_product_neo4j_import_file():
#     import csv
#     # 注意这里要手动删除第一行！！！！！！！！！！！！
#     csvFile = open("./productId_with_actor_list.csv", "r")
#     reader = csv.reader(csvFile)
#     output = open('productId_with_actor_neo4j_import.csv', 'w')
#     output.write(':END_ID(node),:START_ID(node),:TYPE\n')
#     for item in reader:
#         output.write(str(item[0]))
#         output.write(',')
#         output.write(str(item[1]))
#         output.write(',act')
#         output.write('\n')  # 写完一行立马换行
#     output.close()
#
#
# # export_actor_act_product_neo4j_import_file()
#
#
# # 导出neo4j import的director direct product文件
# def export_director_direct_product_neo4j_import_file():
#     import csv
#     # 注意这里要手动删除第一行！！！！！！！！！！！！
#     csvFile = open("./productId_with_director.csv", "r")
#     reader = csv.reader(csvFile)
#     output = open('productId_with_director_neo4j_import.csv', 'w')
#     output.write(':END_ID(node),:START_ID(node),:TYPE\n')
#     for item in reader:
#         output.write(str(item[0]))
#         output.write(',')
#         output.write(str(item[1]))
#         output.write(',direct')
#         output.write('\n')  # 写完一行立马换行
#     output.close()
#
#
# # export_director_direct_product_neo4j_import_file()
#
#
# def get_movie_director():
#     # 获取所有的movie和它们的director，所有的25万+条数据，跳过没有director的数据
#     data = pd.read_csv('./25clean.csv', encoding="ISO-8859-1")
#     productId_with_director_list = []
#     for rowIndex in data.index.tolist():
#         # 如果没有director则跳过
#         if pd.isna(data.loc[rowIndex]['director']):
#             # print(data.loc[rowIndex])
#             continue
#         director_list = data.loc[rowIndex]['director'].split(',')
#         # print(director_list)
#         for director in director_list:
#             director = str(director).replace('\"', '')  # neo4j apoc.load导入数据不能有""
#             director = str(director).replace('\n', '')
#             if director == '':
#                 continue
#             productId_with_director_list.append([data.loc[rowIndex]['id'], director])
#     output = open('productId_with_director.csv', 'w')
#     output.write('id,director\n')
#     for i in range(len(productId_with_director_list)):
#         for j in range(len(productId_with_director_list[i])):
#             output.write(str(productId_with_director_list[i][j]))
#             output.write(',')  # 相当于Tab一下，换一个单元格
#         output.write('\n')  # 写完一行立马换行
#     output.close()


# def get_people():
#     data = pd.read_csv('./shanchu12.csv', encoding='gbk', keep_default_na=False)
#
#     print(data.head(5))
#     peoples = {}
#     for row in range(data.shape[0]):
#         director_lis = str(data.loc[row]['director']).split(',')
#         for director in director_lis:
#             peoples.setdefault(director, []).append('director')
#
#     for row in range(data.shape[0]):
#         actor_lis = str(data.loc[row]['actor']).split(',')
#         for actor in actor_lis:
#             peoples.setdefault(actor, []).append('actor')
#
#     for row in range(data.shape[0]):
#         actor_lis = str(data.loc[row]['supporting actors']).split(',')
#         for supportingActor in actor_lis:
#             peoples.setdefault(supportingActor, []).append('actor')
#
#     for key, value in peoples.items():
#         peoples[key] = list(set(value))
#     actor_num = 0
#     director_num = 0
#     both = 0
#     all = 0
#
#     directorOutput = open('directorOutput.csv', 'w')
#     directorOutput.write('name:ID(node),:Label\n')
#     actorOutput = open('actorOutput.csv', 'w')
#     actorOutput.write('name:ID(node),:Label\n')
#     bothOutput = open('bothOutput.csv', 'w')
#     bothOutput.write('name:ID(node),:Label,:Label\n')
#     for key, value in peoples.items():
#         all += 1
#         if len(value) == 2:
#             bothOutput.write(str(key))
#             bothOutput.write(',director,actor\n')
#             both += 1
#         else:
#             if 'actor' in value:
#                 actorOutput.write(str(key))
#                 actorOutput.write(',actor\n')
#                 actor_num += 1
#             else:
#                 directorOutput.write(str(key))
#                 directorOutput.write(',director\n')
#                 director_num += 1
#     directorOutput.close()
#     actorOutput.close()
#     bothOutput.close()
#
#     print(actor_num)
#     print(director_num)
#     print(both)
#     print(all)


#
#
# def get_movie_director_relation():
#     data = pd.read_csv('./shanchu12.csv', encoding='gbk', keep_default_na=False)
#     print(data.head(5))
#     movie_director_relation = open('movie_director_relation.csv', 'w')
#     movie_director_relation.write(':END_ID(node),:START_ID(node),:TYPE\n')
#     for row in range(data.shape[0]):
#         movie_director_relation.write(str(data.loc[row]['id']))
#         director_lis = str(data.loc[row]['director']).split(',')
#         for director in director_lis:
#             movie_director_relation.write(',' + str(director))
#         movie_director_relation.write('\n')
#
#
def trans_date():
    data = pd.read_csv('./new_data.csv')
    for row in range(data.shape[0]):
        print(row)
        data.loc[row, 'release_date'] = str(data.loc[row, 'release_date']).replace('/', '-')
        if str(data.loc[row, 'date_first_available']) == '##':
            data.loc[row, 'date_first_available'] = ''
        else:
            data.loc[row, 'date_first_available'] = str(data.loc[row, 'date_first_available']).replace('/', '-')
    data.to_csv('temp_movie.csv', index=False)
    # data = pd.read_csv('./movie.csv')
    # for row in range(data.shape[0]):
    #     print(row)
    #     data.loc[row, 'release_date'] = str(data.loc[row, 'release_date']).replace('/', '-')
    #     if str(data.loc[row, 'date_first_available']) == '##':
    #         data.loc[row, 'date_first_available'] = ''
    #     else:
    #         data.loc[row, 'date_first_available'] = str(data.loc[row, 'date_first_available']).replace('/', '-')
    # data.to_csv('movie.csv', index=False)


def get_actor_supporting_actor():
    data = pd.read_csv('./new_data.csv')
    actor_dict = {}
    print(data.head)
    print(data.shape)
    # actor主演
    for row in range(data.shape[0]):
        actor_list = str(data.loc[row]['actor']).split('$$')
        # print(actor_list)
        for actor in actor_list:
            actor = actor.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            # actor.replace('\n', '')  # 去掉回车
            # actor.replace('"', '')  # 替换引号
            # actor.replace("'", '')  # 替换引号
            if actor == '##' or actor == '':  # 代表空
                continue
            actor_dict[actor] = ''
    # supporting actors参演
    for row in range(data.shape[0]):
        actor_list = str(data.loc[row]['supporting_actors']).split('$$')
        # print(actor_list)
        for actor in actor_list:
            actor = actor.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if actor == '##' or actor == '':  # 代表空
                continue
            actor_dict[actor] = ''
    # print(actor_dict)  # 所有的actor都有了
    print("*" * 100)
    actor_dict_star = actor_dict.copy()  # 主演
    actor_dict_participate = actor_dict.copy()  # 参演
    for row in range(data.shape[0]):
        actor_list = str(data.loc[row]['actor']).split('$$')
        # print(actor_list)
        for actor in actor_list:
            actor = actor.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if actor == '##' or actor == '':  # 代表空
                continue
            if actor_dict_star[actor] == '':
                actor_dict_star[actor] = str(data.loc[row]['title'])
            else:
                titles = str(actor_dict_star[actor]) + '$$' + str(data.loc[row]['title'])
                actor_dict_star[actor] = titles
    # for key, values in actor_dict_star.items():
    #     if values != '':
    #         print(values)
    # print(actor_dict_star)
    print("#" * 100)
    for row in range(data.shape[0]):
        supporting_actor_list = str(data.loc[row]['supporting_actors']).split('$$')
        # print(actor_list)
        for supporting_actor in supporting_actor_list:
            supporting_actor = supporting_actor.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if supporting_actor == '##' or supporting_actor == '':  # 代表空
                continue
            if actor_dict_participate[supporting_actor] == '':
                actor_dict_participate[supporting_actor] = str(data.loc[row]['title'])
            else:
                titles = str(actor_dict_participate[supporting_actor]) + '$$' + str(data.loc[row]['title'])
                actor_dict_participate[supporting_actor] = titles
    # for key, values in actor_dict_participate.items():
    #     if values != '':
    #         print(values)
    # print(actor_dict_participate)
    # 接下来就是写出文件！
    res = open('actor.csv', 'w')
    res.write('name,Starring,participate\n')
    for key in actor_dict.keys():
        res.write(str(key))
        res.write(',')
        res.write(str(actor_dict_star[key]))
        res.write(',')
        res.write(actor_dict_participate[key])
        res.write('\n')
    res.close()


def get_director():
    data = pd.read_csv('./new_data.csv')
    director_dict = {}
    print(data.head)
    print(data.shape)
    for row in range(data.shape[0]):
        director_list = str(data.loc[row]['director']).split('$$')
        # print(director_list)
        for director in director_list:
            director = director.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if director == '##' or director == '':  # 代表空
                continue
            director_dict[director] = ''
    # print(director_dict)
    # director导演都有了
    for row in range(data.shape[0]):
        director_list = str(data.loc[row]['director']).split('$$')
        # print(director_list)
        for director in director_list:
            director = director.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if director == '##' or director == '':  # 代表空
                continue
            if director_dict[director] == '':
                director_dict[director] = str(data.loc[row]['title'])
            else:
                titles = str(director_dict[director]) + '$$' + str(data.loc[row]['title'])
                director_dict[director] = titles
    # 接下来就是写出文件！
    res = open('./director.csv', 'w')
    res.write('name,filming\n')
    for key, values in director_dict.items():
        res.write(str(key))
        res.write(',')
        res.write(str(values))
        res.write('\n')
    res.close()


def get_genre():
    data = pd.read_csv('./new_data.csv')
    genres_dict = {}
    print(data.head)
    print(data.shape)
    for row in range(data.shape[0]):
        genre_list = str(data.loc[row]['genres']).split('$$')
        # print(genre_list)
        for genre in genre_list:
            genre = genre.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if genre == '##' or genre == '':  # 代表空
                continue
            genres_dict[genre] = ''
    # genre都有了
    # for key in genres_dict.keys():
    #     print(key)
    for row in range(data.shape[0]):
        genre_list = str(data.loc[row]['genres']).split('$$')
        # print(genre_list)
        for genre in genre_list:
            genre = genre.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if genre == '##' or genre == '':  # 代表空
                continue
            if genres_dict[genre] == '':
                genres_dict[genre] = str(data.loc[row]['title'])
            else:
                titles = str(genres_dict[genre]) + '$$' + str(data.loc[row]['title'])
                genres_dict[genre] = titles
    # # 写出文件！
    print("!" * 200)
    # for key in genres_dict.keys():
    #     print(key)
    res = open('genre.csv', 'w')
    res.write('name,movies\n')
    for key, value in genres_dict.items():
        res.write(str(key))
        res.write(',')
        res.write(str(value))
        res.write('\n')
    res.close()


def get_time():
    data = pd.read_csv('./new_data.csv')
    time_dict = {}
    time_movie_dict = {}
    print(data.head)
    print(data.shape)
    for row in range(data.shape[0]):
        time = str(data.loc[row]['release_date'])
        # print(time)
        time_dict[time] = int(data.loc[row]['week'])
    for row in range(data.shape[0]):
        time = str(data.loc[row]['release_date'])
        time_movie_dict[time] = ''
    for row in range(data.shape[0]):
        time = str(data.loc[row]['release_date'])
        title = str(data.loc[row]['title'])
        if time_movie_dict[time] == '':
            time_movie_dict[time] = title
        else:
            time_movie_dict[time] = time_movie_dict[time] + "$$" + title
    res = open('time.csv', 'w')
    res.write('year,month,day,week,movie\n')
    for key in time_dict.keys():
        if time_dict[key] == 7:
            year = int(key)
            month = -1
            day = -1
        else:
            year, month, day = key.split('/')
        res.write(str(year))
        res.write(',')
        res.write(str(month))
        res.write(',')
        res.write(str(day))
        res.write(',')
        res.write(str(time_dict[key]))
        res.write(',')
        res.write(time_movie_dict[key])
        res.write('\n')
    res.close()


def get_time_id_in_movie_table():
    time_csv = pd.read_csv('movieDatabase4_time.csv')
    movie_csv = pd.read_csv('temp_movie.csv')
    print(time_csv.head())
    print(movie_csv.head())
    timeid_time_dict = {}
    for row in range(time_csv.shape[0]):
        week = str(time_csv.loc[row]['week'])
        if week == '7':
            time = str(time_csv.loc[row]['year'])
        else:
            time = str(time_csv.loc[row]['year']) + '-' + str(time_csv.loc[row]['month']) + '-' + str(
                time_csv.loc[row]['day'])
        timeid_time_dict[time] = str(time_csv.loc[row]['time_id'])
    # print(timeid_time_dict)
    # movie_csv['time_id'] = ''
    for row in range(movie_csv.shape[0]):
        time_id = timeid_time_dict[movie_csv.loc[row]['release_date']]
        # print(time_id)
        movie_csv.loc[row, 'time_id'] = str(time_id)
        # print(movie_csv.loc[row]['time_id'])
    movie_csv = movie_csv.loc[:,
                ['product_id', 'time_id', 'title', 'genres', 'director', 'supporting_actors', 'actor', 'run_time',
                 'release_date', 'date_first_available', 'star', 'link_id', 'link_title']]
    movie_csv.to_csv('movie.csv', index=False)


def get_movie_actor_table():
    movie_csv = pd.read_csv('movieDatabase4_movie.csv')
    actor_csv = pd.read_csv('movieDatabase4_actor.csv')
    print(movie_csv.head())
    print(actor_csv.head())
    movie_dict = {}
    actor_dict = {}
    is_supporting_dict = {}
    for row in range(movie_csv.shape[0]):
        movie_dict[movie_csv.loc[row]['product_id']] = movie_csv.loc[row]['movie_id']
    for row in range(actor_csv.shape[0]):
        actor_dict[actor_csv.loc[row]['name']] = actor_csv.loc[row]['actor_id']
    for row in range(movie_csv.shape[0]):
        actor_list = str(movie_csv.loc[row]['supporting_actors']).split('$$')
        # print(actor_list)
        for actor in actor_list:
            actor = actor.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if actor == '##' or actor == '':  # 代表空
                continue
            is_supporting_dict[str(movie_csv.loc[row]['product_id']) + '|||' + actor] = 1
    for row in range(movie_csv.shape[0]):
        actor_list = str(movie_csv.loc[row]['actor']).split('$$')
        # print(actor_list)
        for actor in actor_list:
            actor = actor.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if actor == '##' or actor == '':  # 代表空
                continue
            is_supporting_dict[str(movie_csv.loc[row]['product_id']) + '|||' + actor] = 0
    movie_actor_res = open('movie_actor.csv', 'w')
    movie_actor_res.write('movie_id,actor_id,is_supporting\n')
    for key, value in is_supporting_dict.items():
        product_id, actor = key.split('|||')
        actor = actor.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
        if actor == '##' or actor == '':  # 代表空
            continue
        movie_actor_res.write(str(movie_dict[product_id]))
        movie_actor_res.write(',')
        try:
            movie_actor_res.write(str(actor_dict[actor]))
        except:
            print('actor', actor)
        movie_actor_res.write(',')
        movie_actor_res.write(str(value))
        movie_actor_res.write('\n')
    movie_actor_res.close()


def get_movie_director_table():
    movie_csv = pd.read_csv('movieDatabase4_movie.csv')
    director_csv = pd.read_csv('movieDatabase4_director.csv')
    print(movie_csv.head())
    print(director_csv.head())
    movie_dict = {}
    director_dict = {}
    for row in range(movie_csv.shape[0]):
        movie_dict[movie_csv.loc[row]['product_id']] = movie_csv.loc[row]['movie_id']
    for row in range(director_csv.shape[0]):
        director_dict[director_csv.loc[row]['name']] = director_csv.loc[row]['director_id']
    movie_director_res = open('movie_director.csv', 'w')
    movie_director_res.write('movie_id,director_id\n')
    for row in range(movie_csv.shape[0]):
        director_list = list(set(str(movie_csv.loc[row]['director']).split('$$')))
        # print(director_list)
        for director in director_list:
            director = director.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if director == '##' or director == '':  # 代表空
                continue
            movie_director_res.write(str(movie_dict[movie_csv.loc[row]['product_id']]))
            movie_director_res.write(',')
            try:
                movie_director_res.write(str(director_dict[director]))
            except:
                print(director)
            movie_director_res.write('\n')
    movie_director_res.close()


def get_movie_genre_table():
    movie_csv = pd.read_csv('movieDatabase4_movie.csv')
    genre_csv = pd.read_csv('movieDatabase4_genre.csv')
    print(movie_csv.head())
    print(genre_csv.head())
    movie_dict = {}
    genre_dict = {}
    for row in range(movie_csv.shape[0]):
        movie_dict[movie_csv.loc[row]['product_id']] = movie_csv.loc[row]['movie_id']
    for row in range(genre_csv.shape[0]):
        genre_dict[genre_csv.loc[row]['name']] = genre_csv.loc[row]['genre_id']
    movie_genre_res = open('movie_genre.csv', 'w')
    movie_genre_res.write('movie_id,genre_id\n')
    for row in range(movie_csv.shape[0]):
        genre_list = str(movie_csv.loc[row]['genres']).split('$$')
        # print(genre_list)
        for genre in genre_list:
            genre = genre.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if genre == '##' or genre == '':  # 代表空
                continue
            movie_genre_res.write(str(movie_dict[movie_csv.loc[row]['product_id']]))
            movie_genre_res.write(',')
            try:
                movie_genre_res.write(str(genre_dict[genre]))
            except:
                print(genre)
            movie_genre_res.write('\n')
    movie_genre_res.close()


def get_director_actor_table():
    data = pd.read_csv('./movieDatabase4_movie.csv')
    director_csv = pd.read_csv('./movieDatabase4_director.csv')
    actor_csv = pd.read_csv('./movieDatabase4_actor.csv')
    director_dict = {}
    actor_dict = {}
    for row in range(director_csv.shape[0]):
        director_dict[director_csv.loc[row]['name']] = director_csv.loc[row]['director_id']
    for row in range(actor_csv.shape[0]):
        actor_dict[actor_csv.loc[row]['name']] = actor_csv.loc[row]['actor_id']
    director_actor_dict = {}
    for row in range(data.shape[0]):
        director_list = str(data.loc[row]['director']).split('$$')
        actor_list = list(
            set(str(data.loc[row]['actor']).split('$$') + str(data.loc[row]['supporting_actors']).split('$$')))
        # print(actor_list)
        for director in director_list:
            director = director.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if director == '##' or director == '':  # 代表空
                continue
            for actor in actor_list:
                actor = actor.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
                if actor == '##' or actor == '':  # 代表空
                    continue
                director_actor_dict[director + '>' + actor] = 0
    for row in range(data.shape[0]):
        director_list = str(data.loc[row]['director']).split('$$')
        actor_list = list(
            set(str(data.loc[row]['actor']).split('$$') + str(data.loc[row]['supporting_actors']).split('$$')))
        for director in director_list:
            director = director.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if director == '##' or director == '':  # 代表空
                continue
            for actor in actor_list:
                actor = actor.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
                if actor == '##' or actor == '':  # 代表空
                    continue
                director_actor_dict[director + '>' + actor] = director_actor_dict[director + '>' + actor] + 1
    res = open('director_actor.csv', 'w')
    res.write('director_id,actor_id,count\n')
    for key in director_actor_dict.keys():
        # print(key)
        director, actor = key.split('>')
        try:
            res.write(str(director_dict[director]))
        except:
            print(director)
        res.write(',')
        try:
            res.write(str(actor_dict[actor]))
        except:
            print(actor)
        res.write(',')
        res.write(str(director_actor_dict[key]))
        res.write('\n')
    res.close()


def get_actor_actor_table():
    data = pd.read_csv('./movieDatabase4_movie.csv')
    actor_csv = pd.read_csv('./movieDatabase4_actor.csv')
    actor_dict = {}
    for row in range(actor_csv.shape[0]):
        actor_dict[actor_csv.loc[row]['name']] = actor_csv.loc[row]['actor_id']
    actor_actor_dict = {}
    for row in range(data.shape[0]):
        actor_list = list(
            set(str(data.loc[row]['actor']).split('$$') + str(data.loc[row]['supporting_actors']).split('$$')))
        for actor_1 in actor_list:
            actor_1 = actor_1.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if actor_1 == '##' or actor_1 == '':  # 代表空
                continue
            for actor_2 in actor_list:
                actor_2 = actor_2.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
                if actor_2 == '##' or actor_2 == '':  # 代表空
                    continue
                if actor_1 == actor_2:
                    continue
                actor_actor_dict[actor_1 + '@@@@' + actor_2] = 0
                actor_actor_dict[actor_2 + '@@@@' + actor_1] = 0
    for row in range(data.shape[0]):
        actor_list = list(
            set(str(data.loc[row]['actor']).split('$$') + str(data.loc[row]['supporting_actors']).split('$$')))
        for actor_1 in actor_list:
            actor_1 = actor_1.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
            if actor_1 == '##' or actor_1 == '':  # 代表空
                continue
            for actor_2 in actor_list:
                actor_2 = actor_2.strip()  # 去掉首尾空格！！！！！！！！！！！！！！！！！！！！
                if actor_2 == '##' or actor_2 == '':  # 代表空
                    continue
                if actor_1 == actor_2:
                    continue
                actor_actor_dict[actor_1 + '@@@@' + actor_2] = actor_actor_dict[actor_1 + '@@@@' + actor_2] + 1
                actor_actor_dict[actor_2 + '@@@@' + actor_1] = actor_actor_dict[actor_2 + '@@@@' + actor_1] + 1
    actor_actor = open('actor_actor.csv', 'w')
    actor_actor.write('actor_id_1,actor_id_2,count\n')
    for key, value in actor_actor_dict.items():
        actor_1, actor_2 = key.split('@@@@')
        try:
            actor_actor.write(str(actor_dict[actor_1]) + ',' + str(actor_dict[actor_2]) + ',' + str(value / 2) + '\n')
        except:
            print(actor_1, ' ', actor_2)
    actor_actor.close()


def remove_yinhao_huiche_in_data():
    data = pd.read_csv('shanchu20210101(1).csv')
    for row in range(data.shape[0]):
        print(row)
        # 去除引号和空格
        txt = str(data.loc[row, 'actor']).replace('"', '').replace("'", '').replace('\n', '&&')
        data.loc[row, 'actor'] = txt
        txt = str(data.loc[row, 'supporting_actors']).replace('"', '').replace("'", '').replace('\n', '&&')
        data.loc[row, 'supporting_actors'] = txt
        txt = str(data.loc[row, 'director']).replace('"', '').replace("'", '').replace('\n', '&&')
        data.loc[row, 'director'] = txt
        txt = str(data.loc[row, 'genres']).replace('"', '').replace("'", '').replace('\n', '&&')
        data.loc[row, 'genres'] = txt
    data.to_csv('new_data.csv', index=False)


def get_director_actor_neo4J():
    director_actor_csv = pd.read_csv('movieDatabase4_director_actor.csv')
    director_csv = pd.read_csv('movieDatabase4_director.csv')
    actor_csv = pd.read_csv('movieDatabase4_actor.csv')
    director_dict = {}
    actor_dict = {}
    for row in range(director_csv.shape[0]):
        director_dict[director_csv.loc[row]['director_id']] = director_csv.loc[row]['name']
    for row in range(actor_csv.shape[0]):
        actor_dict[actor_csv.loc[row]['actor_id']] = actor_csv.loc[row]['name']
    director_actor = open('director_actor_neo4j.csv', 'w')
    director_actor.write(':END_ID(node),:START_ID(node),:TYPE,count:int\n')
    for row in range(director_actor_csv.shape[0]):
        director_actor.write(str(director_dict[director_actor_csv.loc[row]['director_id']]))
        director_actor.write(',')
        director_actor.write(str(actor_dict[director_actor_csv.loc[row]['actor_id']]))
        director_actor.write(',director_actor_corporate,')
        director_actor.write(str(director_actor_csv.loc[row]['count']))
        director_actor.write('\n')
    director_actor.close()


def get_movie_actor_neo4j():
    movie_actor_csv = pd.read_csv('movieDatabase4_movie_actor.csv')
    movie_csv = pd.read_csv('movieDatabase4_movie.csv')
    actor_csv = pd.read_csv('movieDatabase4_actor.csv')
    movie_dict = {}
    actor_dict = {}
    for row in range(movie_csv.shape[0]):
        movie_dict[movie_csv.loc[row]['movie_id']] = movie_csv.loc[row]['product_id']
    for row in range(actor_csv.shape[0]):
        actor_dict[actor_csv.loc[row]['actor_id']] = actor_csv.loc[row]['name']
    movie_actor = open('movie_actor_neo4j.csv', 'w')
    movie_actor.write(':END_ID(node),:START_ID(node),:TYPE,is_suooprting\n')
    for row in range(movie_actor_csv.shape[0]):
        movie_actor.write(str(movie_dict[movie_actor_csv.loc[row]['movie_id']]))
        movie_actor.write(',')
        movie_actor.write(str(actor_dict[movie_actor_csv.loc[row]['actor_id']]))
        movie_actor.write(',act,')
        movie_actor.write(str(movie_actor_csv.loc[row]['is_supporting']))
        movie_actor.write('\n')
    movie_actor.close()


def get_movie_director_neo4j():
    movie_director_csv = pd.read_csv('movieDatabase4_movie_director.csv')
    movie_csv = pd.read_csv('movieDatabase4_movie.csv')
    director_csv = pd.read_csv('movieDatabase4_director.csv')
    movie_dict = {}
    director_dict = {}
    for row in range(movie_csv.shape[0]):
        movie_dict[movie_csv.loc[row]['movie_id']] = movie_csv.loc[row]['product_id']
    for row in range(director_csv.shape[0]):
        director_dict[director_csv.loc[row]['director_id']] = director_csv.loc[row]['name']
    movie_director = open('movie_director_neo4j.csv', 'w')
    movie_director.write(':END_ID(node),:START_ID(node),:TYPE\n')
    for row in range(movie_director_csv.shape[0]):
        movie_director.write(str(movie_dict[movie_director_csv.loc[row]['movie_id']]))
        movie_director.write(',')
        movie_director.write(str(director_dict[movie_director_csv.loc[row]['director_id']]))
        movie_director.write(',direct\n')
    movie_director.close()


def get_movie_genre_neo4j():
    movie_genre_csv = pd.read_csv('movieDatabase4_movie_genre.csv')
    movie_csv = pd.read_csv('movieDatabase4_movie.csv')
    # genre_csv = pd.read_csv('movieDatabase3_genre.csv')
    movie_dict = {}
    # genre_dict = {}
    for row in range(movie_csv.shape[0]):
        movie_dict[movie_csv.loc[row]['movie_id']] = movie_csv.loc[row]['product_id']
    # for row in range(genre_csv.shape[0]):
    #     genre_dict[genre_csv.loc[row]['genre_id']] = genre_csv.loc[row]['name']
    movie_genre = open('movie_genre_neo4j.csv', 'w')
    movie_genre.write(':START_ID(node),:END_ID(node),:TYPE\n')
    for row in range(movie_genre_csv.shape[0]):
        movie_genre.write(str(movie_dict[movie_genre_csv.loc[row]['movie_id']]))
        movie_genre.write(',')
        movie_genre.write(str(movie_genre_csv.loc[row]['genre_id']))
        movie_genre.write(',is_genre\n')
    movie_genre.close()


def get_actor_actor_neo4j():
    actor_actor_csv = pd.read_csv('movieDatabase4_actor_actor.csv')
    actor_csv = pd.read_csv('movieDatabase4_actor.csv')
    actor_dict = {}
    for row in range(actor_csv.shape[0]):
        actor_dict[actor_csv.loc[row]['actor_id']] = actor_csv.loc[row]['name']
    actor_actor = open('actor_actor_neo4j.csv', 'w')
    actor_actor.write(':END_ID(node),:START_ID(node),count:int,:TYPE\n')
    for row in range(actor_actor_csv.shape[0]):
        actor_actor.write(str(actor_dict[actor_actor_csv.loc[row]['actor_id_1']]))
        actor_actor.write(',')
        actor_actor.write(str(actor_dict[actor_actor_csv.loc[row]['actor_id_2']]))
        actor_actor.write(',')
        actor_actor.write(str(actor_actor_csv.loc[row]['count']))
        actor_actor.write(',actor_actor_corporate\n')
    actor_actor.close()


def trans_data_for_neo4j():
    actor = pd.read_csv('actor_not_director.csv')
    director = pd.read_csv('director_not_actor.csv')
    both = pd.read_csv('Result_1.csv')
    movie = pd.read_csv('movieDatabase4_movie.csv')
    genre = pd.read_csv('movieDatabase4_genre.csv')
    time = pd.read_csv('movieDatabase4_time.csv')
    actor = actor.loc[:, ['name', 'Starring', 'participate']]
    actor.rename(columns={'name': 'name:ID(node)'}, inplace=True)
    actor[':LABEL'] = 'actor'
    director = director.loc[:, ['name', 'filming']]
    director.rename(columns={'name': 'name:ID(node)'}, inplace=True)
    director[':LABEL'] = 'director'
    both.rename(columns={'name': 'name:ID(node)'}, inplace=True)
    both['1:LABEL'] = 'director'
    both['2:LABEL'] = 'actor'
    movie = movie.loc[:,
            ['product_id', 'time_id', 'title', 'genres', 'director', 'supporting_actors', 'actor', 'run_time',
             'release_date', 'date_first_available', 'star', 'link_id', 'link_title']]
    movie.rename(columns={'product_id': 'product_id:ID(node)', 'release_date': 'release_date:Date'}, inplace=True)
    movie[':LABEL'] = 'movie'
    # genre = genre.loc[:, ['name', 'movies']]
    genre.rename(columns={'genre_id': 'genre_id:ID(node)'}, inplace=True)
    genre[':LABEL'] = 'genre'
    time.rename(columns={'time_id': 'time_id:ID(node)'}, inplace=True)
    time[':LABEL'] = 'time'
    movie_time = movie.loc[:, ['product_id:ID(node)', 'time_id']]
    movie_time.rename(columns={'product_id:ID(node)': ':START_ID(node)', 'time_id': ':END_ID(node)'}, inplace=True)
    movie_time[':TYPE'] = 'is_time'
    actor.to_csv('actor_neo4j.csv', index=False)
    director.to_csv('director_neo4j.csv', index=False)
    both.to_csv('both_neo4j.csv', index=False)
    movie.to_csv('movie_neo4j.csv', index=False)
    genre.to_csv('genre_neo4j.csv', index=False)
    time.to_csv('time_neo4j.csv', index=False)
    movie_time.to_csv('movie_time_neo4j.csv', index=False)


def get_series_for_neo4j():
    data = pd.read_csv('movieDatabase4_movie.csv')
    series_neo4j = open('series_neo4j.csv', 'w')
    series_neo4j.write('product_id:ID(node),title,TYPE\n')
    movie_series = open('movie_series_neo4j.csv', 'w')
    movie_series.write(':START_ID(node),:END_ID(node),:TYPE\n')
    id_list = []
    for row in range(data.shape[0]):
        link_id_list = str(data.loc[row]['link_id']).split('$$')
        link_title_list = str(data.loc[row]['link_title']).split('$$')
        if len(link_id_list) != len(link_title_list):
            print("error" * 30)
            break
        for i in range(len(link_id_list)):
            if link_id_list[i] == '' or link_id_list[i] == '##':
                continue
            movie_series.write(str(data.loc[row]['product_id']))
            movie_series.write(',')
            movie_series.write(link_id_list[i])
            movie_series.write(',is_series\n')
            if link_id_list[i] not in id_list:
                id_list.append(link_id_list[i])
                series_neo4j.write(link_id_list[i])
                series_neo4j.write(',')
                series_neo4j.write(link_title_list[i])
                series_neo4j.write(',series\n')
    series_neo4j.close()
    movie_series.close()


def get_review_and_relationship_for_neo4j():
    data = pd.read_csv('res.csv')
    relation = data.loc[:, ['reviewreview_id', 'product_id']]
    data = data.drop(columns=['product_id'])
    data[':LABEL'] = 'review'
    relation.rename(columns={'reviewreview_id': ':START_ID(node)', 'product_id': ':END_ID(node)'}, inplace=True)
    relation[':TYPE'] = 'review_to'
    data.rename(columns={'reviewreview_id': 'review_id:ID(node)'}, inplace=True)
    data.to_csv('review_neo4j.csv', index=False)
    relation.to_csv('review_relation_neo4j.csv', index=False)
    # i = 0
    # res = open('res.csv', 'w')
    # for line in open('movieDatabase4_review.csv'):
    #     res.write('review')
    #     res.write(line)
    #     print(i)
    #     i += 1
    # res.close()


def remove_yinhao_for_series_for_neo4j():
    data = pd.read_csv('series_neo4j.csv')
    for row in range(data.shape[0]):
        data.loc[row, 'title'] = str(data.loc[row, 'title']).replace("'", '')
        data.loc[row, 'title'] = str(data.loc[row, 'title']).replace('"', '')
    data.to_csv('new_series_neo4j.csv', index=False)


if __name__ == "__main__":
    # remove_yinhao_huiche_in_data()
    # print('@' * 200)
    # get_actor_supporting_actor()
    # print('@' * 200)
    # get_director()
    # print('@' * 200)
    # get_genre()
    # print('@' * 200)
    # get_time()
    # print('@' * 200)
    # trans_date()
    # print('@' * 200)
    # get_time_id_in_movie_table()
    # print('@' * 200)
    # get_movie_actor_table()
    # print('@' * 200)
    # get_movie_director_table()
    # print('@' * 200)
    # get_movie_genre_table()
    # print('@' * 200)
    # get_director_actor_table()
    # print('@' * 200)
    # get_actor_actor_table()
    # print('@' * 200)
    # get_director_actor_neo4J()
    # print('@' * 200)
    # get_movie_actor_neo4j()
    # print('@' * 200)
    # get_movie_director_neo4j()
    # print('@' * 200)
    # get_movie_genre_neo4j()
    # print('@' * 200)
    # get_actor_actor_neo4j()
    # print('@' * 200)
    # trans_data_for_neo4j()
    # print('@' * 200)
    # get_series_for_neo4j()
    # print('@' * 200)
    get_review_and_relationship_for_neo4j()
    # print('@' * 200)
    # remove_yinhao_for_series_for_neo4j()
    print("-----------------------------------finish-----------------------------------")

# import unicodedata
# def strip_accents(text):
#     try:
#         text = unicode(text, 'utf-8')
#     except NameError:  # unicode is a default on python 3
#         pass
#     text = unicodedata.normalize('NFD', text) \
#         .encode('ascii', 'ignore') \
#         .decode("utf-8")
#     return str(text)
# data = pd.read_csv('data.csv', encoding='gbk')
# columns = data.columns.tolist()
# for row in range(data.shape[0]):
#     print(row)
#     for column in columns:
#         data.loc[row, column] = strip_accents(str(data.loc[row, column]))
# data.to_csv('new_data_2.csv', index=False)
