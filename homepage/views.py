from django.shortcuts import render, HttpResponse
import pandas as pd
from scipy import spatial as sp
#import matplotlib.pyplot as plt
#from matplotlib import style
#style.use('fivethirtyeight')

# Create your views here.
def home(request):

	df = pd.read_csv('C:/Users/19san/DjangoProjects/gramener/india-districts-census-2011.csv')

	#1st question
	#Grouping all the distrcits into states
	literacy_rate = df.groupby('State name')['Population','Literate'].sum()

	#Calculating literacy percent of each state and sorting all the states
	literacy_rate['literacy_percent'] = ((literacy_rate['Literate'])*100.0/literacy_rate['Population']).round(3)
	literacy_rate.sort_values(by=['literacy_percent'],inplace=True)
	
	literacy_rate_json = literacy_rate.to_json(orient='index')

	#2nd Question
	#Extracting districts of bihar and tamilnadu
	df_bihar = df[(df['State name'] == 'BIHAR')].iloc[:,2:]
	df_tamilNadu = df[(df['State name'] == 'TAMIL NADU')].iloc[:,2:]
	df_bihar_json,df_tamilNadu_json = df_bihar.to_json(orient='index'),df_tamilNadu.to_json(orient='index')
	
	#normalising the columns so that value of one column does not mask the effect of others
	for col in df_bihar.iloc[:,1:]:
		df_bihar[col] = (df_bihar[col]-df_bihar[col].min())/(df_bihar[col].max()-df_bihar[col].min())
		df_tamilNadu[col] = (df_tamilNadu[col]-df_tamilNadu[col].min())/(df_tamilNadu[col].max()-df_tamilNadu[col].min())
	
	#caluclating eucledian distance of each data point from one another
	similarity_score = pd.DataFrame(sp.distance.cdist(df_bihar.iloc[:,1:], df_tamilNadu.iloc[:,1:], metric='euclidean'),index = list(df_bihar['District name']),columns = list(df_tamilNadu['District name']))
	
	#converting eucledian distance into similarity score
	similarity_score = similarity_score.applymap(lambda x: (100/(1+x))).round(3)
	
	df_tamilNadu.set_index('District name',inplace=True)
	df_bihar.set_index('District name',inplace=True)
	similarity_score_json,df_bihar_json,df_tamilNadu_json = similarity_score.to_json(orient='index'),df_bihar.to_json(orient='index'),df_tamilNadu.to_json(orient='index')

	#3rd Question
	#Grouping all the distrcits into states
	mobile_pen = df.groupby('State name')['Workers','Agricultural_Workers','Households','Households_with_Telephone_Mobile_Phone'].sum()
	
	#Calculating Agricultural_Workers_% & Mobile_Penetration_% of each state
	mobile_pen['Agricultural_Workers_percent'] = ((mobile_pen['Agricultural_Workers'])*100.0/mobile_pen['Workers']).round(3)
	mobile_pen['Mobile_Penetration_percent'] = ((mobile_pen['Households_with_Telephone_Mobile_Phone'])*100.0/mobile_pen['Households']).round(3)
	
	#Sorting the states on the basis of Agricultural_Workers_
	mobile_pen.sort_values(by=['Agricultural_Workers_percent'],inplace=True)
	
	#Calculating Agricultural_Workers_% & Mobile_Penetration_% of each district in all the states
	df['Agricultural_Workers_percent'] = ((df['Agricultural_Workers'])*100.0/df['Workers']).round(3)
	df['Mobile_Penetration_percent'] = ((df['Households_with_Telephone_Mobile_Phone'])*100.0/df['Households']).round(3)
	
	mobile_pen_json,df_json = mobile_pen.to_json(orient='index'),df.to_json(orient='index')

	args = {'literacy_json':literacy_rate_json, 'df_bihar_json':df_bihar_json, 'df_tamilNadu_json':df_tamilNadu_json, 'similarity_json':similarity_score_json, 'mobile_pen_json':mobile_pen_json, 'df_json':df_json}

	return render(request, 'homepage.html', args)