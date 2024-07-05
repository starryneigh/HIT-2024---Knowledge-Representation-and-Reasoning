from gensim.models import word2vec
import numpy as np
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontManager
import matplotlib
import sys
import os

def similar_topk(word):
    print(f"--与<{word}>最相似的10个词--")
    for e in model.wv.most_similar(positive=[word], topn=10):
        print(e[0], e[1])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python play.py <model_path>")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print(f"{sys.argv[1]} not found.")
        sys.exit(1)
    
    model_path = "./ckpt/my.model"
    matplotlib.rc("font",family='YouYuan')
    model = word2vec.Word2Vec.load(model_path)

    ############### 修改 岳不群 可以找到和这个词最相关的十个词
    print()
    similar_topk("岳不群")
    print("\n"*3)


    ############ 修改positive=["岳不群", "盈盈"], negative=["岳夫人"] 可以找到和<岳不群+盈盈-岳夫人>最相似的词
    print("--和<岳不群+令狐冲-岳夫人>最相似的词--")
    result = model.wv.most_similar(positive=["岳不群", "令狐冲"], negative=["岳夫人"], topn=5) 
    for i, j in result:
        print(i, j)

    print("\n"*3)
    # 查看sim(岳不群，林平之)，sim(岳不群，岳林珊)
    print('sim(岳不群，林平之): ', model.wv.similarity("岳不群", "林平之"))
    print('sim(岳不群，岳灵珊): ', model.wv.similarity("岳不群", "岳灵珊"))

    ################# 自定义词表查看词在二维空间的分布


    human = ["岳不群", '岳灵珊', '岳夫人', "林平之"]
    kongfu = ["广陵散", "葵花宝典", "易筋经", '紫霞']

    human_vec = [model.wv[h] for h in human]
    kongfu_vec = [model.wv[k] for k in kongfu]

    vecs = human_vec + kongfu_vec
    items = human + kongfu
    pca = PCA(2)
    vecs = pca.fit_transform(X=vecs)
    X, Y = [], []
    for vec in vecs:
        X.append(vec[0])
        Y.append(vec[1])
    plt.scatter(X, Y)
    for idx in range(len(X)):
        plt.annotate(items[idx], (X[idx], Y[idx]))
    plt.savefig("./human_kongfu.png")
    # plt.show()




