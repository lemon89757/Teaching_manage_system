import json


class ReadWrite(object):
    def __init__(self):
        self._data_path = \
            r'C:\Users\helloTt\Desktop\tt\2021上半学期（电科）\learning_project\system_student_manage\data'
        #  路径前记得加r

    def to_json(self):
        """管理员方法，将json文件进行初始化（清空并写入data中的内容）"""
        data = dict()
        data["lessons"] = [[{"课程名": ''}, {"任课老师": ''}, {"选课人数上限": 0}, {"选课学生": []}, {"选课学生人数": 0}]]
        data["teachers"] = [[{"姓名": ''}, {"ID": 0}, {"password": None}, {"所教课程相关信息": [[{'课程名': ''}, {"选课人数上限": 0},
                                                                                     {'选课学生': []}, {"选课学生人数": 0}]]}]]
        data["students"] = [[{"姓名": ''}, {"ID": 0}, {"password": None}, {"所选课程相关信息": [[{'课程名': ''}, {"任课老师": ''},
                                                                                       {"选课人数上限": 0}, {"选课学生人数": 0}]]}]]
        data["administrators"] = [[{"姓名": ''}, {"ID": 0}, {"password": None}]]
        with open(self._data_path, 'w') as file:
            data_new = json.dumps(data, indent=4)
            file.write(data_new)

    def get_data(self):
        try:
            with open(self._data_path) as file:
                data_msg = json.load(file)
                self.__dict__.update(data_msg)
            return self.__dict__
        except json.decoder.JSONDecodeError:
            print("请联系管理员进行初始化")

    def save(self):
        with open(self._data_path, 'w') as data_msg:
            json.dump(self.__dict__, data_msg, indent=4)
