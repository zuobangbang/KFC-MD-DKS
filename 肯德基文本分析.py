import pandas
import time
import jieba

from snownlp import SnowNLP
from datetime import datetime
import matplotlib
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
import plotly.plotly
import plotly.graph_objs as go
import numpy as np
import networkx as nx
import json
import seaborn
import matplotlib.pyplot as pyl
import numpy


def read_data(filepath):
    run = pandas.read_csv(filepath, engine='python', encoding='utf-8', header=None)
    print(run)
    run.fillna('NNN')
    # print(run[11])
    # 按行读取
    com, time, floor, zan, sex, name, level, reply = [], [], [], [], [], [], [], []
    '''
    for index in run.index:
        com.append(run.loc[index][0])
        shijian.append(run.loc[index][1])
        floor.append(run.loc[index][2])
        zan.append(run.loc[index][3])
        sex.append(run.loc[index][4])
        name.append(run.loc[index][5])
        level.append(run.loc[index][6])
        reply.append(run.loc[index][7])
    for s in range(len(shijian)):
        try:
            w = time.localtime(shijian[s])
            day.append(time.strftime("%Y-%m-%d ", w))
            hour.append(time.strftime("%H:%M:%S", w))
        except Exception as e:
            day.append('')
            hour.append('')'''
    for i in zip(run[0], run[1], run[2], run[3], run[4], run[5], run[6], run[7]):
        # print(i)
        com.append(i[0])
        time.append(i[1])
        floor.append(i[2])
        zan.append(i[3])
        sex.append(i[4])
        name.append(i[5])
        level.append(i[6])
        reply.append(i[7])
    return com, time, floor, zan, sex, name, level, reply

def hot(com):
    # print(com)
    output_file('各成员话题度.html')
    jzg = ['金钟国', '钟国', '能力者']
    gary = ['gary', '狗哥']
    haha = ['haha', 'HAHA', '哈哈']
    qsm = ['全昭敏', '全妹', '全昭body']
    lsz = ['梁世赞', '世赞', '小不点']
    name = ['池石镇', '刘在石', '宋智孝', '李光洙', '金钟国', 'gary', 'haha', '全昭敏', '梁世赞']
    csz, lzs, szx, lgz, jzg, gary, haha, qsm, lsz = [], [], [], [], [], [], [], [], []
    for i in com:
        if '池石镇' in i or '石镇' in i or '鼻子' in i:
            csz.append(i)
        if '刘在石' in i or '在石' in i or '大神' in i or '蚂蚱' in i:
            lzs.append(i)
        if '宋智孝' in i or '智孝' in i or '懵智' in i or '美懵' in i:
            szx.append(i)
        if '李光洙' in i or '光洙' in i or '一筐猪' in i:
            lgz.append(i)
        if '金钟国' in i or '钟国' in i or '能力者' in i:
            jzg.append(i)
        if 'gary' in i or '狗哥' in i:
            gary.append(i)
        if 'haha' in i or 'HAHA' in i or '哈哈' in i:
            haha.append(i)
        if '全昭敏' in i or '全妹' in i or '全昭body' in i:
            qsm.append(i)
        if '梁世赞' in i or '世赞' in i or '小不点' in i:
            lsz.append(i)
    count = [len(csz), len(lzs), len(szx), len(lgz), len(jzg), len(gary), len(haha), len(qsm), len(lsz)]
    print(count)
    source = ColumnDataSource(data=dict(name=name, counts=count,
                                        color=['orange', 'yellowgreen', 'pink', 'darksalmon', 'lightgreen',
                                               'paleturquoise', 'lightsteelblue', 'hotpink', 'yellow']))
    p = figure(x_range=name, y_range=(0, 600), plot_height=250, title="话题度排行",
               toolbar_location=None, tools="")
    p.vbar(x='name', top='counts', color='color', width=0.9, source=source)
    p.legend.orientation = "horizontal"
    # p.legend.location = "top_right"
    show(p)

def comment(com):
    df = pandas.DataFrame()
    pl = []
    stopword = ['的', '了', '是', '。', '，', ' ', '？', '！', '就', '\n', '：', '“', '”', '*', '=', '（', '）', '吗', '吧', '(',
                ')', '・', '[', ']', '、', '°', '？', '！', '.', '-', '｀', '；', ',', '《', '》']
    for i in range(len(com)):
        cut_list = jieba.cut(com[i], cut_all=False)
        w = '/'.join(cut_list)
        w = w.split('/')
        for j in w:
            if not j in stopword:
                pl.append(j)
    for s in set(pl):
        if len(s) > 1:
            if pl.count(s) > 50:
                x = {}
                x['word'] = s.strip()
                x['count'] = pl.count(s)
                df = df.append(x, ignore_index=True)
                # print(df)
                '''
                x = {}
                x['word'] = s.strip('\n')
                x['count'] = pl.count(s)
                x=[]
                x.append(s)
                x.append(pl.count(s))
                word.append(x)
    word=sorted(word,key=lambda i:i[1],reverse=True)

    word=[('弹幕', 1479), ('真的', 1086), ('什么', 827)]
    print(type(word))
    word=json.loads(word)
    print(word)
    #pf=pandas.DataFrame()
    #pf = pf.append(word,ignore_index=True)
    pf=pandas.DataFrame.from_dict(word)'''
    #print(df)
    df.to_csv('kfc.csv', encoding='utf-8', index=False, mode='a', header=False)
    print(df)
    # return word
def snownlp(com):
    '''
    q = []
    for i in com:
        s = SnowNLP(i)
        q.append(round(s.sentiments, 1))
    print(q)
    emotion = []
    count = []
    for i in sorted(set(q)):
        emotion.append(str(i))
        count.append(q.count(i))
    print(count)
    print(emotion)
    print(type(emotion))'''
    count=[658, 565, 530, 545, 661, 712, 970, 950, 1115, 1451, 1914]
    emotion=['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']
    output_file('麦当劳评论情感分析.html')
    source = ColumnDataSource(data=dict(emotion=emotion, counts=count))
    p = figure(x_range=emotion, y_range=(0, 2000), plot_height=250, title="麦当劳评论情感分析",
               toolbar_location=None, tools="")
    p.vbar(x='emotion', top='counts', width=0.9, source=source)
    p.legend.orientation = "horizontal"
    show(p)

from pyecharts import Geo, Bar, Pie, Line, Radar


def male(sex):
    print(sex)
    att = ['男', '女', '保密']
    val = []
    for i in att:
        val.append(sex.count(i))
    pie = Pie("", "麦当劳性别饼图", title_pos="middle", width=1200, height=600)
    pie.add("", att, val, label_text_color=None, is_label_show=True, legend_orient='vertical',
            is_more_utils=True, legend_pos='left')
    pie.render("sexPie.html")

def network_edg_csv():
    keys = ['肯德基', '麦当劳', '德克士']
    xx = ['肯德基', '麦当劳', '德克士']

    kfc = [14363, 2291, 191]
    md = [2425, 11510, 149]
    dks = [202, 124, 2261]
    for i in range(len(kfc)):
        kfc[i] = round(kfc[i] / 14363, 4) * 100
    for i in range(len(md)):
        md[i] = round(md[i] / 11510, 4) * 100
    for i in range(len(dks)):
        dks[i] = round(dks[i] / 2261, 4) * 100
    k=[kfc,md,dks]
    print(k)
    k=pandas.DataFrame(k)
    fig=pyl.figure()
    names=['kfc', 'md', 'dks']
    ax=fig.add_subplot(figsize=(100, 100)) # 图片大小为20*20  
    ax=seaborn.heatmap(k, cmap='rainbow',linewidths = 0.05, vmax = 100,vmin = 0,annot = True, annot_kws = {
        'size': 6, 'weight': 'bold'})
    # 热力图参数设置（相关系数矩阵，颜色，每个值间隔等）   
    pyl.xticks(np.arange(3) + 0.5, names,rotation=-90)# 横坐标标注点  
    pyl.yticks(np.arange(3) + 0.5, names,rotation=360)
    ax.set_title('Characteristic correlation')  # 标题设置
    #ax.set_xticklabels(ax.get_xticklabels(), rotation=-90)
    #pyl.savefig('cluster.tif', dpi=300)
    pyl.show()
network_edg_csv()

# 2.做一个词云
'''
filepath = '肯德基.csv'
# write_data(filepath)
com, time, floor, zan, sex, name, level, reply = read_data(filepath)  # 1代表星期一0代表星期天
comment(com)

#snownlp(com)#做情感分析
#male(sex)
#network_edg_csv(com)#做相关系数矩阵
#network()#做社交网络图
#ana_week(week)
#ana_day(day)
#ana_hour(hour)
#hot(com)#话题度排行
#com_zan(com,zan)#评论和赞的关系
day(day)
comment(com)#出词云图
#print(pl)
#'''