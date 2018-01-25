# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import jieba.analyse
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

class FanghuaPipeline(object):

    def __init__(self):
        # 打开爬取的数据保存文件
        self.file = open('./extra_dict/str.txt', 'w', encoding='utf-8', errors='ignore')

    def process_item(self, item, spider):
        self.file.write(item['content'])
        return item

    def close_spider(self, spider):
        # 关闭爬取的数据保存文件
        self.file.close()

        # jieba 分词
        self.jieba_word()

    def jieba_word(self):

        # 读取爬取的数据
        content = open('./extra_dict/str.txt', 'r', encoding='utf-8', errors='ignore').read()

        # jieba分词 排除个别词
        jieba.analyse.set_stop_words("./extra_dict/stop_words.txt")

        # jieba分词保存1000个
        tags = jieba.analyse.extract_tags(content, topK=1000, withWeight=True)

        # 打开jieba分词的保存文件
        file_object = open('./extra_dict/cut_str.txt', 'w', encoding='utf-8', errors='ignore')

        # 保存jieba分词
        for v, n in tags:
            # 权重是小数，为了凑整，乘了一万
            # print(v + '\t' + str(int(n * 10000)))
            data_str = v + '\t' + str(int(n * 10000)) + '\n'
            file_object.write(data_str)

        # 关闭jieba分词保存文件
        file_object.close()

        # 生成词云图
        self.word_cloud()

    def word_cloud(self):

        d = path.dirname(__file__)

        # 读取分词文件
        text = open(path.join(d, './extra_dict/cut_str.txt'), 'r', encoding='utf-8', errors='ignore').read()

        # 加载词云图图片模板
        alice_coloring = np.array(Image.open(path.join(d, "./extra_dict/li.jpg")))
        stopwords = set(STOPWORDS)
        stopwords.add("said")

        # 设置字体
        wc = WordCloud(font_path="./extra_dict/simhei.ttf", background_color="white", max_words=2000, mask=alice_coloring,
                       stopwords=stopwords, max_font_size=40, random_state=42)
        # 生成词云
        wc.generate(text)

        # # 创建画笔
        # image_colors = ImageColorGenerator(alice_coloring)

        # # 显示
        # plt.imshow(wc, interpolation="bilinear")
        # plt.axis("off")
        # plt.figure()
        # # 着色显示
        # # 可以添加 color_func=image_colors 着色
        # plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
        # plt.axis("off")
        # plt.figure()
        # plt.imshow(alice_coloring, cmap=plt.cm.gray, interpolation="bilinear")
        # plt.axis("off")

        wc.to_file(path.join(d, "./extra_dict/yun.png"))
        plt.show()
