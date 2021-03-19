import json


class Params():
    """Class that loads hyperparameters from a json file.
        Example:
        ```
        params = Params(json_path)
        print(params.learning_rate)
        params.learning_rate = 0.5  # change the value of learning_rate in params
        ```
        """
    def __init__(self, json_path):
        with open(json_path) as f:
            params = json.load(f)  # 将json格式数据转换为字典
            self.__dict__.update(params)

    def save(self, json_path):
        with open(json_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)  # indent缩进级别进行漂亮打印

    def update(self, json_path):
        """Loads parameters from json file"""
        with open(json_path) as f:
            params = json.load(f)
            self.__dict__.update(params)

    @property  # Python内置的@property装饰器就是负责把一个方法变成属性调用的
    def dict(self):
        """Gives dict-like access to Params instance by `params.dict['learning_rate']"""
        return self.__dict__


if __name__ == '__main__':
    data = dict()
    data["lessons"] = [[{"课程名": ''}, {"任课老师": ''}, {"选课人数上限": 0}, {"选课学生": []}, {"选课学生人数": 0}]]
    data["teachers"] = [[{"姓名": ''}, {"ID": 0}, {"password": None}, {"所教课程相关信息": [[{'课程名': ''}, {"选课人数上限": 0},
                                                                                  {'选课学生': []}, {"选课学生人数": 0}]]}]]
    data["students"] = [[{"姓名": ''}, {"ID": 0}, {"password": None}, {"所选课程相关信息": [[{'课程名': ''}, {"任课老师": ''},
                                                                                   {"选课人数上限": 0}, {"选课学生人数": 0}]]}]]
    data["administrators"] = [[{"姓名": ''}, {"ID": 0}, {"password": None}]]
    json_str = json.dumps(data, indent=4)  # ???? 中文才会转换成乱码

    with open('params.json', 'w') as f:  # 创建一个params.json文件
        f.write(json_str)  # 将json_str写到文件中
    #
    # params = Params('params.json')
    # # params.SEED = 5   # 修改json中的数据
    # params.save('params.json')  # 将修改后的数据保存
    # print(params.dict)
# if __name__ == '__main__':
#     def get_data():
#         try:
#             with open('params.json') as file:
#                 data_msg = json.load(file)
#             return data_msg
#         except json.decoder.JSONDecodeError:
#             return {'lessons': ''}
#
#     lessons = get_data()['lessons']


