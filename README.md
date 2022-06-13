# delete_ALL_comments

删除所有注释 python 小脚本

**！！！警告，本脚本是为学习用途而生，请勿在任何生产环境等可能造成经济损失的场景下使用，否则一切后果自行承担，作者概不负责！！！**

## 基本使用

可以通过命令行使用

```bash
python delete_all_comments.py [你的文件名]
```

然后，程序会询问用户是否备份注释，默认为是

## 配置文件

该程序使用 json 文件配置
一共有 delete_comments/alias_config.json, delete_comments/ext_config.json 两个配置文件

### alias_config.json

别名转换器，比如 C++有很多种后缀名，可以通过这个别名转换器转换为可以识别的后缀名从而获取正则表达式规则，又比如 java，js 等注释规则与 C/C++相似，因此.java 可以转换为.c
同时，为了提高效率，当一个别名被查找过一次时，就会被保存至后缀名配置文件

### ext_config.json

后缀名配置文件，可以通过后缀名查询正则表达式规则

## 两个实用功能

### 批量删除注释备份文件

```bash
python delete_all_comments.py clean [要删除的目录]
```

### 批量删除选定目录下文件的注释

```bash
python delete_all_comments.py all [要删除的目录]
```

英文版帮助：(通过 python delete_all_comments.py help 获取)

如果发现了什么 Bug，可以致信peterliuforever@gmail.com
