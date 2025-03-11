#
#	Analizzatore Log per Maratona DX ARI Roma 2025
#	IZ0MJE Stefano - pubblico dominio
# 	nessuna garania sull'accuratezza dei risultati
#
# una lista conterrà i QSO qualificanti, che vengono aggiunti soltanto se utili
# il QSO è qualificante se "new one" per le categorie che assegnano punteggio

# country e zone sono dizionari che portano come primo elemento country o zona e come secondo elemento l'ordinale di lista del QSO

# elementi necessari: country, zona, modo, nominativo, timestamp

import sys

qualificanti = []
countries = {}
zones = {}
digitali = ['FT8','MFSK','FT4','RTTY','JT4','JT6M','JT9','JT44','JT65','PSK','QRA64']

def campo(nome,riga): 
	field_start = riga.find(nome)
	if field_start == -1:
		return('n/a')
	else:
		field_start = riga.find('>',field_start)
		field_end = riga.find('<',field_start)
		return(riga[field_start +1:field_end -1:])

print("========== QSO conteggiati ==========")

with open(sys.argv[1]) as file:
	for line in file:
		if len(line) > 72:
			nominativo = campo('<CALL:',line)
			
			country = campo('<COUNTRY:',line)
			if country == 'n/a':
				break
								
			modo = campo('<MODE:',line)
			if modo in digitali:
				modo = "digi"
			if (modo == "SSB") or (modo == "CW"):
				modo = "SSB/CW"
			banda = campo('<BAND:',line)
			
			data = campo('<QSO_DATE:',line)
			ora = campo('<TIME_ON:',line)
			zonacq = campo('<CQZ:',line)
			
			if nominativo == "IQ0RM":
				country = "ARI Roma"
				qso = nominativo + "," + country + "," + modo + "," + banda + "," + data + "," + ora + "," + zonacq +  ",3"
			else:
				qso = nominativo + "," + country + "," + modo + "," + banda + "," + data + "," + ora + "," + zonacq +  ",1"


			# se il country non è ancora nella matrice
			if country not in countries:
				#	lo aggiungiamo alla lista dei qualificanti
				qualificanti.append(qso)
				qsoindex = len(qualificanti)
				#	lo aggiungiamo alla lista countries
				countries[country] = qsoindex
				print(qsoindex, end="")
				print(" - ", end="")
				print(qso, end="")
				print(" -- nuovo country")

			# altrimenti vediamo se ci serve per la zona
			elif zonacq not in zones:
				#	lo aggiungiamo alla lista dei qualificanti
				qualificanti.append(qso)
				qsoindex = len(qualificanti)
				#	lo aggiungiamo alla lista zone
				zones[zonacq] = qsoindex
				print(qsoindex, end="")
				print(" - ", end="")
				print(qso, end="")
				print(" -- nuova zona")

print("\n\n\n========== RIEPILOGO ==========")

# siccome ARI Roma l'abbiamo considerata come un country, bisogna togliere 1 dal conteggio, se collegata
print("Countries		", end="")
if "ARI Roma" in countries:
	punt_ctry = len(countries.keys())-1
else:
	punt_ctry = len(countries.keys())
print(punt_ctry)

print("Zone			", end="")
punt_zone = len(zones.keys())
print(punt_zone)

if "ARI Roma" in countries:
	punt_iq0rm = 3
else:
	punt_iq0rm = 0

print("IQ0RM			", end="")
print(punt_iq0rm)
print("-------------------------------")
print("Totale			", end="")
print(punt_ctry + punt_zone + punt_iq0rm)

print("\n\n\n========== Zone non collegate ==========")
for i in range (1,40):
	if str(i) not in zones:
		print(i, end=" ")
	i += 1
print()
