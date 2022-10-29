import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./caption-rand-clip/merged_pred.csv')  ##CHANGE
sns.set(rc={'figure.figsize':(12, 8)})
sns.set(font_scale = 2)
sns.set_style("whitegrid")

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times"],
    'axes.labelsize': 42,
    'axes.titlesize':42,
    'xtick.labelsize':40,
    'ytick.labelsize':40
})

# print(len(df[df["full_ann_num_parts"]==6]))
#B) plot only one graph
g = sns.lineplot(data=df, x="ann_num_parts", y="avg_probability", hue="full_ann_num_parts", palette=sns.color_palette("rocket", 6), err_style="band")
g.set(xlabel = "\# of Parts Described and Colored", xticks=range(8))
g.set(ylabel = "Target Probability")
g.set_ylim(0,1)
g.set_xlim(0,7)
g.set(title='CLIP') ##CHANGE
# plt.legend(title='Number of parts in full annotation', loc='lower right')
plt.legend([],[], frameon=False)
plt.tight_layout()
plt.show()