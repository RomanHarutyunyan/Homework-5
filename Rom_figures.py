from plotly.offline import plot, iplot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import quandl
import plotly.figure_factory as ff
import matplotlib as mpl
import plotly.plotly as py

data1 = quandl.get("FRED/GDP", authtoken = "xu1RpiEyfmLi7p5rE1UN")
data2 = quandl.get("WIKI/GOOGL", authtoken = "xu1RpiEyfmLi7p5rE1UN")
data3 = quandl.get("BCHARTS/ABUCOINSUSD", authtoken = "xu1RpiEyfmLi7p5rE1UN")





#Graph1

x_values1_corr = ["X8","X7","X6","X5"]
x_values2_corr = ["X4","X3","X2","X1"]

y_values1_corr = [17,45,17,20]
y_values2_corr = [-17,-45,-5,-37]

trace1_corr = go.Bar(y=x_values1_corr, x=y_values1_corr, name="<b>Negative</b>", orientation="h", marker=dict(color="coral", line=dict(color="dark brown", width=1.5)))
trace2_corr = go.Bar(y=x_values2_corr, x=y_values2_corr, name="Positive", orientation="h", marker=dict(color="lightblue", line=dict(color="black", width=1.5)))

layout = dict(title="<b>Correlations with employees probability of churn</b>",
              yaxis=dict(title="Variable"))

data = [trace1_corr,trace2_corr]
corr = dict(data=data, layout=layout)



#Graph2

x_values_gdp = pd.to_datetime(data1.index.values)
y_values_gdp = data1.Value
trace_gdp = go.Scatter(x=x_values_gdp, y=y_values_gdp,
                      mode="lines", fill= "tozeroy")
layout_gdp = dict(title="<b>US GDP over time</b>")
data_gdp = [trace_gdp]
gdp = dict(data=data_gdp, layout=layout_gdp)


#Graph3

x_values1_dopc=data2.Open.pct_change()
x_values2_dopc=data3.Open.pct_change()

trace1_dopc=go.Box(x=x_values2_dopc, name="<b>Bitcoin</b>")
trace2_dopc=go.Box(x=x_values1_dopc, name="<b>Google</b>")

layout_dopc=dict(title="<i>Distribution of Price changes</i>")

data_dopc = [trace1_dopc,trace2_dopc]
dopc = dict(data=data_dopc, layout=layout_dopc)


#Graph4

header= dict(values=["Google","Bitcoin"],
             align=["left", "center"],
             font=dict(color="white", size=12),
             fill=dict(color="#119DFF")
            )

data2["PC"]=data2.Open.pct_change()
data3["PC"]=data3.Open.pct_change()

data2_1=data2.iloc[1:5,-1:].round(3)
data3_1=data3.iloc[1:5,-1:].round(3)

data2_2=data2_1.values
data3_2=data3_1.values

cells = dict(values=[data2_2, data3_2],
             align = ["left","center"],
             fill = dict(color=["yellow","white"])
            )
trace_dopct = go.Table(header=header, cells=cells)

data_dopct = [trace_dopct]
layout_dopct = dict(width=500, height=300)
dopct = dict(data=data_dopct, layout=layout_dopct)



#Graph5

trace_srm=[dict(Task='Task 1', Start='2018-01-01', Finish='2018-01-31', Resource='Idea validation'),
           dict(Task='Task 2', Start='2018-03-01', Finish='2018-04-15', Resource='Team formation'),
           dict(Task='Task 3', Start='2018-04-17', Finish='2018-09-30', Resource='Prototyping')]

data_srm= ff.create_gantt(trace_srm,title="Startup Roadmap", index_col='Resource', reverse_colors=False, show_colorbar=True)

layout_srm= dict(title="Startup Roadmap")

srm = dict(data=data_srm, layout=layout_srm)