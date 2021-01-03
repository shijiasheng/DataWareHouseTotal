# docker Hive操作
```
cd cloud_calculation/docker-hive-master
docker-compose up -d
docker-compose exec hive-server bash
/opt/hive/bin/beeline -u jdbc:hive2://localhost:10000

先在docker外导入MySQL/data文件夹下数据进入容器
再在启动好的hive中建立相关表
再把数据导入表中
相关sql语句都写在了hive.sql中
```

# docker

```
启动        systemctl start docker

守护进程重启   sudo systemctl daemon-reload

重启docker服务   systemctl restart  docker

重启docker服务  sudo service docker restart

关闭docker service docker stop

关闭docker systemctl stop docker

停止所有的容器  docker stop $(docker ps -aq)

删除所有容器  docker rm $(docker ps -aq)
```







