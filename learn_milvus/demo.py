import random

import numpy
import numpy as np
import random

from pymilvus import CollectionSchema, FieldSchema, DataType, utility, connections, Collection
import pickle

file = open('../vector.pkl', 'rb')
vectors = pickle.load(file)
file.close()

connections.connect(host='121.199.45.82', port='19530')
# book_id = FieldSchema(
#     name="book_id",
#     dtype=DataType.INT64,
#     is_primary=True,
# )
# word_count = FieldSchema(
#     name="word_count",
#     dtype=DataType.INT64,
# )
# book_intro = FieldSchema(
#     name="book_intro",
#     dtype=DataType.FLOAT_VECTOR,
#     dim=2
# )
# schema = CollectionSchema(
#     fields=[book_id, word_count, book_intro],
#     description="Test book search"
# )
# collection_name = "book"
#
# collection = Collection(
#     name=collection_name,
#     schema=schema,
#     using='default',
#     shards_num=2,
#     consistency_level="Strong"
# )
#
data = [
    [i for i in range(1)],
    [i for i in range(10000, 10001)],
    [[random.random() for _ in range(2)] for _ in range(1)],
]

print(data)

collection = Collection("book")  # Get an existing collection.
mr = collection.insert(data)
# if 1 == 2:
#     img_id = FieldSchema(name='img_id', dtype=DataType.INT64, is_primary=True)
#     img_intro = FieldSchema(name='img_intro', dtype=DataType.FLOAT_VECTOR, dim=2)
#     schema = CollectionSchema(fields=[img_id, img_intro], description='img')
#     collection_name = 'img2'
#
#     collection = Collection(name=collection_name, schema=schema, shards_num=2, consistency_level='Strong')
#
# collection = Collection('img')
# collection.insert([[1], [[1, 2]]])
key = 0
# collection.insert([
#     [key for key in range(len(vectors))],
#     vectors
# ])
print([key for key in range(len(vectors))])
# for vector in vectors:
#     mr = collection.insert([
#         [key],
#         [list(vector)]])
#     print(mr)
#     key += 1

# print([[1], [[1, 2]]])
# print([[random.random()], [list(vectors[0])]])
