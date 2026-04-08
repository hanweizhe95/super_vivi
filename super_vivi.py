import json
import time
import requests
import selenium

# 1. 读取 JSON 文件
with open('students.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 2. 访问数据

# 3. 遍历学生列表
print("\n逐个学生信息：")
for student in data['students']:
    print(f"正在填写{student['name']['surname']} {student['name']['first_name']}的申请...")
    print(f"姓名：{student['name']}")
    time.sleep(0.5) 
    print(f"生日：{student['birthday']}")
    time.sleep(0.5) 
    print(f"邮箱：{student['email']}")
    time.sleep(0.5) 
    print(f"电话：{student['phone']}")
    time.sleep(0.5) 
    print(f"雅思成绩：{student['IELTS']}")
    time.sleep(0.5) 
    print("-" * 20)