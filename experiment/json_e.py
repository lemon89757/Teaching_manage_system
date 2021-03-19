import json
data = {
    "lessons": [],
    "peoples": [
        [
            {
                "ID": 123456789
            },
            {
                "名字": "tt"
            },
            {
                "密码": "123456"
            },
            {
                "类型": "Student"
            }
        ],
        [
            {
                "ID": 123
            },
            {
                "name": "joe"
            },
            {
                "password": "123"
            },
            {
                "type": "Student"
            }
        ],
        [
            {
                "ID": 1111
            },
            {
                "name": "monica"
            },
            {
                "password": "11"
            },
            {
                "type": "Teacher"
            }
        ]
    ]
}
data_json = json.dumps(data)
with open("experiment.json", 'w') as file:
    file.write(data_json)
