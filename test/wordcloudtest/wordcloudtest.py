# -*- encoding:utf-8 -*-.
#利用背景图片生成词云，设置停用词
"""
Image-colored wordcloud
=======================

"""
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#源码所在目录
d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d,"txt\\a tale of two cities.txt")).read()

# read the mask / color image taken from
# http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
alice_coloring = np.array(Image.open(path.join(d, "png\\love.png")))
stopwords = set(STOPWORDS)
stopwords.add("said")

wc = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
               stopwords=stopwords, max_font_size=40, random_state=42)
# generate word cloud
wc.generate(text)

# create coloring from image
image_colors = ImageColorGenerator(alice_coloring)

# show
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.figure()
wc.to_file(path.join(d, 'png\\love1.png'))
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
wc.to_file(path.join(d, 'png\\love2.png'))
plt.axis("off")
plt.figure()
plt.show()