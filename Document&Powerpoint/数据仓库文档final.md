# 目录

[toc]

# 1. 需求分析

针对电影及其周边信息，建立基于关系型数据仓库、分布式文件型数据仓库系统和图数据库的数据仓库系统，并进行系统性能比对

i.	能够从数据来源处获取数据，进行数据预处理

ii.	建立关系型数据仓库存储模型，存储数据

iii.	建立分布式文件系统存储模型，存储数据

iv.	建立图数据库存储模型，存储数据

v.	在数据展现的界面上能够执行数据应用中的查询，并将在三种不同存储模型上的执行时间以数值的方式和图表的方式显示在界面上

vi.	对每种存储方式结合本项目说明各自适用于处理什么查询，针对本项目在存储优化中做了什么工作，优化前后的比较结果是怎样的，以文档的方式提交

## 1.1 系统功能性分析

本部分对系统功能性需求进行说明

### 1.1.1 条件查询

按照指定条件或条件范围进行查询

既可以指定单个条件，也可以指定多个条件的组合查询

**按照时间进行查询及统计**

查询指定年份上映的所有电影

查询指定月份上映的所有电影

查询指定星期几上映的所有电影

查询指定季度上映的所有电影

查询指定的时长范围的电影

**按照电影的特征进行查询及统计:**

查询指定名称的电影

**按照导演进行查询及统计:**

查询指定导演指导的电影

查询指定导演集合指导的电影

**按照演员进行查询及统计:**

查询指定演员参演的电影

查询指定演员集合参演的电影

**按照电影类别进行查询及统计:**

查询指定类别的电影

查询指定类别集合的电影

**针对电影评论进行查询及统计：**

查询指定电影下的所有评论

### 1.1.2 关系查询

**演员与演员合作关系查询**

查询与指定演员合作的演员及合作次数

**演员与导演合作关系查询**

查询与指定演员合作的导演及合作次数

**导演与演员合作关系查询**

查询与指定导演合作的演员及合作次数

### 1.1.3 统计查询

评论情感分析查询

按照月份进行统计查询

按照星期进行统计查询

### 1.1.4 系列电影查询

# 2. 架构和架构设计

## 2.1  系统总体框架

![](https://tongji4m3.oss-cn-beijing.aliyuncs.com/并发类架构图.png)

## 2.2   数据库选择

关系型数据库：MySQL

图数据库：Neo4j

分布式数据仓库：Hive

## 2.3 后端实现简介

（1）项目组首先在已经安装好的Hive，Mysql，Neo4j数据库上创建数据仓库查询所需的相关表结构，并且导入预先清洗好的数据。

（2）随后连接远程Hive，Mysql，Neo4j数据库，基于SpringBoot使用JDBC构建数据仓库后端查询项目。

（4）项目组同时集成了Swagger以实现后端接口的调试。

（5）项目组最终将数据仓库后端项目部署于云服务器上，为前端提供API接口。

![1](https://tongji4m3.oss-cn-beijing.aliyuncs.com/2021-1-2-11.png)

# 3. 数据ETL及数据质量

## 3.1 数据爬取

### 3.1.1 获取product_id

利用python提取原始`movie.txt`文件，总共获取253059个product_id。

### 3.1.2 爬取html

利用爬虫根据product_id爬取亚马逊网页，并下载备用，总共约140G的html文件。

**我们项目组提取了达到140G的页面HTML文件最终帮助了其他很多组！**

#### 3.1.2.1 异常页面检测

- 空页面检测：

某些URL对应的页面已经不存在，在爬取时会返回空页面，此时返回的Response不为200，可以通过Response的值进行检测。

- 验证码页面检测：

当亚马逊服务器检测到某一IP获取了过多的数据后，会返回验证码页面进行验证。在爬取过程中，通过某一URL获得了页面信息后，解析该页面的title信息，若title为“Amazon.com”，不包含任何关于产品的信息，则可以判定该页面为验证码页面。

#### 3.1.2.1 应对反爬机制

- 动态cookie：

在程序中用`Selenium`与`ChromeDriver`先获取一系列cookie，在爬取网页时随机选取其中的cookie进行访问。

- 更换IP：

在爬取信息过程中，若检测到异常页面数量超过一个阈值，则更换IP，并继续爬取。

**共获得253059条有效数据**

## 3.2 数据获取

数据获取阶段通过python程序实现

### 3.2.1 基本过程：

  <1>从评论数据集中获取所有productId，将其保存在txt文件中。

  <2>利用chromedriver模拟真实浏览器以及request库获取了所有亚马逊产品信息页面，并以.html格式存储了约114GB的待处理数据。

  <3>使用BeautifulSoup对页面中的数据进行解析，提取出所需字段。

  <4>使用csv库的DictWriter将获取的数据存入csv文件

### 3.2.2 过程中出现的问题及解决方案：

问题1：两种电影信息页面 Prime 与 非Prime

措施：经过两种页面html文件的内容比对，我们发现只有非Prime的页面有id为productTitle的标签，并以此来区别两种页面，设计了两种不同的函数来提取不同页面的信息。

问题2：因cookie的设置或亚马逊数据库的调整，对电影信息页面的请求可能会失败，如：请求超时、机器人检测、验证码、页面404等，导致信息爬取失败

措施：

<1>设置cookie列表，每次请求都使用cookie池里的一个随机cookie，降低机器人检测、验证码等情况的出现。

<2>页面404：记录出错的次序，之后将不会在请求改页面

<3>请求超时：重新请求

**共获得251665条有效数据**

## 3.3 数据清洗

### 3.3.1 时间（release date）字段统一

**问题：**

1. 电影存在release date和First Date Available两个字段
2. 部分电影的release date只有年份
3. 电影的日期不统一，共有四种格式：April 1,2000; 01M 1,2000; 2000; 1-April-00
4. 需要多出来季度的字段。
5. 需要多出来星期几的字段。

**措施：**

1. 在合并过程中采取信息量最大的情况为准，如合并中一个版本为2000，另一个版本为2000/03/30，则以20000330为准。
2. 若存在release date，则以release date为准，否则以First Date Available为准。
3. 统一格式化，为yyyy/mm/dd的格式。
4. 通过月份判断季度，如果只有年份，保存四个季度。
5. 通过基姆拉尔森计算公式和蔡勒公式对于日期进行判断，星期日是0，其余从星期一到星期六分别是从1到6；如果只有年份，则增加一个字段为7，表示没有具体星期。

### 3.3.2 时长（run time）字段统一

**问题：**

电影时长格式没有统一，存在很多种情况：h和m为单位；hour和min为单位；hour和minite为单位；sec为单位。其中针对不同的单位仍有单复数的问题寇待解决。

**措施：**

单位统一为h:mm:ss的形式，方便后期进行处理。

### 3.3.3 评分（ratings）字段统一

**问题：**

1. 部分电影评分不统一，存在十分满分制和五分满分制。
2. 部分电影的评分为空值。

**措施：**

1. 采用五分制为标准评分制
2. 从原数据集中重新计算用户评分的平均值并填充空值以及不符合规格的字段。

### 3.3.4 导演、主演、参演（director, actor, supporting actors）字段统一

**问题：**

1. 人名存在大小写的问题，如Gray和GRay（诸如此类）。
2. 英文人名中出现诸如"P.  J.Bob"人名中空格较多的情况。
3. 人名之间的关系存在通过"&"等字符来表示而不是","。
4. 人名中出现很多不符合常理的人名信息。
5. 人名中出现非英语名称。
6. 多人名。
7. 存在引号影响判断。
8. 存在回车替代了","的问题。

**措施：**

1. 人名统一采取大小写转换，首字母大写，其余小写的情况。
2. 人名统一姓名之间空格改为一个空格
3. 人名之间的"&"符号改为正常形式。
4. 人名中的不符合常理的人名信息采用删除或手动修改的策略。
5. 非英文名称的数据将注入法文俄文修改为英文数据。
6. 统一采取分隔符进行分割后统一处理。
7. 统一将引号去掉，减少影响。
8. 统一将回车修改。

### 3.3.5 类别（genre）字段统一

**问题：**

1. 电影类别字段存在多种合并。
2. 电影字段为空。

**措施：**

1. 将合并的种类中每一种种类单独取出，一个电影可以对应多种类别。
2. 爬取amazon商品页面的面包屑导航navigation作为类别的补充。

### 3.3.6 标题（title）统一

**问题：**

1. 标题存在多国语言，如法语俄语。
2. 标题存在诸多"[]"和"()"的形式的内容以及某些特指电影属性的字段，属于无关信息，如：'(IMAX)','(DVD)','(Home Use)','(BD)','(English Subtitled)','(Full Screen Edition)','(D-VHS)','United', '[VHS]', '[Region 2]', 'DVD', '_DUPLICATE_'等等，其中包含的内容为版本，格式等等。
3. 标题中存在诸多标点符号，如":"和" - "和"/"，后面的字段属于很特殊的情况，后面多表示分内容。举例如：X-Men: Days of Future Past或者X-Men - Days of Future Past或者X-Men/Days of Future Past等情况。
4. 标题中存在"&"等参与标题表示含义的字符。
5. 标题中存在空格过多等情况。

**措施：**

1. 统一将英语外的语言转换成英语。
2. 统一删除表示电影属性的信息。
3. 统一将表示子标题的符号的信息表示为":"。
4. 统一将"&"转换为英语"and"等。
5. 统一将两个单词之间的空格改为一个空格。

### 3.3.7 数据统一修改字段

**问题：**

1. 存在回车换行的情况。
2. 存在引号多余的情况。
3. 存在英语外的外语的问题。

**措施：**

1. 统一修改回车换行为逗号。
2. 统一修改引号。
3. 统一改为英语，方便后续导入数据库。

## 3.4 数据合并

数据合并主要意图为通过数据合并完成同一部电影的不同版本之间的合并。

### 3.4.1 判断方法一：进行编辑距离算法

采用传统的编辑距离的算法，将采取非常严格的方式，满足两个条件，数据清洗之后的title和director以及actor等关键信息重合度非常高，达到超过0.9以上；时间严格遵循相同原则。也就是说时间release date满足要统一的时间点。

### 3.4.2 判断方法二：采用爬虫数据，爬虫页面中链接部分

通过爬虫发现，每个电影的页面中包含了同电影不同版本的信息，则认为为同一部电影。为other format字段。如果电影的productid在other format里，则认为属于同一部电影。

### 3.4.3 数据合并原则与细节

确定两部电影为同一部电影后的技术细节：

1. 普遍字段采用信息量多的作为该部电影的某个字段的信息。
2. 电影导演演员包括主演和参演普遍采用合并后的结果，满足足够详细。
3. 电影的评分ratings采用多部版本的平均值。
4. 设置link id字段和link title字段，将合并的电影的版本和标题进行存储，用于检测和展示。
5. 合并中other format采取荣誉合并，如temp1和temp2合并之后temp1中存储之前两个的other format的并集。

**共获得164895条有效数据**

## 3.5 电影筛选

本次筛选我们项目组采用的相对比较严格甚至苛刻的筛选条件，作为一部合格的电影数据，需要保证以下几点：

1. 需要保证有导演（director）字段。
2. 需要保证有主演（actor）字段。
3. 需要保证有时长字段（run time）字段。
4. 需要保证有上映日期（release date）字段，并且播放时长从需要大于20 min，小于5 hours。
5. 需要保证有电影标题（title）字段。

**共获得87213条有效数据**

# 4. 影评情感评价（sentiment）模型

目前市面上的情感分析工具普遍没有针对影评设计的，不具备针对性。所以没有采取很多的工具包，而是采用的是自己训练模型的方式。

我们首先找到了合适的电影影评的数据集：http://ai.stanford.edu/~amaas/data/sentiment/。

然后寻找到了合适的训练模型，对于我们的影评数据进行好评差评的打分。

## 4.1 数据集

影评的数据集：http://ai.stanford.edu/~amaas/data/sentiment/。影评的数据集同样来自斯坦福大学提供的数据。为25000个数据，每个数据代表着一个英文影评。对于所有的影片，都进行了标记，其中分为negative和positive两种sentiment。

数据集介绍：

Large Movie Review Dataset

This is a dataset for binary sentiment classification containing substantially more data than previous benchmark datasets. We provide a set of 25,000 highly polar movie reviews for training, and 25,000 for testing. There is additional unlabeled data for use as well. Raw text and already processed bag of words formats are provided. See the README file contained in the release for more details.

![image-20210103134447734](https://i.loli.net/2021/01/03/y4bBElsjozfWn5r.png)

## 4.2 训练模型

我们的训练采用了两种方法，并酌情进行了结合。

### 4.2.1 深度学习

顺着数据集我们找到了kaggle上针对这个数据集的竞赛，kaggle也同样提供了针对这个IMDB的评论数据训练我们的NLP模型进行评论的情感分析。我们的模型使用keras框架搭建，首先使用Word2vec生成词向量，然后使用LSTM对转换为词向量的句子进行情感预测。

我们采用了在竞赛中取得较高准确率（93.51%）的开源的训练代码，作者为Nilan。

### 4.2.2 snowNLP

于此同时，我们采用了NLP的比较合适的工具包，通过其sentiment的情感分析，首先对于negative和positive两种情感进行数据集训练，然后再将数据进行导入判断每条评论的内容。

# 5. 数据库设计

## 5.1.  关系型数据库

关系型数据库主要用于对电影的条件查询。我们选用了Mysql作为我们的关系型数据库。Mysql是一个很简单的关系型数据库，也因此导致了其功能有限。

### 5.1.1数据库图

![](https://tongji4m3.oss-cn-beijing.aliyuncs.com/Diagram 1.png)

### 5.1.2表设计

**movie**存储电影相关信息

| Field                | Type                  | Comment  |
| -------------------- | --------------------- | -------- |
| movie_id             | int(11) NOT NULL      |          |
| product_id           | varchar(255) NOT NULL |          |
| time_id              | int(11) NOT NULL      |          |
| title                | longtext NOT NULL     |          |
| genres               | longtext NULL         |          |
| director             | longtext NULL         |          |
| supporting_actors    | longtext NULL         |          |
| actor                | longtext NULL         |          |
| run_time             | varchar(255) NULL     |          |
| release_date         | varchar(255) NULL     | 发布日期 |
| date_first_available | varchar(255) NULL     |          |
| star                 | double NULL           | 评分     |
| link_id              | longtext NULL         |          |
| link_title           | longtext NULL         |          |



**actor**存储演员相关信息，包括他主演和参演的电影

| Field       | Type                  | Comment                         |
| ----------- | --------------------- | ------------------------------- |
| actor_id    | int(11) NOT NULL      |                                 |
| name        | varchar(255) NOT NULL |                                 |
| Starring    | longtext NULL         | 主演的电影用字符串标识,便于查询 |
| participate | longtext NULL         | 参演的电影用字符串标识,便于查询 |



**director**存储导演的名字和他导演的电影集合

| Field       | Type                  | Comment                             |
| ----------- | --------------------- | ----------------------------------- |
| director_id | int(11) NOT NULL      |                                     |
| name        | varchar(255) NOT NULL |                                     |
| filming     | longtext NOT NULL     | 导演拍摄的电影用字符串标识,便于查询 |



**genre**存储题材和属于该题材的电影集合

| Field    | Type                  | Comment                   |
| -------- | --------------------- | ------------------------- |
| genre_id | int(11) NOT NULL      |                           |
| name     | varchar(255) NOT NULL |                           |
| movies   | longtext NULL         | 该类型的电影集合,便于查询 |



**review**存储对于某个电影的评价。

| Field        | Type                  | Comment              |
| ------------ | --------------------- | -------------------- |
| review_id    | int(11) NOT NULL      |                      |
| product_id   | varchar(255) NOT NULL |                      |
| user_id      | varchar(255) NOT NULL |                      |
| profile_name | varchar(255) NULL     |                      |
| helpfulness  | varchar(255) NULL     |                      |
| score        | varchar(255) NULL     |                      |
| time         | varchar(255) NULL     |                      |
| star         | double NULL           | 对该电影评价的倾向性 |



**time**存储某个时间点的所有电影集合。

| Field   | Type             | Comment                      |
| ------- | ---------------- | ---------------------------- |
| time_id | int(11) NOT NULL |                              |
| year    | int(11) NULL     |                              |
| month   | int(11) NULL     |                              |
| day     | int(11) NULL     |                              |
| week    | int(11) NULL     |                              |
| movie   | longtext NULL    | 存储该时间点的一系列电影集合 |



**actor_actor**存储演员和演员之间的关系，即他们合作的次数

| Field      | Type             | Comment |
| ---------- | ---------------- | ------- |
| actor_id_1 | int(11) NOT NULL |         |
| actor_id_2 | int(11) NOT NULL |         |
| count      | int(11) NULL     |         |



**director_actor**存储导演和演员合作的关系和次数

| Field       | Type             | Comment |
| ----------- | ---------------- | ------- |
| director_id | int(11) NOT NULL |         |
| actor_id    | int(11) NOT NULL |         |
| count       | int(11) NULL     |         |



**movie_actor**存储了电影和演员的关系，因为电影和演员是多对多的关系，所以必须额外有一张关系表进行存储，并且有一个额外的字段标识该演员和电影的关系是主演还是参演。

| Field         | Type             | Comment                |
| ------------- | ---------------- | ---------------------- |
| movie_id      | int(11) NOT NULL |                        |
| actor_id      | int(11) NOT NULL |                        |
| is_supporting | tinyint(1) NULL  | 该演员是否是参演该电影 |



**movie_director**存储了电影和导演的关系，因为电影和导演是多对多的关系，所以必须额外有一张关系表进行存储。

| Field       | Type             | Comment |
| ----------- | ---------------- | ------- |
| movie_id    | int(11) NOT NULL |         |
| director_id | int(11) NOT NULL |         |



**movie_genre**存储了电影和题材的关系，因为电影和题材是多对多的关系，所以必须额外有一张关系表进行存储。

| Field    | Type             | Comment |
| -------- | ---------------- | ------- |
| movie_id | int(11) NOT NULL |         |
| genre_id | int(11) NOT NULL |         |

## 5.2.  图数据库

图数据库采用neo4j

### 5.2.1图数据库存储模型

![未命名文件](https://cffuuimg.oss-cn-shanghai.aliyuncs.com/%E6%9C%AA%E5%91%BD%E5%90%8D%E6%96%87%E4%BB%B6.png)

图数据库总共有七种节点（node）

```
movie：存储电影的基本信息
director：存储导演的名称
actor：存储演员的名称
time：存储某个时间的具体的年、月、日、星期
genre：存储某个类型的名称
series：存储某个电影的系列信息
review：存储评论的基本信息
```

图数据库总共有七种关系（relationship）

```
direct：记录导演与电影的指导关系
act：记录演员与电影的参演关系，具有一个is_supporting属性记录是否为参演
cooperate：冗余，记录演员、导演之间的合作，具有一个count属性记录合作次数
is_time：记录电影属于哪个日期
is_genre：记录电影属于哪个类型
is_series：记录电影具有哪些系列
review_to：记录评论与电影的关系
```

## 5.3 分布式数据仓库——数据存储模型

### 5.3.1 简介

分布式文件系统将服务范围扩展到了整个网络。不仅改变了数据的存储和管理方式，也拥有了本地文件系统所无法具备的数据备份、数据安全等优点，它更加适合用于存储数量级较大的数据文件，比如用户评论等。在本次项目中，我们采用Hive作为我们的分布式数据仓库，它是基于Hadoop的一个数据仓库工具，可以将结构化的数据文件（或者非结构化的数据）映射为一张数据库表，并提供简单的sql查询功能，可以将sql语句转换为MapReduce任务进行运行。

###   5.3.2 系统搭建情况

项目组搭建的是基于Hadoop和MapReduce的Hive数据库作为分布式数据仓库，并部署于阿里云云服务器上。

项目组使用docker进行Hadoop集群搭建，并通过使用docker-compose脚本来启动，停止和重启应用，简化每次启动多个容器时的复杂操作。

集群总共运行了五个容器，一个作为NameNode，一个作为DataNode，其余三个为hive提供必要的服务支持。

![image-20210103100013736](https://tongji4m3.oss-cn-beijing.aliyuncs.com/image-20210103100013736.png)

### 5.3.3 数据存储模型

![img](https://tongji4m3.oss-cn-beijing.aliyuncs.com/hive11.png)

### 5.3.4 表设计

**movie**存储电影相关信息

| Field                | Type   | Comment  |
| -------------------- | ------ | -------- |
| movie_id             | int    |          |
| product_id           | string |          |
| time_id              | int    |          |
| title                | string |          |
| genres               | string |          |
| director             | string |          |
| supporting_actors    | string |          |
| actor                | string |          |
| run_time             | string |          |
| release_date         | string | 发布日期 |
| date_first_available | string |          |
| star                 | double | 评分     |
| link_id              | string |          |
| link_title           | string |          |



**actor**存储演员相关信息，包括他主演和参演的电影

| Field       | Type   | Comment                         |
| ----------- | ------ | ------------------------------- |
| actor_id    | int    |                                 |
| name        | string |                                 |
| Starring    | string | 主演的电影用字符串标识,便于查询 |
| participate | string | 参演的电影用字符串标识,便于查询 |



**director**存储导演的名字和他导演的电影集合

| Field       | Type   | Comment                             |
| ----------- | ------ | ----------------------------------- |
| director_id | int    |                                     |
| name        | string |                                     |
| filming     | string | 导演拍摄的电影用字符串标识,便于查询 |



**genre**存储题材和属于该题材的电影集合

| Field    | Type   | Comment                   |
| -------- | ------ | ------------------------- |
| genre_id | int    |                           |
| name     | string |                           |
| movies   | string | 该类型的电影集合,便于查询 |



**review**存储对于某个电影的评价。

| Field        | Type   | Comment              |
| ------------ | ------ | -------------------- |
| review_id    | int    |                      |
| product_id   | string |                      |
| user_id      | string |                      |
| profile_name | string |                      |
| helpfulness  | string |                      |
| score        | string |                      |
| time         | string |                      |
| star         | double | 对该电影评价的倾向性 |



**time**存储某个时间点的所有电影集合。

| Field   | Type   | Comment                      |
| ------- | ------ | ---------------------------- |
| time_id | int    |                              |
| year    | int    |                              |
| month   | int    |                              |
| day     | int    |                              |
| week    | int    |                              |
| movie   | string | 存储该时间点的一系列电影集合 |



**actor_actor**存储演员和演员之间的关系，即他们合作的次数

| Field      | Type | Comment |
| ---------- | ---- | ------- |
| actor_id_1 | int  |         |
| actor_id_2 | int  |         |
| count      | int  |         |



**director_actor**存储导演和演员合作的关系和次数

| Field       | Type | Comment |
| ----------- | ---- | ------- |
| director_id | int  |         |
| actor_id    | int  |         |
| count       | int  |         |



**movie_actor**存储了电影和演员的关系，因为电影和演员是多对多的关系，所以必须额外有一张关系表进行存储，并且有一个额外的字段标识该演员和电影的关系是主演还是参演。

| Field         | Type    | Comment                |
| ------------- | ------- | ---------------------- |
| movie_id      | int     |                        |
| actor_id      | int     |                        |
| is_supporting | boolean | 该演员是否是参演该电影 |



**movie_director**存储了电影和导演的关系，因为电影和导演是多对多的关系，所以必须额外有一张关系表进行存储。

| Field       | Type | Comment |
| ----------- | ---- | ------- |
| movie_id    | int  |         |
| director_id | int  |         |



**movie_genre**存储了电影和题材的关系，因为电影和题材是多对多的关系，所以必须额外有一张关系表进行存储。

| Field    | Type | Comment |
| -------- | ---- | ------- |
| movie_id | int  |         |
| genre_id | int  |         |

# 6. 数据库优化

## 6.1 关系型数据库优化

### 6.1.2 指定int型自增主键

在建表阶段，项目组就刻意把每个表的主键设置为int型的自增Id，之后MySQL会自动为该主键建立主键索引。好处如下：

+ 自增型主键以利于插入性能的提高；
+ 自增型主键设计(int)可以降低二级索引的空间，提升二级索引的内存命中率；
+ 自增型的主键可以减小page的碎片，提升空间和内存的使用。

### 6.1.3 设置冗余字段

项目组为genre、director、actor等表设置一个longtext的冗余字段存储他们对应的电影信息。

例如：对应演员表，存储了他参演以及主演的电影信息，此时单表查询即可：

![image-20210103153021309](https://tongji4m3.oss-cn-beijing.aliyuncs.com/image-20210103153021309.png)

```mysql
select * from actor where name = "Mark Thompson"
```

此时查询只需要0.09s

![image-20210103153438206](https://tongji4m3.oss-cn-beijing.aliyuncs.com/image-20210103153438206.png)

而如果不设置冗余字段，则需要通过movie_actor进行join操作执行查询：

```mysql
select distinct title
from movie,movie_actor
where movie.movie_id = movie_actor.movie_id
  and movie_actor.actor_id = (select actor_id from actor where name = "Mark Thompson");
```

耗时：0.17s

![image-20210103154219037](https://tongji4m3.oss-cn-beijing.aliyuncs.com/image-20210103154219037.png)

### 6.1.4 设置索引

要查询在某一时间点的电影，是通过先在time表通过时间条件查询出time_id，然后再在movie表中查找符合条件的movie

并且考虑在time中查询，一般都是（年，月，日）中按顺序查询，所以考虑设置组合索引（年，月，日），这样不管查询（年），（年，月），（年，月，日）都能使用到索引，并且只需要主键time_id，不需要回表查询，速度很快。

```mysql
select time_id from time where year = "2019"
```

不使用索引：

![image-20210103155902260](https://tongji4m3.oss-cn-beijing.aliyuncs.com/image-20210103155902260.png)

```mysql
ALTER TABLE time ADD INDEX (year,month,day);
```

![image-20210103160434858](https://tongji4m3.oss-cn-beijing.aliyuncs.com/image-20210103160434858.png)

![image-20210103160849496](https://tongji4m3.oss-cn-beijing.aliyuncs.com/image-20210103160849496.png)

### 6.1.5 索引前后性能比较

| 查询语句                                                     | 无索引 | 对name字段建索引 |
| ------------------------------------------------------------ | ------ | ---------------- |
| select actor_id from actor where name = "Mark Thompson"      | 804ms  | 696ms            |
| select genre_id from genre where name = "Drama"              | 2287ms | 1118ms           |
| select director_id from director where name = "Charles Adelman" | 881ms  | 698ms            |

## 6.2 图数据库优化

### 6.2.1 索引优化

由于需要频繁的查询演员和导演的名称，且演员节点与导演节点数量过多，因此创建索引.

```
CALL db.createIndex(":actor(name)", "lucene+native-2.0")
```

```
CALL db.createIndex(":director(name)", "lucene+native-2.0")
```

优化前后对比如下：

前

```
查询演员Kevin Pollack所有的电影:99ms
擦寻导演Charles Adelman所有的电影:60ms
查询与演员Gates合作最多的演员:90ms
查询与演员Gates合作最多的导演:95ms
查询与导演Charles Adelman合作最多的演员:40ms
```

后

```
查询演员Kevin Pollack所有的电影:45ms
擦寻导演Charles Adelman所有的电影:48ms
查询与演员Gates合作最多的演员:24ms
查询与演员Gates合作最多的导演:23ms
查询与导演Charles Adelman合作最多的演员:25ms
```

### 6.2.2 冗余优化

当查询演员、导演之间的合作次数时，由于关系过多，查询结果较慢，因此在neo4j图数据库中新增`cooperate`关系。

![未命名文件 (1)](https://cffuuimg.oss-cn-shanghai.aliyuncs.com/%E6%9C%AA%E5%91%BD%E5%90%8D%E6%96%87%E4%BB%B6%20(1).png)

并在`cooperate`关系中存储两者的合作次数，用作查询。

优化前后对比如下：

前

```
查询所有演员和导演中合作最多的:3700ms
查询与演员Levar合作最多的演员:21ms
查询与演员Gates合作最多的导演:110ms
查询与导演Gates合作最多的演员:90ms
```

后

```
查询所有演员和导演中合作最多的:423ms
查询与演员Levar合作最多的演员:24ms
查询与演员Gates合作最多的导演:23ms
查询与导演Gates合作最多的演员:25ms
```

## 6.3 分布式数据库优化

在各优化阶段，以review表为例，执行相同的查询任务，即查找某一部电影下的所有评论，观察执行时间，对比优化效果。以下为查询的SQL语句

```mysql
select * from review where product_id = "B003AI2VGA";
```

### 6.3.1 建立基本表

```mysql
# 在第一个阶段，首先将txt格式的review数据文件通过命令放到分布式文件存储系统中
docker cp /root/data1/review.txt docker-hive-master_hive-server_1:/opt;

# 再在Hive中建立review表
# 建表语句参加sql文本

# 最后通过命令将数据文件映射到Hive表格中，从而建立起textfile格式的基本表格
LOAD DATA LOCAL INPATH '/opt/review.csv' OVERWRITE INTO TABLE review;

# 执行查询耗时：44.688s 
```

### 6.3.2 设置索引

####  6.3.2.1 索引适用的场景

索引适用于不更新的静态字段。以免总是重建索引数据。每次建立、更新数据后，都要重建索引以构建索引表。

Hive索引可以建立在表中的某些列上，以提升一些操作的效率，例如减少MapReduce任务中需要读取的数据块的数量。

虽然Hive并不像事物数据库那样针对个别的行来执行查询、更新、删除等操作。它更多的用在多任务节点的场景下，快速地全表扫描大规模数据。但是在某些场景下，建立索引还是可以提高Hive表指定列的查询速度。

**由于我们对review的查询大部分基于product_id列，所以在该字段建立索引可以提高查询速度**

#### 6.3.2.2 Hive索引的机制

hive在指定列上建立索引，会产生一张索引表（Hive的一张物理表），里面的字段包括，索引列的值、该值对应的HDFS文件路径、该值在文件中的偏移量;

#### 6.3.2.3 实践

```mysql
# 为review 的product_id字段设置索引
create index product_id_index on table review(product_id) as 'org.apache.hadoop.hive.ql.index.compact.CompactIndexHandler' with deferred rebuild IN TABLE index_table_review;

# 说明
org.apache.hadoop.hive.ql.index.compact.CompactIndexHandler ：创建索引需要的实现类
product_id_index:索引名称
review:表名
index_table_review:创建索引后的表名
```

 ```mysql
# 此时索引表无数据
select * from index_table_review limit 5;
 ```

![image-20210103091052956](https://tongji4m3.oss-cn-beijing.aliyuncs.com/image-20210103090815693.png)



```mysql
# 为索引插入数据
alter index product_id_index on review rebuild;

# 此时发现索引表中有了数据
select * from index_table_review limit 5;

# review中确实存在了索引
show index on review;
```

![image-20210103083102283](https://tongji4m3.oss-cn-beijing.aliyuncs.com/image-20210103091215921.png)

![image-20210103090815693](https://tongji4m3.oss-cn-beijing.aliyuncs.com/image-20210103091052956.png)



```mysql
# 索引默认不使用
# 想要索引在查询时生效，还得设置使用索引
SET hive.input.format=org.apache.hadoop.hive.ql.io.HiveInputFormat;
SET hive.optimize.index.filter=true;
SET hive.optimize.index.filter.compact.minsize=0;

# 执行查询，共消耗36.144s,确实比不加索引要快，但是效果不是特别明显
```

![image-20210103092826457](https://tongji4m3.oss-cn-beijing.aliyuncs.com/image-20210103092826457.png)

###      6.3.3 开启本地模式

大多数的Hadoop job是需要hadoop提供的完整的可扩展性来处理大数据的。不过，有时hive的输入数据量是非常小的。在这种情况下，为查询出发执行任务的时间消耗可能会比实际job的执行时间要多的多。对于大多数这种情况，hive可以通过本地模式在单台机器上处理所有的任务。对于小数据集，执行时间会明显被缩短。如此一来，对数据量比较小的操作，就可以在本地执行，这样要比提交任务到集群执行效率要快很多。

鉴于本次项目中存在数据量较小、集群节点数目较少等客观因素，导致无法完全发挥分布式存储系统的优势。因此，根据项目的业务需求，决定开启Hive的本地模式。

```mysql
set hive.exec.mode.local.auto=true;
```

#### 6.3.3.1 本地模式适用情况

1. job的输入数据大小必须小于参数：hive.exec.mode.local.auto.inputbytes.max(默认128MB)
2. job的map数必须小于参数：hive.exec.mode.local.auto.tasks.max(默认4)
3. job的reduce数必须为0或者1

因为我们的review文件大约有800MB，为了支持本地模式，必须要设置**inputbytes.max**

```mysql
set hive.exec.mode.local.auto=true;

set hive.exec.mode.local.auto.inputbytes.max=10000000000;

set hive.exec.mode.local.auto.tasks.max=10;

# 查询时间： 3.357s
```

# 7. 查询和统计程序

## 1.1 系统功能性分析

本部分对系统功能性需求进行说明

### 1.1.1 条件查询

按照指定条件或条件范围进行查询

既可以指定单个条件，也可以指定多个条件的组合查询

**按照时间进行查询及统计**

查询指定年份上映的所有电影

查询指定月份上映的所有电影

查询指定星期几上映的所有电影

查询指定季度上映的所有电影

查询指定的时长范围的电影

**按照电影的特征进行查询及统计:**

查询指定名称的电影

**按照导演进行查询及统计:**

查询指定导演指导的电影

查询指定导演集合指导的电影

**按照演员进行查询及统计:**

查询指定演员参演的电影

查询指定演员集合参演的电影

**按照电影类别进行查询及统计:**

查询指定类别的电影

查询指定类别集合的电影

**针对电影评论进行查询及统计：**

查询指定电影下的所有评论

### 1.1.2 关系查询

**演员与演员合作关系查询**

查询与指定演员合作的演员及合作次数

**演员与导演合作关系查询**

查询与指定演员合作的导演及合作次数

**导演与演员合作关系查询**

查询与指定导演合作的演员及合作次数

### 1.1.3 统计查询

评论情感分析查询

按照月份进行统计查询

按照星期进行统计查询

# 8. 实验和分析

| 序号 | 查询内容                                                     | mysql  | neo4j | hive    |
| ---- | ------------------------------------------------------------ | ------ | ----- | ------- |
| 1    | 查询2011年的所有电影                                         | 93ms   | 50ms  | 8211ms  |
| 2    | 查询2011年1月的所有电影                                      | 84ms   | 76ms  | 5305ms  |
| 3    | 查询2011年1月10日的所有电影                                  | 29ms   | 62ms  | 5766ms  |
| 4    | 查询2011年2季度的所有电影                                    | 76ms   | 58ms  | 5381ms  |
| 5    | 查询演员Gates参演的所有电影                                  | 742ms  | 32ms  | 12214ms |
| 6    | 查询演员Roxann主演的所有电影                                 | 600ms  | 38ms  | 13921ms |
| 7    | 查询导演Burton指导的所有电影                                 | 654ms  | 34ms  | 12204ms |
| 8    | 查询演员Roxann和导演Burton共同的电影                         | 599ms  | 33ms  | 19076ms |
| 9    | 查询Drama类型的所有电影                                      | 5926ms | 80ms  | >2min   |
| 10   | 查询Action类型的所有电影                                     | 5277ms | 44ms  | >2min   |
| 11   | 查询评分大于2的所有电影                                      | 1136ms | 47ms  | >2min   |
| 12   | 查询2011年评分大于2且由Kevin Pollack主演，由Charles Adelman导演的题材为Drama的电影 | 512ms  | 222ms | 29221ms |
| 13   | 查询与演员Mark Thompson合作最多的导演及其合作次数            | 75ms   | 24ms  | 7197ms  |
| 14   | 查询与演员Roxann合作最多的导演及其合作次数                   | 62ms   | 15ms  | 7185ms  |
| 15   | 查询与演员Mark Thompson合作最多的演员及其合作次数            | 4ms    | 18ms  | 21127ms |
| 16   | 查询与演员Roxann合作最多的演员及其合作次数                   | 4ms    | 14ms  | 20988ms |
| 17   | 查询与导演Charles Adelman合作最多的演员及其合作次数          | 4ms    | 16ms  | 6686ms  |
| 18   | 查询与导演Ron Shelton合作最多的演员及其合作次数              | 6ms    | 16ms  | 6834ms  |
| 19   | 查询product_id为的电影及其所有系列的评论                     | 2882ms | 35ms  | 37010ms |
|      |                                                              |        |       |         |



# 9. 前端实现

## 9.1 电影的组合查询

![image-20210103185453733](https://i.loli.net/2021/01/03/9xzOe1WukFf3vZK.png)

## 9.2 评论查询

![image-20210103185532565](https://i.loli.net/2021/01/03/rfkdCHWynzQpqPJ.png)

## 9.3 查询导演合作的演员，查询演员合作的导演，查询演员合作的演员

![image-20210103185627930](https://i.loli.net/2021/01/03/DfhodJsExbFAG37.png)

![image-20210103185646416](https://i.loli.net/2021/01/03/2dUbFMYmJzwgDXo.png)

![image-20210103185703588](https://i.loli.net/2021/01/03/axqAODndcQWrJF2.png)

## 9.4 统计图表：

包括评论区的情感统计，电影针对月份和星期的统计。

![image-20210103185727062](https://i.loli.net/2021/01/03/MtD9FYRxQ4W2UKd.png)

![image-20210103185745029](https://i.loli.net/2021/01/03/qgKdMaA7Vi6pjOc.png)

# 10. 成员

1851632 石稼晟

1751022 李翠琪

1854081 付诚

1853781 戴家辉