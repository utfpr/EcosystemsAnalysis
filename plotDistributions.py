import sys
import os
import plotly
import plotly.offline as offline
import plotly.graph_objs as go
import math
from ecosystemDataManager.ecosystemDataManager import EcosystemDataManager

def plotHistogram(vector, name_histogram):
	trace = go.Histogram(
		name='Results',
		x = vector,
		xbins=dict(
			start=1,
			end=50,
			size=0.5
		)
	)
	data = [trace]
	plotly.offline.plot(data, filename=name_histogram)

def plotHistograms(vectors, name_histogram):
	data = []
	for vector in vectors:
		trace = go.Histogram(
			x = vectors[vector],
			name = vector,
			xbins=dict(
				start=0,
				end=2,
				size=0.1,
			)
		)
		data.append(trace)
	plotly.offline.plot(data, filename=name_histogram)
	

def plotBoxPlot(vector, name_boxplot):
	trace0 = go.Box(
		y=vector,
	)
	data = [trace0]
	plotly.offline.plot(data, filename=name_boxplot)

def plotMultBoxPlot(vectors, name_boxplot):
	data = []
	for vector in vectors:
		trace = go.Box(
			y=vectors[vector],
			boxpoints='all',
			name=vector
		)
		data.append(trace)
	# plotly.offline.plot(data, filename=name_boxplot)
	offline.plot({'data': [{'y': [4, 2, 3, 4]}], 
               'layout': {'title': 'Test Plot', 
                          'font': dict(size=16)}},
             image='png')



def plorBarChart(vector_x, vector_y, nameBarChart):
	data = [go.Bar(
	        x=vector_x,
	        y=vector_y
	)]	
	plotly.offline.plot(data, filename=nameBarChart)


def plotMultBarsChart(setName, vector_x, vectors_y, nameBarChart):
	data = []
	i = 0
	for vector in vectors_y:
		trace = go.Bar(
			x=vector_x,
			y=vector,
			name=setName[i]
		)
		i += 1
		data.append(trace)
	layout = go.Layout(
    	barmode='group'
	)
	fig = go.Figure(data=data, layout=layout)
	plotly.offline.plot(fig, filename=nameBarChart)

def plorScatterChart(vector_x, vector_y, nameBarChart):
	data = [go.Scatter(
	        x=vector_x,
	        y=vector_y,
			mode = 'lines+markers'
	)]	
	plotly.offline.plot(data, filename=nameBarChart)

def plotMultScatterChart(setName, vector_x, vectors_y, nameBarChart):
	data = []
	i = 0
	for vector in vectors_y:
		trace = go.Scatter(
			x=vector_x,
			y=vector,
			name=setName[i],
			mode = 'lines+markers'
		)
		i += 1
		data.append(trace)
	plotly.offline.plot(data, filename=nameBarChart)

def plotMostPopularLicenses(keys, values, chartName):
	trace = go.Bar(
		name=chartName,
		y = values,
		x = keys
	)
	data = [trace]
	plotly.offline.plot(data, filename=chartName)

def plotPackageHistory(package, chartName):
	historyVersions = package.getHistory()
	listLocalRegularityRate = []
	listGlobalRegularityRate = []
	listGlobalRegularityMean = []
	versionsName = []
	for version in historyVersions:
		versionsName.append(version.getName())
		listLocalRegularityRate.append((version.getLocalRegularityRate()))
		listGlobalRegularityRate.append((version.getGlobalRegularityRate()))
		listGlobalRegularityMean.append((version.getGlobalRegularityMean()))
	setName = ["Local Regularity Rate", "Global Regularity Rate", "Global Regularity Mean"]
	plotMultScatterChart(setName, versionsName, [listLocalRegularityRate, listGlobalRegularityRate, listGlobalRegularityMean], chartName)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage:", sys.argv[0], "<ecosystem> [<package>] [only]")
		sys.exit(1)
	ecosystem = sys.argv[1]
	if len(sys.argv) > 2:
		package = sys.argv[2]
	else:
		print("<package> not provided. Most popular and irregular package will be used to plot their history")
		package = None
	try:
		os.makedirs("visualizations")
	except Exception as e:
		pass
	if "only" in sys.argv:
		print("plotting only package history")
	ecosystemDataManager = EcosystemDataManager(ecosystem)
	if "only" not in sys.argv:
		#packageSizeDistribution = [len(package) for package in ecosystemDataManager.getPackages()]
		#plotBoxPlot(packageSizeDistribution, "visualizations/" + ecosystem + '_boxplot_packageSizeDistribution.html')
		#plotHistogram(packageSizeDistribution, "visualizations/" + ecosystem + '_histogram_packageSizeDistribution.html')
		#irregularPackages = ecosystemDataManager.getMostPopularIrregularPackages(10)
		#irregularPackagesHasLocalRegularityRates = {irregularPackage.getName(): irregularPackage.getLocalRegularityRates() for irregularPackage in irregularPackages}
		#plotMultBoxPlot(irregularPackagesHasLocalRegularityRates, "visualizations/" + ecosystem + '_boxplot_regularityRateVersions.html')
		#plotHistograms(irregularPackagesHasLocalRegularityRates, "visualizations/" + ecosystem + '_histogram_regularityRateVersions.html')
		licenses = ecosystemDataManager.getMostPopularLicenses(50)		
		plotMostPopularLicenses([str(k) for k, v in licenses], [v for k, v in licenses], "visualizations/" + ecosystem + "_bars_mostPopularLicenses.html")
		plotMostPopularLicenses([str(k) for k, v in licenses], [math.log10(v) for k, v in licenses], "visualizations/" + ecosystem + "_bars_mostPopularLicenses_log10.html")
	if package:
		package = ecosystemDataManager.getPackage(package)
	else:
		package = irregularPackages[0]
	#plotPackageHistory(package, "visualizations/" + ecosystem + package.getName() + '_regularity_rate_bars.html')