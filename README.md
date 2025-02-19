# Patent-DataAnalysis
本项目通过批量调用大语言模型实现对专利数据的分析

### 创建大语言模型实例
此时你可以直接传输你的api_key
```python
client=OpenAI(
 api_key="你的api_key",base_url="大语言模型官方地址"
)
```
或者将api_key设置在系统环境变量中,通过os系统调用
```python
client=OpenAI(
 api_key=os.getenv("DASHSCOPE_API_KEY"),base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"#通义千问模型
)
```
