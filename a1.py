# Name : RESHMI CHATTERJEE
# Roll Number : 2019441

import urllib.request
import datetime

def getLatestRates():
	""" Returns: a JSON string that is a response to a latest rates query.
	The JSON string will have the attributes rates, base and date (yyyy-mm-dd).
	"""
	url =  urllib.request.urlopen("https://api.exchangeratesapi.io/latest") 
	data = url.read()
	return data 

def currencyIndex(currency, date):
	y="https://api.exchangeratesapi.io/" + date
	url =  urllib.request.urlopen(y) #put link
	x = url.read()
	x=str(x)
	if (x.find('error'))>-1:
		return "error"
	b = x.index(currency)
	if currency=="EUR":
		return 1.00
	value = x[ (x.index(":",b) + 1) : x.index("," , b) ]
	return float(value)


def changeBase(amount, currency, desiredCurrency, date):
	# amount is of type int
	# currency and desiiredCurrency are of type string (INR, USD etc.)
	# date is string "yyyy-mm-dd"
	# return type is float
	if currency==desiredCurrency:
		return float(amount)
	cv = currencyIndex(currency, date)
	if cv=="error":
		return "error"
	dcv = currencyIndex(desiredCurrency, date)
	if dcv=="error":
		return "error"
	value = amount * (dcv / cv)
	return value



def printAscending(json):
	""" Output: the sorted order of the Rates
	Parameter json: a json string to parse
	You don't have to return anything.
	"""
	x=str(json)
	b = x.find("{")
	b = x.find("{",b+1)
	c=x.find("}")
	x=x[b+1:c] + "," #"cad":3232, ....
	a=x.count(":") #number of currency
	a=int(a)
	l=[] #list l =[["sdsa",43],[],...]
	j=-1
	for i in range(a):
		j=x.find(":",j+1)
		k=x.find(",",j)
		curr=x[j-4:j-1]
		curval=float(x[j+1:k])
		abc=[curr,curval]
		l.append(abc)
	for i in range(a-1):
		for j2 in range (a -i -1):
			if l[j2][1]>l[j2+1][1]:
				t=l[j2]
				l[j2]=l[j2+1]
				l[j2+1]=t
	for i in range(a-1):
		print("1 Euro = ",l[i][1],l[i][0])






#........
def dateSeparate(d):
	y=int(d[0:4])
	m=int(d[5:7])
	d=int(d[8:])
	date=datetime.datetime(y,m,d)
	return date
#.....

def l3curr(json,c,d): #c=currency d=date
	a=json.find(d)
	if a==-1:
		return "error"
	json=json[a:]
	b=json.rfind(c)
	d=json.index(":",b) + 1
	e=json.index("," , b)
	value = json[ d : e ]
	return float(value)


def extremeFridays(startDate, endDate, currency):
	""" Output: on which friday was currency the strongest
	    and on which was it the weakest
	    You don't have to return anything.

	    Parameters: stardDate and endDate are strings of
	    the form yyyy-mm-dd

	    currency is also a string representing the currency
	    whose extremes you have to determine
	"""

	y="https://api.exchangeratesapi.io/history?start_at=" + startDate + "&end_at=" + endDate
	url =  urllib.request.urlopen(y) #put link
	x = url.read()
	x=str(x)

	s=dateSeparate(startDate)
	e=dateSeparate(endDate)
	ld=[] #list of days exclusive of start and end -- datetime,string form

	es = e - s       

	for j in range(1,es.days):
		d = s + datetime.timedelta(days=j)
		l=[]
		l.append(d)
		d=str(d)
		l.append(d[0:10])
		ld.append(l)

	fri=[] #list of fridays

	l=len(ld)
	for i in range(l):
		if((ld[i][0].weekday()==4)and(l3curr(x,currency, ld[i][1])!="error")):
			ld[i].append(currencyIndex(currency, ld[i][1]))
			fri.append(ld[i])
	l=len(fri)
	for i in range(l-1):
		for j2 in range (l -i -1):
			if fri[j2][2]>fri[j2+1][2]:
				t=fri[j2]
				fri[j2]=fri[j2+1]
				fri[j2+1]=t

	print(currency,"was strongest on", fri[0][1], ". 1 Euro was equal to",fri[0][2],currency)

	print(currency,"was weakest on", fri[l-1][1], ". 1 Euro was equal to",fri[l-1][2],currency)



def findMissingDates(startDate, endDate):
	""" Output: the dates that are not present when you 
	    do a json query from startDate to endDate

	   Parameters: startDate and endDate are strings of
	   the form yyyy-mm-dd
	"""
	print("The following dates were not present:")

	y="https://api.exchangeratesapi.io/history?start_at=" + startDate + "&end_at=" + endDate
	url =  urllib.request.urlopen(y) #put link
	x = url.read()
	x=str(x)

	# find dates and print
	s=dateSeparate(startDate)
	e=dateSeparate(endDate)
	ld=[] #list of days exclusive of start and end -- datetime,string form

	es = e - s       

	for j in range(1,es.days):
		d = s + datetime.timedelta(days=j)
		l=[]
		l.append(d)
		d=str(d)
		l.append(d[0:10])
		ld.append(l)

	fri=[] #list of missing days
	currency="INR"

	l=len(ld)
	for i in range(l):
		if(l3curr(x,currency, ld[i][1])=="error"):
			print(ld[i][1])
