import json
import time
import requests
import selenium
from schools.cityu import cityu
from schools.hku import hku

# 1. 读取 JSON 文件
with open('students.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 2. 访问数据

# 3. 遍历学生列表
print("\n逐个学生信息：")
for student in data['students']:
    print(f"正在填写{student['name']['surname']} {student['name']['first_name']}的申请...")
    for school in student['schools']:
        if school['name'] == "hku":
            print("appling for hku")
            hku(student, school)
        elif school['name'] == "cityu":
            print("appling for cityu")
            cityu(student, school)
    print("-" * 20)