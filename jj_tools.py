import sys
import os
import shutil
import argparse

TIPS_STRING = """
-> collect {path} {dir_name} 把当前路径下所有一级文件夹内的文件移动到新建文件夹内
-> remove {path} {suffix} 删除当前路径下指定后缀名的文件
-> list {path} 遍历当前路径下的文件夹
-> rename {path} {name} 顺序重命名路径下所有文件
-> listRename {path} 批量把路径下，文件夹内的文件根据文件夹重命名
-> sizeFilter {path} size {destination} 把路径下大于指定大小的文件移到指定文件夹内
"""

ERROR_STRING = """
command error
请输入 jj_tools -help 查看帮助
"""

ACTION_LIST = ["-help", "c", "d", "list", "r", "lr"]

ACTION_COMMANDS = [
    {"name": "-help", "func": "help", "help": "查看帮助"}
]

def log(s):
    sys.stderr.write("jj_tools: ")
    sys.stderr.write(s)
    sys.stderr.write("\n")
    sys.stderr.flush()


def file_delete(path, name):
    for sub_file in os.listdir(path):
        sub_path = os.path.join(path, sub_file)
        if os.path.isdir(sub_path):
            file_delete(sub_path, name)
        else:
            suffix = sub_path.split(".")[-1]
            if suffix == name:
                log("remove: " + sub_path)
                os.remove(sub_path)


def file_traverse(path, index=0):
    index += 1
    for sub_file in os.listdir(path):
        log(index * " * " + sub_file)
        sub_path = os.path.join(path, sub_file)
        file_traverse(sub_path, index)


def file_rename(path, name):
    total_list = os.listdir(path)

    try:
        for index, file in enumerate(total_list):
            new = name + str(index)
            os.rename(os.path.join(path, file), os.path.join(path, new))

    except Exception as e:
        print("rename error: ", e)


def file_rename_follow_dir(path):
    total_list = os.listdir(path)

    try:
        for dir in total_list:
            print(os.path.join(path, dir))
            dir_path = os.path.join(path, dir)
            if os.path.isdir(dir_path):
                for index, file in enumerate(os.listdir(dir_path)):
                    suffix = os.path.splitext(file)[-1]
                    new_name = dir + "_" + str(index) + suffix
                    src = os.path.join(dir_path, file)
                    dst = os.path.join(dir_path, new_name)
                    log(src)
                    log(dst)
                    os.rename(src, dst)
            else:
                print("not dir: ", dir)

    except Exception as e:
        print("rename error: ", e)


def file_collection(path, new_dir):
    if not os.path.exists(path + "/" + new_dir):
        os.mkdir(path + "/" + new_dir)

    total_list = os.listdir(path)
    # print("total_list: ", total_list)
    dir_list = []
    for dir in total_list:
        # print(dir)
        # print(os.path.isdir(path + "/" + dir))
        if os.path.isdir(path + "/" + dir) and dir[0] != ".":
            dir_list.append(dir)
    print(dir_list)

    for dir in dir_list:
        dir_path = os.path.join(path, dir)
        for file in os.listdir(dir_path):
            try:
                ori = os.path.join(dir_path, file)
                if os.path.isfile(ori):
                    des = os.path.join(path, new_dir)
                    log("move {} to {}".format(ori, des))
                    print("-" * 50)
                    shutil.move(ori, des)
            except Exception as e:
                print("files move error: ", e)


def size_filter(path, size, des):
    des_path = os.path.join(path, des)
    if not os.path.exists(des_path):
        os.mkdir(des_path)

    n = 0
    for root, dirs, files in os.walk(path):
        # n += 1
        # print("n == " + str(n) + " root: " + "--" * 50)
        # print("root: " + root)
        # print("dirs: " + "--" * 50)
        # print(dirs)
        # print("files: " + "--" * 50)
        # print(files)

        if len(files) > 0:
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)  / (1024 * 1024)
                print(file + ", size: " + str(round(file_size, 2)) + "M")

                if file_size > size:
                    shutil.move(file_path, des_path)

if __name__ == '__main__':

    print(sys.argv)
    print(len(sys.argv))

    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "-help"):
        log(TIPS_STRING)
        exit(0)

    path = sys.argv[2]
    if not os.path.exists(path):
        log("path is not exist!!")

    if len(sys.argv) == 3 and sys.argv[1] == "list":
        file_traverse(path)

    elif len(sys.argv) == 3 and sys.argv[1] == "listRename":
        file_rename_follow_dir(path)

    elif len(sys.argv) == 4 and sys.argv[1] == "collect":
        file_collection(path, sys.argv[3])

    elif len(sys.argv) == 4 and sys.argv[1] == "rename":
        file_rename(path, sys.argv[3])

    elif len(sys.argv) == 4 and sys.argv[1] == "remove":
        name = sys.argv[3]
        file_delete(path, name)

    elif len(sys.argv) == 5 and sys.argv[1] == "sizeFilter":
        size = int(sys.argv[3])
        des = sys.argv[4]
        size_filter(path, size, des)

    else:
        log(ERROR_STRING)
