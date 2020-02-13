import pandas as pd
# bokeh
from bokeh.io import save
from bokeh.plotting import figure

df_fit = pd.read_csv("./test_file/activity_4450634582.csv")

# 平均ペースを時速に変換する
list_speed_num = []
for pace in df_fit["平均ペース"]:
    m = pace.split(":")[0]
    s = pace.split(":")[1]
    f = round(int(s) / 60, 2)
    minute = int(m) + f
    list_speed_num.append(round(60 / minute, 2))
df_fit["speed_num"] = list_speed_num

# 累積時間を変換する
list_time_num = []
for time in df_fit["累積時間"]:
    m = time.split(":")[-2]
    s = time.split(":")[-1]
    f = round(float(s) / 60, 2)
    try:
        h = time.split(":")[-3]
    except IndexError:
        h = 0
    list_time_num.append(int(h) * 60 + int(m) + f)
df_fit["time_num"] = list_time_num

# Bokeh
# 距離と時間のplot
TOOLTIPS = [
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
]
p = figure(
    tooltips=TOOLTIPS,
    plot_width=800,
    plot_height=400,
    x_axis_label="minute",
    y_axis_label="distance(km)",
    title="距離と時間")
p.line(x=df_fit["time_num"],  # X軸
       y=df_fit.index,  # Y軸
       line_width=5,  # 線の幅
       line_color='#084594',  # 線の色
       line_alpha=0.5,  # 線の彩度
       legend="距離"  # 凡例の表示名
       )
# htmlとして保存
save(p, filename='distance_time.html')

# 時間とペース
TOOLTIPS = [
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
]
p = figure(
    tooltips=TOOLTIPS,
    plot_width=800,
    plot_height=400,
    x_axis_label="minute",
    y_axis_label="speed(km/)",
    title="平均速度と時間")

p.line(x=df_fit["time_num"],  # X軸
       y=df_fit["speed_num"],  # Y軸
       line_width=5,  # 線の幅
       line_color='red',  # 線の色
       line_alpha=0.5,  # 線の彩度
       legend="平均速度"  # 凡例の表示名
       )
# htmlとして保存
save(p, filename='speed_time.html')
