import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import json
import scipy
from scipy.optimize import linear_sum_assignment
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize as tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
import numpy as np
from numpy import dot
from numpy.linalg import norm
np.random.seed(1)
from nltk.stem.porter import *
stemmer = PorterStemmer()
import math
from statistics import mean


f = open('../../batch_final.json')
data = json.load(f)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times"],
    'axes.labelsize': 25,
    'axes.titlesize':25,
    'xtick.labelsize':25,
    'ytick.labelsize':25
})

###########segmentation##############

'''
d: {1:str, 2:str, ..., 7:str}
returns s: e.g. [[1,2,5],[4],[3,6,7]]
'''
def make_sets(d):
    s=[]
    rev=defaultdict(list)
    for k,v in d.items():
        rev[v].append(k)
    for ann, ind_set in rev.items():
        s.append(ind_set)
    return s

def weight(s1,s2):
    return -len(set(s1)&set(s2)) #make negative bc we're finding the MAX number of pieces that do not change

'''
l1,l2: e.g. [[1,2,5],[4],[3,6,7]]
returns: len(l1)*len(l2) cost matrix matching elm from l1 to l2
'''
def cost_matrix(l1,l2):
    mat = np.zeros((len(l1),len(l2)))
    for i in range(len(l1)):
        for j in range(len(l2)):
            mat[i][j] = weight(l1[i],l2[j])
    return mat

'''
d1,d2: piece-annotation dictionaries
returns: number, higher value == higher agreement (MAX number of pieces that do not change)
'''
def seg_agreement(d1,d2):
    cost = cost_matrix(make_sets(d1),make_sets(d2))
    row_ind, col_ind = linear_sum_assignment(cost)
    return -cost[row_ind, col_ind].sum()
            

file_to_segagr = defaultdict(int)
for file, anns in data['annotations'].items():
    piece_anns = [detail['piece-annotation'] for detail in anns.values()]
    mean_agr=0
    l=len(piece_anns)
    for i in range(l-1):
        for j in range(i+1,l):
            mean_agr += seg_agreement(piece_anns[i],piece_anns[j])
    mean_agr /= l*(l-1)/2
    file_to_segagr[file] = mean_agr   


###########pp##############
def clean(x):
    words = tokenize(x.lower())
    wl = [w for w in words if w not in stop_words and (w.islower() or w.isalnum())]
    return wl

#vocab size
words = defaultdict(int)
for file, anns in data['annotations'].items():
    for user, detail in anns.items():
        wl = clean(detail['whole-annotation']['wholeAnnotation'])
        for w in wl:
            words[stemmer.stem(w)] += 1
print('Vocab size: ', len(words))
print('Total words: ', sum(words.values()))
vocab = list(words.keys())
len(vocab)

'''
[whole_anns]: all whole shape annotations of a tangram (tokenized, removed stopwords, lowercased) 
{user: [anns]}
[user]: user to exclude
returns: normalized smoothed word probability for every word in [anns]
'''
def build_lm(whole_anns, user, k=1/100, V=2651):
    p={}
    word_to_count=defaultdict(int)
    total=0
    for uid, a in whole_anns.items():
        if uid!=user:
            for w in a:
                word_to_count[stemmer.stem(w)]+=1 #stemmed
                total+=1
    for w, c in word_to_count.items():
        p[w]=(c+k) / (total+k*V)
    return p, total

'''
returns: normalized smoothed word probability for word [w] in vocabulary based on [p] yielded by lm
'''
def word_prob(p, total, w, k=1/100, V=2651):
    if w in p:
        return p[w]
    else:
        return k/(total+k*V)
    
'''
[x]: list of strings
'''
def calc_pp(x, p, total):
    s=0
    t=0 # test sum is 1
    for w in vocab:
        t+=word_prob(p,total,w)
    if not math.isclose(1, t):
        print(t)
    for w in x:
        s+= math.log(word_prob(p,total,w),2)
    return ((-1)/len(x))*s

file_to_wholeanns={} #{file: {user: [cleaned whole anns]}}
for file, anns in data['annotations'].items():
    whole_anns={}
    for user, d in anns.items():
        whole_anns[user]=clean(d['whole-annotation']['wholeAnnotation'])
    file_to_wholeanns[file]=whole_anns

file_to_pp={}
for file, anns in data['annotations'].items():
    pp=[]
    for user, d in anns.items():
        p,total = build_lm(file_to_wholeanns[file], user)
        x = file_to_wholeanns[file][user] # whole shape annotation of this annotator
        log_ppi=calc_pp(x,p,total)
        pp.append(log_ppi)
    file_to_pp[file] = 2**mean(pp)


###############graph####################
seg=[]
whole=[]
coord_to_f = {}
for f, agr in file_to_segagr.items():
    seg.append(agr)
    whole.append(file_to_pp[f])
    coord_to_f[(agr,file_to_pp[f])] = (f)

###grid###
def find_idx(arr, coord):
    for i in range(len(arr)-1):
        if coord>arr[i] and coord<=arr[i+1]:
            return i
    print(arr, coord)
    return None
            
def to_grid():
    cs=np.linspace(3.9, 5196, num=6)
    sa=np.linspace(3.85, 7, num=6)
    grid_to_coord=defaultdict(list) # each cell = list of coords
    coord_to_grid={}
    for (x,y), f in coord_to_f.items():
        i=find_idx(sa,x)
        j=find_idx(cs,y)
        grid_to_coord[(i,j)].append((x,y,f))
        coord_to_grid[(x,y)] = (i,j)
    #grid_to_coord: {grid: [(coord_x, coord_y, file),...]}
    #coord_to_grid: {(coord_x,coord_y): (grid_x,grid_y)}
    return grid_to_coord, coord_to_grid
    

import random
def pick_coord(grid_to_coord, num=1):
    grid_to_samples={}
    for g, coords in grid_to_coord.items():
        if len(coords)<num:
            grid_to_samples[g] = random.sample(coords, len(coords))
        else:
            grid_to_samples[g] = random.sample(coords, num)
    return grid_to_samples

#pick from grids
grid_to_coord, coord_to_grid = to_grid()
picked = pick_coord(grid_to_coord)

#pick from all
all_coords = [item for sublist in list(grid_to_coord.values()) for item in sublist]
# print(len(all_coords))
all_except_picked = [a for a in all_coords if a not in picked]
all_coords_sample = random.sample(all_except_picked, 25)

np.random.seed(1)

###hover###
x = seg
y = whole
c = np.random.randint(1,1004,size=1004)

norm = plt.Normalize(1,1003)
cmap = plt.cm.RdYlGn

fig,ax = plt.subplots()
sc = plt.scatter(x,y)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)


p=0
for grid, samples in picked.items():
    for (x,y,f) in samples:
        plt.text(x=x, y=y, s=f)
        plt.scatter(x, y, c='red')
        print(f)
        p+=1
print('sampled by grids:', p)

p=0
for x,y,f in all_coords_sample:
      plt.text(x=x, y=y, s=f)
      plt.scatter(x, y, c='green')
      print(f)
      p+=1
print('sampled overall:', p)

# periphery = [
#     "page2-34.svg",
#     "page9-46.svg",
#     "page3-85.svg",
#     "page7-107.svg",
#     "page8-159.svg",
#     "page6-203.svg",
#     "page2-112.svg",
#     "page1-116.svg",
#     "page1-69.svg",
#     "page8-234.svg",
#     "page8-21.svg",
#     "page5-75.svg",
# ]

# grid_pick = [
#     "page1-0.svg",
#   "page5-59.svg",
#   "page3-121.svg",
#   "page6-164.svg",
#   "page4-128.svg",
#   "page5-136.svg",
#   "page6-99.svg",
#   "page7-14.svg",
#   "page5-128.svg",
#   "page9-27.svg",
#   "page7-105.svg",
#   "page6-162.svg",
#   "page9-13.svg",
#   "page1-128.svg",
#   "page5-186.svg",
#   "page3-72.svg",
#   "page4-157.svg",
#   "page3-182.svg",
#   "page7-197.svg",
#   "page7-180.svg",
#   "page6-143.svg",
#   "page7-81.svg",
#   "page3-136.svg",
#   "page5-64.svg",
#   "page7-218.svg",
# ]

# random_pick = [
#   "page3-128.svg",
#   "page7-26.svg",
#   "page6-78.svg",
#   "page4-24.svg",
#   "page5-153.svg",
#   "page7-248.svg",
#   "page5-244.svg",
#   "page4-93.svg",
#   "page5-28.svg",
#   "page8-235.svg",
#   "page5-200.svg",
#   "page2-131.svg",
#   "page8-183.svg",
#   "page1-119.svg",
#   "page5-232.svg",
#   "page1-129.svg",
#   "page4-162.svg",
#   "page3-41.svg",
#   "page6-180.svg",
#   "page6-149.svg",
#   "page1-105.svg",
#   "page4-10.svg",
#   "page5-178.svg",
#   "page2-137.svg",
#   "page3-35.svg",
# ]


# for f in periphery:
#     f=f.replace('.svg','')
#     x=file_to_segagr[f]
#     y=file_to_pp[f]
#     plt.text(x=x, y=y, s=f, size=18)
#     plt.scatter(x, y, c='purple')
# for f in grid_pick:
#     f=f.replace('.svg','')
#     x=file_to_segagr[f]
#     y=file_to_pp[f]
#     plt.text(x=x, y=y, s=f, size=18)
#     plt.scatter(x, y, c='red')
# for f in random_pick:
#     f=f.replace('.svg','')
#     x=file_to_segagr[f]
#     y=file_to_pp[f]
#     plt.text(x=x, y=y, s=f, size=18)
#     plt.scatter(x, y, c='green')




def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    coord = (pos[0],pos[1])
    text = coord_to_f[coord]+' '+str(coord)
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(cmap(0))
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)
plt.rc('font', size=15)
plt.xlabel("Part Segmentation Agreement (PSA)")
plt.ylabel("Log Perplexity, k=1/100")
plt.yticks(np.linspace(3.9, 5196, num=6))
plt.xticks(np.linspace(3.85, 7, num=6))
plt.grid()
plt.show()
# plt.savefig('sample.pdf')
