from towhee import pipeline
from rich.progress import track
import os
import pickle

# milvus 别名
alias = "milvus"
# milvus ip
host = "121.199.45.82"
# milvus port
port = "19530"

# base_path = '/Users/wjun/Downloads/学习资料/JPEGImages/'
base_path = '/Users/wjun/Downloads/学习资料/JPEGImages/'
# 构建 embedding 模型
pipline = pipeline('image-embedding')
# 获取图片的本地路径
img_path = [base_path + path for path in os.listdir(base_path)]
# 控制台构建一个进度条用于观察进度
vector = [pipline(path) for path in track(img_path, description="Embedding...")]
print("图片 embedding 完成")
# 序列化 embedding 结果
f = open("vector.pkl", "wb")
pickle.dump(vector, f)
f.flush()
f.close()
