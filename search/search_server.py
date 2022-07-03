from pymilvus import CollectionSchema, FieldSchema, DataType, utility, connections, Collection
from rich.progress import track
import pymysql
import pickle
import logging
import os

# ----------------------------------------------------------------------------------------------------------------------
# 构建日志
logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)-5s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ----------------------------------------------------------------------------------------------------------------------
# 反序列化
file = open('vector.pkl', 'rb')
vectors = pickle.load(file)
file.close()
logger.info("序列化完成，加载数据量：%d", len(vectors))

# ----------------------------------------------------------------------------------------------------------------------
# 给数据添加主键id
base_path = '/Users/wjun/Downloads/学习资料/JPEGImages/'
img_path = [base_path + path for path in os.listdir(base_path)]
pk = [str(i) + "-" + img_path[i] for i in range(len(vectors))]
# 将主键与向量进行zip
data = dict(zip(pk, vectors))
logger.info("为向量生成主键id")

# ----------------------------------------------------------------------------------------------------------------------
# collection name
collection_name = 'search_image'
# 维度
dim = vectors[0].shape[0]

# 构建 collection 的 schema 信息
# 主键字段
image_id = FieldSchema(name='image_id', dtype=DataType.INT64, is_primary=True, description='图片id')
# 向量字段
image_vector = FieldSchema(name='image_vector', dtype=DataType.FLOAT_VECTOR, dim=dim, description='图片向量')
# 构建 Collection
schema = CollectionSchema(fields=[image_id, image_vector], description='以图搜图')

# ----------------------------------------------------------------------------------------------------------------------
# milvus 别名
alias = "default"
# milvus ip
host = "121.199.45.82"
# milvus port
port = "19530"
# 连接 milvus
connections.connect(host=host, port=port, alias=alias)
logger.info("连接 milvus")
# 判断待构建的 collection 是否存在，不存在创建
if utility.has_collection(collection_name):
    logger.info("集合 %s 已存在", collection_name)
else:
    logger.info("集合 %s 不存在，开始创建", collection_name)
    Collection(name=collection_name, schema=schema, consistency_level='Strong')

collection = Collection(collection_name)

# ----------------------------------------------------------------------------------------------------------------------
# 连接 mysql
host = '127.0.0.1'
port = 3306
user = 'root'
password = '980729'
connect = pymysql.connect(host=host, port=port, user=user, password=password)
logger.info("连接 mysql")
cursor = connect.cursor()
insert_sql = "insert into milvus_search.meta(id,path) values('%s','%s')"


# ----------------------------------------------------------------------------------------------------------------------
# 插入数据，同时插入mysql和milvus
try:
    for key, value in track(data.items(), description="Insert..."):
        pk, path = key.split("-")
        # 元数据写入 mysql
        cursor.execute(insert_sql % (pk, path))
        collection.insert([
            [int(pk)],
            [list(value)]
        ])
    # 向量数据写入 milvus
    # logger.info("insert milvus")
    # 批量插入
    # collection.insert([
    #     [int(keys.split("-")[0]) for keys in data.keys()][1:1000],
    #     list(data.values())[1:1000]])
    connect.commit()
except Exception as e:
    logger.error("错误回滚:" + str(e))
    connect.rollback()

# 关闭连接
connections.disconnect(alias=alias)
logger.info("关闭 milvus 连接")
connect.close()
logger.info("关闭 mysql 连接")
logger.info("服务端构建完成")
