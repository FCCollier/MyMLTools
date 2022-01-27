# MyScrapy

## 版本信息

| 版本号   | 功能描述             | 完成情况 |
|-------|------------------|------|
 | 0.0.1 | 下载javhoo列表数据     | 未完成  |
| 0.0.2 | 登录JavDB，下载个人收藏信息 | 未完成  |

## 爬虫分类

### Javdb

### JavBus

### JavHoo

## 常用命令
### 生成requirements文件
```
cd 项目目录
pip freeze > requirements.txt
```
### 安装requirements依赖
```
pip install -r requirements.txt
```
### 生成exe文件
```commandline
nuitka --standalone --show-memory --show-progress --nofollow-imports --plugin-enable=qt-plugins --follow-import-to=utils,src --output-dir=out --windows-icon-from-ico=./logo.ico demo.py
```
```
--standalone：方便移植到其他机器，不用再安装python
--show-memory --show-progress：展示整个安装的进度过程
--nofollow-imports：不编译代码中所有的import，比如keras，numpy之类的。
--plugin-enable=qt-plugins：我这里用到pyqt5来做界面的，这里nuitka有其对应的插件。
--follow-import-to=utils,src：需要编译成C++代码的指定的2个包含源码的文件夹，这里用,来进行分隔。
--output-dir=out：指定输出的结果路径为out。
--windows-icon-from-ico=./logo.ico：指定生成的exe的图标为logo.ico这个图标，这里推荐一个将图片转成ico格式文件的网站（比特虫）。
--windows-disable-console：运行exe取消弹框。这里没有放上去是因为我们还需要调试，可能哪里还有问题之类的。
```