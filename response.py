import json
file_path =r'C:\Users\mysel\project\EducationBot\test_response.json'
with open(file_path, "r", encoding="utf-8") as f:

    s =json.load(f)
print(len(s))
print(len(s['runs']))
for chat in s['runs']:
        print('User questions: ',chat['message']['content'])
        print("GPT response: ",chat['response']['content'])