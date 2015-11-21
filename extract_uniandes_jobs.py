import requests
from bs4 import BeautifulSoup
import csv

USERNAME = 'YOUR_USER_NAME'
PASSWORD = 'YOUR_PASSWORD'

LOGIN_URL = 'https://ctp.uniandes.edu.co/_joomla/index.php?option=com_content&view=section&id=11&Itemid=391'
LISTING_URL = 'https://ctp.uniandes.edu.co/_joomla/index.php?option=com_content&view=section&id=10&Itemid=384'
DETAIL_URL = 'https://ctp.uniandes.edu.co/_joomla/index.php?option=com_content&view=section&id=5&Itemid=386'

session = requests.session()


reqheaders = {
	'Content-Type': 'application/x-www-form-urlencoded'
}

formdata = {
	'aspirante[login]' : USERNAME,
	'aspirante[clave]' : PASSWORD
}

print("Connexion...")
r = session.post(LOGIN_URL, data=formdata, headers=reqheaders, allow_redirects=False)
print("Connecté")


formdata = {
	'oportunidad[servicio]': '2',
	'fechas': 'todas',
	'desde': '',
	'hasta': '',
	'oportunidad[anosexperiencia]': '',
	'buscar': 'Buscar'
}

print("Récupération des offres...")
r = session.post(LISTING_URL, data=formdata, headers=reqheaders, allow_redirects=False)
print("Récupéré")

print("Parsing...")
soup = BeautifulSoup(r.text)

table  = soup.find(id="tabla_formas_grande")

data = []

rows = table.find_all('tr')
for row in rows:
	cols = row.find_all('td')
	cols = [ele.text.strip() for ele in cols]
	data.append(cols)

with open('jobs.csv', 'w') as csvfile:
	jobswriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)
	iterjobs = iter(data)
	next(iterjobs)
	next(iterjobs)
	for job in iterjobs:
		formdata = {
			'oportunidad': job[0],
			'servicio': '2'
		}
		print("Récupération de l'offre...")
		r = session.post(DETAIL_URL, data=formdata, headers=reqheaders, allow_redirects=False)
		print("Récupérée")
		print("Parsing offre...")
		soup = BeautifulSoup(r.text)
		tables = soup.find_all("table")
		rows = tables[4].find_all("tr")
		salario_row = rows[16]
		salario_cols = salario_row.find_all('td')
		salario = salario_cols[1]	
		funciones_row = rows[18]
		funciones_cols = funciones_row.find_all('td')
		funciones = funciones_cols[1]
		print("Offre parsé")
		jobswriter.writerow([job[0], job[2], job[3], job[4], salario.text.strip(), funciones.text.strip()])
print("Fichier csv écrit")
