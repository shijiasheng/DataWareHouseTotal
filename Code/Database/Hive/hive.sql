docker cp /root/data1/actor.txt docker-hive-master_hive-server_1:/opt;
docker cp /root/data1/actor_actor.txt docker-hive-master_hive-server_1:/opt;
docker cp /root/data1/director.txt docker-hive-master_hive-server_1:/opt;
docker cp /root/data1/director_actor.txt docker-hive-master_hive-server_1:/opt;
docker cp /root/data1/genre.txt docker-hive-master_hive-server_1:/opt;
docker cp /root/data1/movie.txt docker-hive-master_hive-server_1:/opt;
docker cp /root/data1/movie_actor.txt docker-hive-master_hive-server_1:/opt;
docker cp /root/data1/movie_director.txt docker-hive-master_hive-server_1:/opt;
docker cp /root/data1/movie_genre.txt docker-hive-master_hive-server_1:/opt;
docker cp /root/data1/review.txt docker-hive-master_hive-server_1:/opt;
docker cp /root/data1/time.txt docker-hive-master_hive-server_1:/opt;


CREATE TABLE `actor`  (
  `actor_id` int ,
  `name` String ,
  `Starring` String ,
  `participate` String
)row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES
    (
        "separatorChar"=","
    )
    STORED AS TEXTFILE;
    
   LOAD DATA LOCAL INPATH '/opt/actor.txt' OVERWRITE INTO TABLE actor;

CREATE TABLE `actor_actor`  (
  `actor_id_1` int,
  `actor_id_2` int ,
  `count` int
)row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES
    (
        "separatorChar"=","
    )
    STORED AS TEXTFILE;

 LOAD DATA LOCAL INPATH '/opt/actor_actor.txt' OVERWRITE INTO TABLE actor_actor;

CREATE TABLE `director`  (
  `director_id` int  ,
  `name` String   ,
  `filming` String   COMMENT '导演拍摄的电影用字符串标识,便于查询'
)row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES
    (
        "separatorChar"=","
    )
    STORED AS TEXTFILE;
    
   LOAD DATA LOCAL INPATH '/opt/director.txt' OVERWRITE INTO TABLE director;

CREATE TABLE `director_actor`  (
  `director_id` int  ,
  `actor_id` int  ,
  `count` int 
)row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES
    (
        "separatorChar"=","
    )
    STORED AS TEXTFILE;
    
   LOAD DATA LOCAL INPATH '/opt/director_actor.txt' OVERWRITE INTO TABLE director_actor;

CREATE TABLE `genre`  (
  `genre_id` int  ,
  `name` String   ,
  `movies` String  COMMENT '该类型的电影集合,便于查询'
)row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES
    (
        "separatorChar"=","
    )
    STORED AS TEXTFILE;
    
   LOAD DATA LOCAL INPATH '/opt/genre.txt' OVERWRITE INTO TABLE genre;

CREATE TABLE `movie`  (
  `movie_id` int  ,
  `product_id` String   ,
  `time_id` int  ,
  `title` String  ,
  `genres` String ,
  `director` String ,
  `supporting_actors` String ,
  `actor` String ,
  `run_time` String ,
  `release_date` String  COMMENT '发布日期',
  `date_first_available` String ,
  `star` String  COMMENT '评分',
  `link_id` String ,
  `link_title` String 
)row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES
    (
        "separatorChar"=","
    )
    STORED AS TEXTFILE;
    
   LOAD DATA LOCAL INPATH '/opt/movie.txt' OVERWRITE INTO TABLE movie;

CREATE TABLE `movie_actor`  (
  `movie_id` int  ,
  `actor_id` int  ,
  `is_supporting` int
)row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES
    (
        "separatorChar"=","
    )
    STORED AS TEXTFILE;
    
   LOAD DATA LOCAL INPATH '/opt/movie_actor.txt' OVERWRITE INTO TABLE movie_actor;

CREATE TABLE `movie_director`  (
  `movie_id` int  ,
  `director_id` int  
)row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES
    (
        "separatorChar"=","
    )
    STORED AS TEXTFILE;
    
   LOAD DATA LOCAL INPATH '/opt/movie_director.txt' OVERWRITE INTO TABLE movie_director;

CREATE TABLE `movie_genre`  (
  `movie_id` int  ,
  `genre_id` int  
)row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES
    (
        "separatorChar"=","
    )
    STORED AS TEXTFILE;
    
   LOAD DATA LOCAL INPATH '/opt/movie_genre.txt' OVERWRITE INTO TABLE movie_genre;

CREATE TABLE `review`  (
  `review_id` int  ,
  `product_id` String  ,
  `user_id` String  ,
  `profile_name` String ,
  `helpfulness` String ,
  `score` String ,
  `time` String ,
  `star` double 
)row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES
    (
        "separatorChar"=","
    )
    STORED AS TEXTFILE;

    
   LOAD DATA LOCAL INPATH '/opt/review.txt' OVERWRITE INTO TABLE review;

CREATE TABLE `time`  (
  `time_id` int  ,
  `year` int ,
  `month` int ,
  `day` int ,
  `week` int ,
  `movie` String  COMMENT '存储该时间点的一系列电影集合'
)row format serde 'org.apache.hadoop.hive.serde2.OpenCSVSerde' WITH SERDEPROPERTIES
    (
        "separatorChar"=","
    )
    STORED AS TEXTFILE;
    
   LOAD DATA LOCAL INPATH '/opt/time.txt' OVERWRITE INTO TABLE time;

