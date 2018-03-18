import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


from plotly.offline import plot, iplot
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import quandl
import plotly.figure_factory as ff
import matplotlib as mpl
import plotly.plotly as py

from Rom_figures import corr
from Rom_figures import gdp
from Rom_figures import dopc
from Rom_figures import dopct
from Rom_figures import srm

gdp_data = quandl.get("FRED/GDP", authtoken = "xu1RpiEyfmLi7p5rE1UN")

app=dash.Dash()

app.css.append_css({"external_url": 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
app.title="Homework 5"

app.layout=html.Div([
	
	#ROW1

	html.Div([html.H1(children="Homework 5", style={"color":"brown", "text-align":"center", "font-family":"helvetica",
		"font-weight":"bold", "font-size":"40px",})],
		className="twelve columns"),


	# ROW2

		html.Div([
			
			html.Div([

			dcc.RadioItems(id="radio", options=[
            {"label": "Employee Churn", "value": corr}],
            value="show"),

            dcc.RadioItems(id="radio", options=[
            {"label": "Startup RoadMap", "value": srm}],
            value="show")

            ], className="three columns"),

			
			html.Div([
			dcc.Graph(id="Graphs")],
			className="nine columns"),

			], className="twelve columns"),



	#ROW3

		html.Div([
			html.Div([dcc.Dropdown(
				id = 'dropdown',
				options=[
	            {'label': 'Google', 'value': 'GOOGL'},
	            {'label': 'Apple', 'value': 'AAPL'},
	            {'label': 'Microsoft', 'value': 'MSFT'},
	            {'label': 'Amazon', 'value': 'AMZN'},
	            {'label': 'General Electric', 'value': 'GE'}

	            ], placeholder='Please, select a stock', multi=True),
			
			html.Button(id='submit',n_clicks=0, children='Submit'),
			], className="two columns"),

			html.Div([
			dcc.Graph(id="Boxplot")],
			className="five columns"),

			html.Div([
			dcc.Graph(id="Table")],
			className="five columns"),

			], className="twelve columns"),




	#ROW4
		
		html.Div([
			html.Div([dcc.RangeSlider(id = 'option_in', min=0, max=len(gdp_data.index), value=[0, len(gdp_data.index)])],
			className="four columns"),

			html.Div([dcc.Graph(id="GDP")],
			className="eight columns"),
			
			], className="twelve columns")
		
		




		])

#Button

@app.callback(
    Output(component_id="Graphs", component_property="figure"),
    [Input(component_id="radio", component_property="value")])

def update_graph(input_value1):
    figure=input_value1
    return figure

    


#Dropdown(callback)

@app.callback(
    Output(component_id='Boxplot', component_property='figure'),
    [Input(component_id='submit', component_property='n_clicks')],
    [State(component_id='dropdown', component_property='value')])

def update_graph(clicks, input_value2):
	quandl_input1 = "WIKI/"+input_value2[0]
	quandl_input2 = "WIKI/"+input_value2[1]
	
	stock_data1 = quandl.get(quandl_input1, authtoken = "xu1RpiEyfmLi7p5rE1UN")
	stock_data2 = quandl.get(quandl_input2, authtoken = "xu1RpiEyfmLi7p5rE1UN")
	
	x_values1 = stock_data1.Open.pct_change()
	x_values2 = stock_data2.Open.pct_change()
	
	trace1 = go.Box(x=x_values1, name=input_value2[0])
	trace2 = go.Box(x=x_values2, name=input_value2[1])
	
	layout_dopc = dict(title="<i>Distribution of Price changes</i> "+input_value2[0]+" and "+input_value2[1])
	data_dopc = [trace1,trace2]
	figure = dict(data=data_dopc, layout=layout_dopc)
	return figure

#DOPC table(callback)
@app.callback(
    Output(component_id='Table', component_property='figure'),
    [Input(component_id='submit', component_property="n_clicks")],
    [State(component_id='dropdown', component_property='value')]
)


def update_table(clicks, input_value2):
	quandl_input3 ="WIKI/"+input_value2[0]
	quandl_input4 = "WIKI/"+input_value2[1]
	
	stock_data3 = quandl.get(quandl_input3, authtoken = "xu1RpiEyfmLi7p5rE1UN")
	stock_data4 = quandl.get(quandl_input4, authtoken = "xu1RpiEyfmLi7p5rE1UN")
	
	stock_data3["PC"]=stock_data3.Open.pct_change()
	stock_data4["PC"]=stock_data4.Open.pct_change()
	
	stock_data3=stock_data3.iloc[1:5,-1:].round(3)
	stock_data4=stock_data4.iloc[1:5,-1:].round(3)
	
	header= dict(values=[input_value2[0],input_value2[1]],
				align=["left", "center"],
				font=dict(color="white",
				size=12),
				fill=dict(color="#119DFF"))
	
	cells=dict(values=[stock_data3.values, stock_data4.values],
			align=["left", "center"],
			fill=dict(color=["yellow", "white"]))
	
	trace_dopct=go.Table(header=header, cells=cells)
		
	data_dopct=[trace_dopct]	
	layout_dopct=dict(width=500, height=300)	
	table=dict(data=data_dopct, layout=layout_dopct)
	
	return table



#Slider(callback)

@app.callback(
    Output(component_id='GDP', component_property='figure'),
    [Input(component_id='option_in', component_property='value')]
)
def update_graph(input_value3):

	gdp_index = gdp_data.index[input_value3[0]:input_value3[1]]
	gdp_values = gdp_data.Value[input_value3[0]:input_value3[1]]

	trace_gdp = [go.Scatter(x=gdp_index,y=gdp_values,fill="tozeroy")]
	layout_gdp = dict(title = '<b>US GDP over time</b>')
	figure = dict(data=trace_gdp, layout = layout_gdp)
	return figure


if __name__ == '__main__':
    app.run_server()