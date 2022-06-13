
import re
import os
import sys
import colorama
import json
from pprint import pprint

# 删除所有注释python小脚本

class DeleteComments:
    def __init__(self) -> None:
        self.lines = ""
        self.pattern = []
        self.filename = ""
        self.dirname = "."
        self.ext = ""
        self.origin_ext = ""
        self.comment_name = ""
        self.ext_config_file = ""
        self.alias_config_file = ""
        self.re_module = [["([   ])*(", ".*", "(\n)*)+"],
                          ["([   ])*(","[\s\S]*","(\n)*)+"]]
        self.known_ext = {
            # ".c": ["([   ])*(//.*(\n)*)+", "([   ])*(/\*[\s\S]*\*/(\n)*)+"],
            # ".cpp": ["([   ])*(//.*(\n)*)+", "([   ])*(/\*[\s\S]*\*/(\n)*)+"],
            # ".java": ["([   ])*(//.*(\n)*)+", "([   ])*(/\*[\s\S]*\*/(\n)*)+"],
            # ".py": ["([   ])*(#.*(\n)*)+", "([   ])*([\'\"]{3}[\s\S]*[\'\"]{3}(\n)*)+"]
        }
        self.all_comments = ""
    # 读取json配置文件

    def json_config_parser(self):
        cfg = {}
        with open(self.ext_config_file, "r") as f:
            cfg = json.load(f)
            print(colorama.Fore.BLUE)
            pprint(f"config from {self.ext_config_file}:\n{cfg}")
            print(colorama.Style.RESET_ALL)
        self.known_ext = cfg
    # 更新json配置文件

    def update_json_config(self):
        into = json.dumps(self.known_ext, indent=2)
        with open(self.ext_config_file, "w") as f:
            f.write(into)

    # 将规则相似的后缀名用别名转换器转换为可解析为规则的后缀名
    # 并且将该别名对应的规则保存在后缀名的配置中，方便下次使用
    def alias_parser(self):
        with open(self.alias_config_file, "r") as f:
            cfg = json.load(f)
            for _,v in cfg.items():
                if self.ext in v:
                    self.ext = v[0]
                    self.known_ext[self.origin_ext] = self.known_ext[self.ext]
                    return True
        return False
        
    # 删除所有注释
    def delete_comments(self):
        for pat in self.pattern:
            pat = re.compile(pat)
            # 不论如何，注释会保存在成员变量中，方便后续提取
            for ele in re.findall(pat, self.lines):
                self.all_comments += "".join(ele)
            self.lines = re.sub(pat, "", self.lines)
        return self.lines

    # 获取正则表达式规则
    def get_pattern(self):
        # 如果是未知的后缀名
        if self.ext not in self.known_ext.keys() and self.alias_parser() == False:
            print("no match file extension!")
            flag = "y"
            while flag == "y":
                print(
                    "you need to complete the regex rule with inputing several"
                    " 'start' and 'end'")
                # 选择此时输入的注释规则是适用于多行的
                mod = input(
                    "Does the comment rule cross lines?(y|N)(Default:N)")
                mod = 1 if mod == "y" else 0
                # 输入注释的开始和结束，比如//的开始和结束分别是“//”和“\n”
                start = input("please input start:")
                end = input("please input end:(\\n for line break)")
                end = "\n" if end == "\\n" else end
                self.pattern.append(
                    self.re_module[mod][0]+start +
                    self.re_module[mod][1]+end +
                    self.re_module[mod][2])
                flag = input("Do you want to continue?(y|N)(Default:y)")
                flag = "N" if flag == "N" else "y"
            # 将输入的规则输入已知的规则集合中
            self.known_ext[self.ext] = self.pattern
            return self.pattern
        self.pattern = self.known_ext[self.ext]
        return self.pattern
    # 提交文件以供处理

    def commit_file(self, filename: str, store: bool = True):
        # 存入文件名并分离目录名
        self.init_file(filename)
        # 读取文件内容并保存为字符串
        with open(self.filename, "r") as f:
            self.lines = "".join(f.readlines())
        # 读取json配置文件
        self.json_config_parser()
        # 获取符合后缀名的正则表达式规则
        self.get_pattern()
        # 正式处理文件
        self.delete_comments()
        # 在.swap文件中存入删除注释后的内容
        with open(self.filename+".swap", "w") as f:
            f.write(self.lines)
        # 如果用户要求存储注释
        if store == True:
            cnt = 1
            # 如果comments.txt已经存在就换用comments1.txt，以此类推
            ori_name = self.comment_name
            while os.path.exists(os.path.join(self.dirname, self.comment_name)):
                tmp = ori_name.split(".")
                if len(tmp) >= 2:
                    self.comment_name = tmp[0]+str(cnt)+"."+".".join(
                        tmp[1:] if len(tmp) > 2 else [tmp[1]])
                else:
                    self.comment_name += str(cnt)
                cnt += 1
            # 写入注释
            with open(os.path.join(self.dirname, self.comment_name), "w") as f:
                f.write(self.all_comments)
        # 狸猫换太子
        os.remove(self.filename)
        os.rename(self.filename+".swap", self.filename)
    # 初始化文件的一系列属性

    def init_file(self, filename: str,\
        ext_file: str = "ext_config.json", alias_file:str = "alias_config.json"):
        self.filename = filename
        self.comment_name = self.filename+".txt"
        self.dirname = os.path.dirname(self.filename)
        self.dirname = self.dirname if self.dirname != "" else "."
        self.origin_ext = self.ext = os.path.splitext(self.filename)[-1]
        self.ext_config_file = ext_file
        self.alias_config_file = alias_file
        
    
    # 删除给定文件目录下的所有comments文件
    def clean_comment_file(self):
        tmp_pat = re.compile("comments[0-9]*.txt")
        for f in os.listdir(self.dirname):
            if re.match(tmp_pat, f) is not None:
                print(f"romoving file: {f}")
                os.remove(f)


def help():
    # 为防止中文输出出现乱码使用了英文写输出...后面发现是多此一举
    # help使用绿色输出
    print(colorama.Fore.LIGHTGREEN_EX)
    print('''
          Please input filename needed to delete comments
          for example,
          python delete_all_comments.py ./file/test.cpp
          -------
          This program uses two configure file whose name is defaultly set as:
          alias_config.json\t\text_config.json
          -alias_config.json
                define the extension's alias, which reduce writting same rules for different file extensions.
          -ext_config.json
                define the comment rules of certain file extensions 
          -------
          The program has the delete rule of files with extension of .cpp,.c,.java,.py util now
          if provided file's extension is not in collection,
          the program will automatically enter rule input mod,
          then you can set rules by giving start symbol and end symbol of the comment
          -------
          There's also two practical option:
          To remove all backup comments file in chosen directory:
            python delete_all_comments.py clean [directory]
          To delete all files' comments of chosen directory:
            python delete_all_comments.py all [directory]
                                        Written By Peter Liu on 2022.6.13
          ''')
    print(colorama.Style.RESET_ALL)


def main():
    if len(sys.argv) < 2:
        help()
        return
    else:
        if sys.argv[1] in ["help", "-h", "--help"]:
            help()
            return
        
        dlt = DeleteComments()
        if sys.argv[1] == "clean":
            if len(sys.argv) > 2:
                dlt.dirname = sys.argv[2]
            dlt.clean_comment_file()
            return
            
        jud = input("Do you want a backup for your comments?(y|N)(Default:y)")
        jud = False if jud == "N" else True
        filelist = sys.argv[1:]
        if sys.argv[1] == "all":
            if len(sys.argv) > 2:
                dlt.dirname = sys.argv[2]
            print(f"all files' comments in {dlt.dirname} will be deleted!")
            filelist = os.listdir(dlt.dirname)
        for f in filelist:
            dlt.commit_file(f, jud)
        dlt.update_json_config()


if __name__ == "__main__":
    main()
