import os
import time
import pandas as pd
from openai import OpenAI

start_time = time.time()  # 获取当前时间
# 创建空列表
company_list = []
sector_list=[]
address_list = []
AI_count_list = []
total_list = []
# 创建OpenAI实例
client=OpenAI(
 api_key=os.getenv("DASHSCOPE_API_KEY"),base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"#通义千问模型
 # api_key=os.getenv("DeepSeek_API_KEY"), base_url="https://api.deepseek.com"#DeepSeek模型
 # base_url="https://api.aigc369.com/v1"#第三方地址
)

# 读取文件信息
file = 'FILE_PATH.xlsx'
data = pd.read_excel(file)

# 获得AI回答
def get_openai_response(client, prompt):
 response = client.chat.completions.create(
   model="qwen-plus",
  # model='deepseek-chat',
  messages=[
   {"role": "user", "content": prompt}
  ]
 )
 return response.choices[0].message.content

#计数变量初始化
AI_count = 0
total_count = 0
error_count = 0
# 主要逻辑代码
for i in range('循环次数'):
 selected_data = data.loc[i,['专利名称','摘要']]# 获取专利名称和摘要
 company_name = data.loc[i,'原始企业名称']
 sector_name = data.loc[i,'行业名称']
 address = data.loc[i,'地址']
 # 如果该公司不在列表中
 if company_name not in company_list:
  # 将各项数据值加入各项列表
  company_list.append(company_name)
  sector_list.append(sector_name)
  address_list.append(address)
  # 刷新专利数值
  AI_count = 0
  total_count = 0
 # 创建提示
 prompt = f'''根据提供的专利名称和摘要，判断该专利是否属于人工智能相关专利,如果属于,返回'true',否则返回'false',不要输出任何额外文本.
           ###
           {selected_data}
           ###
           '''
 ### 异常处理
 try:
  # 获得回答
  response = get_openai_response(client,prompt)
  # 截取异常
 except Exception as e:
  # 统计出错间隔时间和次数
  error_count += 1
  error_time = time.time()
  interval_time=error_time - start_time
  print(interval_time)
  print(error_count)
  print(e)
  total_count = total_count + 1
  # 判断该专利是否是该公司的最后一个专利
  if i >= len(data) - 1 or data.loc[i + 1, '原始企业名称'] not in company_list:
   # 总结专利总数
   AI_count_list.append(AI_count)
   total_list.append(total_count)
  # 跳出本次循环
  continue
 #统计与人工智能相关专利数量
 else:
  if response=='true':
   AI_count=AI_count+1
  total_count=total_count+1
  # 判断该专利是否是该公司的最后一个专利
  if i>= len(data)-1 or data.loc[i+1,'原始企业名称'] not in company_list:
   # 总结专利总数
   AI_count_list.append(AI_count)
   total_list.append(total_count)

# 检查列表是否对齐
# print(company_list)
# print(sector_list)
# print(address_list)
# print(AI_count_list)
# print(total_list)

# 生成excel文档
df=pd.DataFrame({'原始企业名称':company_list,'行业':sector_list,'地址':address_list,'人工智能相关专利数':AI_count_list,'总专利数':total_list})
df.to_excel(r"OUTPUT_PATH.xlsx",index=False)

# 计算运行时间
end_time = time.time()# 获取当前时间
elapsed_time = end_time - start_time
print(f"代码运行时间: {elapsed_time} 秒")