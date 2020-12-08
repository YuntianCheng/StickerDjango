### 表情包生辰工具

**上传照片或者照相生成表情包**

**前端用的Vue，后端是Django**



#### 环境：python3.7 node.js

#### 安装Vue

npm install -g vue-cli



#### 安装python库

brew install boost
brew install cmake
pip3 install -r requirements.txt


以上是macOS的配制方法，unbuntu将brew换成apt-get


#### 启动方法
##### 1. 前后端分别启动

前端：
cd Sticker
npm install
npm run serve

后端：
python3 manage.py runserver


##### 2. 将Vue打包进django

cd Sticker
npm install
npm run build

然后将生成的dist文件夹拖到Web文件夹里
python3 manage.py runserver


