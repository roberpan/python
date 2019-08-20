# 导入 wordcloud 模块和 matplotlib 模块
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# 读入一个txt文件
text = open('txt\\Jane_Eyre.txt','r').read()
# 生成词云
wordcloud = WordCloud().generate(text)
# 显示词云图片
plt.imshow(wordcloud)
plt.axis('off')
plt.show()
# 保存图片
wordcloud.to_file('test.jpg')