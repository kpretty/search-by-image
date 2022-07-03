from towhee import pipeline
from pymilvus import connections, Collection
import pymysql
import cv2

your_image = '/Users/wjun/Downloads/学习资料/JPEGImages/2007_000648.jpg'
pipline = pipeline('image-embedding')
vector = pipline(your_image)
# milvus 别名
alias = "default"
# milvus ip
host = "121.199.45.82"
# milvus port
port = "19530"
collection_name = 'search_image'
# 连接 milvus
connections.connect(host=host, port=port, alias=alias)
# 连接 mysql
host = '127.0.0.1'
port = 3306
user = 'root'
password = '980729'
connect = pymysql.connect(host=host, port=port, user=user, password=password)

collection = Collection(collection_name)

search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
result = collection.search(data=[list(vector)], anns_field='image_vector', param=search_params, limit=5,
                           consistency_level='Strong')

cursor = connect.cursor()
sql = ""
if len(result[0].ids) == 0:
    print("没有匹配项")
    exit(0)
elif len(result[0].ids) == 1:
    sql = "select path from milvus_search.meta where id = %s" % str(result[0].ids[0])
else:
    sql = "select path from milvus_search.meta where id in %s" % str(tuple(result[0].ids))

cursor.execute(sql)
imread = cv2.imread(your_image)
cv2.imshow('your image', imread)
image_id = 0
for img in cursor.fetchall():
    imread = cv2.imread(img[0])
    cv2.imshow(str(image_id), imread)
    image_id += 1
cv2.waitKey(0)
cv2.destroyAllWindows()
