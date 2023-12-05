import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DIST_SIZE = 100 # tamaño de la muestra
boxplots = []
boxplots.append(dict(
    dist=np.random.normal(0, 1, size=DIST_SIZE),
    label= "Normal\n$\mu=0, \sigma=1$" ,
    fill_color= "pink" ,
    brush_color= "deeppink" ))
boxplots.append(dict(
    dist=np.random.geometric(0.4, size=DIST_SIZE),
    label= "Geometric\n$p=0.4$" ,
    fill_color= "lightblue" ,
    brush_color= "navy" ))
boxplots.append(dict(
    dist=np.random.chisquare(2, size=DIST_SIZE),
    label= "Chi-squared\n$df=2$" ,
    fill_color= "lightgreen" ,
    brush_color= "darkgreen" ))

fig, ax = plt.subplots(figsize=(8, 6)) # 800x600 px
for i, boxplot in enumerate(boxplots):
    fcolor, bcolor = boxplot["fill_color"], boxplot["brush_color"]
    ax.boxplot(boxplot["dist"],
      labels=[boxplot["label"]],
      positions=[i],
      widths=[.3],
      notch=True,
      patch_artist=True,
      boxprops=dict(edgecolor=bcolor,  facecolor=fcolor, linewidth=2),
      capprops=dict(color=bcolor, linewidth=2),
      flierprops=dict(color=bcolor, markerfacecolor=fcolor, linestyle= "none", markeredgecolor="none", markersize=9),
      medianprops=dict(color=bcolor),
      whiskerprops=dict(color=bcolor,linewidth=1),
      showmeans=True)
ax.yaxis.grid(color="lightgray")
ax.xaxis.set_ticks_position("none")
ax.yaxis.set_ticks_position("none")
ax.spines["right"].set_visible(False) # ocultar borde derecho
ax.spines["top"].set_visible(False) # ocultar borde superior
fig.tight_layout()
    
plt.show()
