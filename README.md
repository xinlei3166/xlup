---
typora-copy-images-to: ipic
---

# 一个图片和视频上传服务系统
### author: 君惜
### 语言：python3
### 框架：sanic
### 数据库：mysql
### 缓存：redis
### web框架: vue
### ui框架: iview



# 运行

## 后台

### 安装环境

```python
pipenv install
```

### 导入数据库数据

```python
mysql -u root -B xlup -p 123456 < models/xlup.sql
```

### 启动后台服务

```python
pipenv run python main.py start
```

## 前台

### 安装环境

```shell
cd web
npm install
```

### 启动测试

```shell
npm run serve
```

### 浏览

输入地址`http://localhost:8080`

* 登录页

![image-20181224111455296](https://ws4.sinaimg.cn/large/006tNbRwly1fyhnxzxpxvj31e20u0u0x.jpg)

默认账户：admin，密码：123456

* 首页

![image-20181224111542771](https://ws1.sinaimg.cn/large/006tNbRwly1fyhnyz4dgij31lt0u0tgt.jpg)

* 图片列表

![image-20181224111605864](https://ws4.sinaimg.cn/large/006tNbRwly1fyhnz6axbaj31m00u0dos.jpg)

* 视频列表

![image-20181224111628135](https://ws4.sinaimg.cn/large/006tNbRwly1fyhnzjv736j31lu0u0k1f.jpg)

* 用户列表

![image-20181224111704743](https://ws4.sinaimg.cn/large/006tNbRwly1fyho06w7j0j31m80u0tit.jpg)