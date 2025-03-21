#
#	Analizzatore Log per Maratona DX ARI Roma 2025
#	IZ0MJE Stefano - pubblico dominio
# 	nessuna garanzia sull'accuratezza dei risultati
#
# una lista conterrà i QSO qualificanti, che vengono aggiunti soltanto se utili
# il QSO è qualificante se "new one" per le categorie che assegnano punteggio

# country e zone sono dizionari che portano come primo elemento country o zona e come secondo elemento l'ordinale di lista del QSO

# elementi necessari: country, zona, modo, nominativo, timestamp
# v 0.6 15 Mar 2025 - corretto errore nel conteggio / elenco delle zone
# v 0.5 14 Mar 2025 - aggiunta generazione rapportino in file "calcolo-maratona.txt"
# v 0.4 14 Mar 2025 - aggiunto supporto per log generati da BBLOGGER
# v 0.3 13 Mar 2025 - aggiunto supporto per log generati da QLog e avviso su assenza zone (QARTest)
# v 0.2 12 Mar 2025 - aggiunto supporto per log che non inserisca il nome del country ma solo numero DXCC
# v 0.1 11 Mar 2025 - release iniziale


import sys

logfile = ''
qualificanti = []
countries = {}
zones = {}
digitali = ['FT8','MFSK','FT4','RTTY','JT4','JT6M','JT9','JT44','JT65','PSK','QRA64']
dxcc = {
	0:'None',
	1:'CANADA',
	2:'ABU AIL IS.',
	3:'AFGHANISTAN',
	4:'AGALEGA & ST. BRANDON IS.',
	5:'ALAND IS.',
	6:'ALASKA',
	7:'ALBANIA',
	8:'ALDABRA',
	9:'AMERICAN SAMOA',
	10:'AMSTERDAM & ST. PAUL IS.',
	11:'ANDAMAN & NICOBAR IS.',
	12:'ANGUILLA',
	13:'ANTARCTICA',
	14:'ARMENIA',
	15:'ASIATIC RUSSIA',
	16:'NEW ZEALAND SUBANTARCTIC ISLANDS',
	17:'AVES I.',
	18:'AZERBAIJAN',
	19:'BAJO NUEVO',
	20:'BAKER & HOWLAND IS.',
	21:'BALEARIC IS.',
	22:'PALAU',
	23:'BLENHEIM REEF',
	24:'BOUVET',
	25:'BRITISH NORTH BORNEO',
	26:'BRITISH SOMALILAND',
	27:'BELARUS',
	28:'CANAL ZONE',
	29:'CANARY IS.',
	30:'CELEBE & MOLUCCA IS.',
	31:'C. KIRIBATI (BRITISH PHOENIX IS.)',
	32:'CEUTA & MELILLA',
	33:'CHAGOS IS.',
	34:'CHATHAM IS.',
	35:'CHRISTMAS I.',
	36:'CLIPPERTON I.',
	37:'COCOS I.',
	38:'COCOS (KEELING) IS.',
	39:'COMOROS',
	40:'CRETE',
	41:'CROZET I.',
	42:'DAMAO, DIU',
	43:'DESECHEO I.',
	44:'DESROCHES',
	45:'DODECANESE',
	46:'EAST MALAYSIA',
	47:'EASTER I.',
	48:'E. KIRIBATI (LINE IS.)',
	49:'EQUATORIAL GUINEA',
	50:'MEXICO',
	51:'ERITREA',
	52:'ESTONIA',
	53:'ETHIOPIA',
	54:'EUROPEAN RUSSIA',
	55:'FARQUHAR',
	56:'FERNANDO DE NORONHA',
	57:'FRENCH EQUATORIAL AFRICA',
	58:'FRENCH INDO-CHINA',
	59:'FRENCH WEST AFRICA',
	60:'BAHAMAS',
	61:'FRANZ JOSEF LAND',
	62:'BARBADOS',
	63:'FRENCH GUIANA',
	64:'BERMUDA',
	65:'BRITISH VIRGIN IS.',
	66:'BELIZE',
	67:'FRENCH INDIA',
	68:'KUWAIT/SAUDI ARABIA NEUTRAL ZONE',
	69:'CAYMAN IS.',
	70:'CUBA',
	71:'GALAPAGOS IS.',
	72:'DOMINICAN REPUBLIC',
	74:'EL SALVADOR',
	75:'GEORGIA',
	76:'GUATEMALA',
	77:'GRENADA',
	78:'HAITI',
	79:'GUADELOUPE',
	80:'HONDURAS',
	81:'GERMANY',
	82:'JAMAICA',
	83:'n/a',
	84:'MARTINIQUE',
	85:'BONAIRE, CURACAO',
	86:'NICARAGUA',
	87:'n/a',
	88:'PANAMA',
	89:'TURKS & CAICOS IS.',
	90:'TRINIDAD & TOBAGO',
	91:'ARUBA',
	93:'GEYSER REEF',
	94:'ANTIGUA & BARBUDA',
	95:'DOMINICA',
	96:'MONTSERRAT',
	97:'ST. LUCIA',
	98:'ST. VINCENT',
	99:'GLORIOSO IS.',
	100:'ARGENTINA',
	101:'GOA',
	102:'GOLD COAST, TOGOLAND',
	103:'GUAM',
	104:'BOLIVIA',
	105:'GUANTANAMO BAY',
	106:'GUERNSEY',
	107:'GUINEA',
	108:'BRAZIL',
	109:'GUINEA-BISSAU',
	110:'HAWAII',
	111:'HEARD I.',
	112:'CHILE',
	113:'IFNI',
	114:'ISLE OF MAN',
	115:'ITALIAN SOMALILAND',
	116:'COLOMBIA',
	117:'ITU HQ',
	118:'JAN MAYEN',
	119:'JAVA',
	120:'ECUADOR',
	122:'JERSEY',
	123:'JOHNSTON I.',
	124:'JUAN DE NOVA, EUROPA',
	125:'JUAN FERNANDEZ IS.',
	126:'KALININGRAD',
	127:'KAMARAN IS.',
	128:'KARELO-FINNISH REPUBLIC',
	129:'GUYANA',
	130:'KAZAKHSTAN',
	131:'KERGUELEN IS.',
	132:'PARAGUAY',
	133:'KERMADEC IS.',
	134:'KINGMAN REEF',
	135:'KYRGYZSTAN',
	136:'PERU',
	137:'REPUBLIC OF KOREA',
	138:'KURE I.',
	139:'KURIA MURIA I.',
	140:'SURINAME',
	141:'FALKLAND IS.',
	142:'LAKSHADWEEP IS.',
	143:'LAOS',
	144:'URUGUAY',
	145:'LATVIA',
	146:'LITHUANIA',
	147:'LORD HOWE I.',
	148:'VENEZUELA',
	149:'AZORES',
	150:'AUSTRALIA',
	151:'MALYJ VYSOTSKIJ I.',
	152:'MACAO',
	153:'MACQUARIE I.',
	154:'YEMEN ARAB REPUBLIC',
	155:'MALAYA',
	157:'NAURU',
	158:'VANUATU',
	159:'MALDIVES',
	160:'TONGA',
	161:'MALPELO I.',
	162:'NEW CALEDONIA',
	163:'PAPUA NEW GUINEA',
	164:'MANCHURIA',
	165:'MAURITIUS',
	166:'MARIANA IS.',
	167:'MARKET REEF',
	168:'MARSHALL IS.',
	169:'MAYOTTE',
	170:'NEW ZEALAND',
	171:'MELLISH REEF',
	172:'PITCAIRN I.',
	173:'MICRONESIA',
	174:'MIDWAY I.',
	175:'FRENCH POLYNESIA',
	176:'FIJI',
	177:'MINAMI TORISHIMA',
	178:'MINERVA REEF',
	179:'MOLDOVA',
	180:'MOUNT ATHOS',
	181:'MOZAMBIQUE',
	182:'NAVASSA I.',
	183:'NETHERLANDS BORNEO',
	184:'NETHERLANDS NEW GUINEA',
	185:'SOLOMON IS.',
	186:'NEWFOUNDLAND, LABRADOR',
	187:'NIGER',
	188:'NIUE',
	189:'NORFOLK I.',
	190:'SAMOA',
	191:'NORTH COOK IS.',
	192:'OGASAWARA',
	193:'OKINAWA (RYUKYU IS.)',
	194:'OKINO TORI-SHIMA',
	195:'ANNOBON I.',
	196:'PALESTINE',
	197:'PALMYRA & JARVIS IS.',
	198:'PAPUA TERRITORY',
	199:'PETER 1 I.',
	200:'PORTUGUESE TIMOR',
	201:'PRINCE EDWARD & MARION IS.',
	202:'PUERTO RICO',
	203:'ANDORRA',
	204:'REVILLAGIGEDO',
	205:'ASCENSION I.',
	206:'AUSTRIA',
	207:'RODRIGUES I.',
	208:'RUANDA-URUNDI',
	209:'BELGIUM',
	210:'SAAR',
	211:'SABLE I.',
	212:'BULGARIA',
	213:'SAINT MARTIN',
	214:'CORSICA',
	215:'CYPRUS',
	216:'SAN ANDRES & PROVIDENCIA',
	217:'SAN FELIX & SAN AMBROSIO',
	218:'CZECHOSLOVAKIA',
	219:'SAO TOME & PRINCIPE',
	220:'SARAWAK',
	221:'DENMARK',
	222:'FAROE IS.',
	223:'ENGLAND',
	224:'FINLAND',
	225:'SARDINIA',
	226:'SAUDI ARABIA/IRAQ NEUTRAL ZONE',
	227:'FRANCE',
	228:'SERRANA BANK & RONCADOR CAY',
	229:'GERMAN DEMOCRATIC REPUBLIC',
	230:'FEDERAL REPUBLIC OF GERMANY',
	231:'SIKKIM',
	232:'SOMALIA',
	233:'GIBRALTAR',
	234:'SOUTH COOK IS.',
	235:'SOUTH GEORGIA I.',
	236:'GREECE',
	237:'GREENLAND',
	238:'SOUTH ORKNEY IS.',
	239:'HUNGARY',
	240:'SOUTH SANDWICH IS.',
	241:'SOUTH SHETLAND IS.',
	242:'ICELAND',
	243:'PEOPLES DEMOCRATIC REP. OF YEMEN',
	244:'SOUTHERN SUDAN',
	245:'IRELAND',
	246:'SOVEREIGN MILITARY ORDER OF MALTA',
	247:'SPRATLY IS.',
	248:'ITALY',
	249:'ST. KITTS & NEVIS',
	250:'ST. HELENA',
	251:'LIECHTENSTEIN',
	252:'ST. PAUL I.',
	253:'ST. PETER & ST. PAUL ROCKS',
	254:'LUXEMBOURG',
	255:'ST. MAARTEN, SABA, ST. EUSTATIUS',
	256:'MADEIRA IS.',
	257:'MALTA',
	258:'SUMATRA',
	259:'SVALBARD',
	260:'MONACO',
	261:'SWAN IS.',
	262:'TAJIKISTAN',
	263:'NETHERLANDS',
	264:'TANGIER',
	265:'NORTHERN IRELAND',
	266:'NORWAY',
	267:'TERRITORY OF NEW GUINEA',
	268:'TIBET',
	269:'POLAND',
	270:'TOKELAU IS.',
	271:'TRIESTE',
	272:'PORTUGAL',
	273:'TRINDADE & MARTIM VAZ IS.',
	274:'TRISTAN DA CUNHA & GOUGH I.',
	275:'ROMANIA',
	276:'TROMELIN I.',
	277:'ST. PIERRE & MIQUELON',
	278:'SAN MARINO',
	279:'SCOTLAND',
	280:'TURKMENISTAN',
	281:'SPAIN',
	282:'TUVALU',
	283:'UK SOVEREIGN BASE AREAS ON CYPRUS',
	284:'SWEDEN',
	285:'VIRGIN IS.',
	286:'UGANDA',
	287:'SWITZERLAND',
	288:'UKRAINE',
	289:'UNITED NATIONS HQ',
	291:'UNITED STATES OF AMERICA',
	292:'UZBEKISTAN',
	293:'VIET NAM',
	294:'WALES',
	295:'VATICAN',
	296:'SERBIA',
	297:'WAKE I.',
	298:'WALLIS & FUTUNA IS.',
	299:'WEST MALAYSIA',
	301:'W. KIRIBATI (GILBERT IS. )',
	302:'WESTERN SAHARA',
	303:'WILLIS I.',
	304:'BAHRAIN',
	305:'BANGLADESH',
	306:'BHUTAN',
	307:'ZANZIBAR',
	308:'COSTA RICA',
	309:'MYANMAR',
	312:'CAMBODIA',
	315:'SRI LANKA',
	318:'CHINA',
	321:'HONG KONG',
	324:'INDIA',
	327:'INDONESIA',
	330:'IRAN',
	333:'IRAQ',
	336:'ISRAEL',
	339:'JAPAN',
	342:'JORDAN',
	344:'DEMOCRATIC PEOPLES REP. OF KOREA',
	345:'BRUNEI DARUSSALAM',
	348:'KUWAIT',
	354:'LEBANON',
	363:'MONGOLIA',
	369:'NEPAL',
	370:'OMAN',
	372:'PAKISTAN',
	375:'PHILIPPINES',
	376:'QATAR',
	378:'SAUDI ARABIA',
	379:'SEYCHELLES',
	381:'SINGAPORE',
	382:'DJIBOUTI',
	384:'SYRIA',
	386:'TAIWAN',
	387:'THAILAND',
	390:'TURKEY',
	391:'UNITED ARAB EMIRATES',
	400:'ALGERIA',
	401:'ANGOLA',
	402:'BOTSWANA',
	404:'BURUNDI',
	406:'CAMEROON',
	408:'CENTRAL AFRICA',
	409:'CAPE VERDE',
	410:'CHAD',
	411:'COMOROS',
	412:'REPUBLIC OF THE CONGO',
	414:'DEMOCRATIC REPUBLIC OF THE CONGO',
	416:'BENIN',
	420:'GABON',
	422:'THE GAMBIA',
	424:'GHANA',
	428:'COTE DIVOIRE',
	430:'KENYA',
	432:'LESOTHO',
	434:'LIBERIA',
	436:'LIBYA',
	438:'MADAGASCAR',
	440:'MALAWI',
	442:'MALI',
	444:'MAURITANIA',
	446:'MOROCCO',
	450:'NIGERIA',
	452:'ZIMBABWE',
	453:'REUNION I.',
	454:'RWANDA',
	456:'SENEGAL',
	458:'SIERRA LEONE',
	460:'ROTUMA I.',
	462:'REPUBLIC OF SOUTH AFRICA',
	464:'NAMIBIA',
	466:'SUDAN',
	468:'KINGDOM OF ESWATINI',
	470:'TANZANIA',
	474:'TUNISIA',
	478:'EGYPT',
	480:'BURKINA FASO',
	482:'ZAMBIA',
	483:'TOGO',
	488:'WALVIS BAY',
	489:'CONWAY REEF',
	490:'BANABA I. (OCEAN I.)',
	492:'YEMEN',
	493:'PENGUIN IS.',
	497:'CROATIA',
	499:'SLOVENIA',
	501:'BOSNIA-HERZEGOVINA',
	502:'NORTH MACEDONIA (REPUBLIC OF)',
	503:'CZECH REPUBLIC',
	504:'SLOVAK REPUBLIC',
	505:'PRATAS I.',
	506:'SCARBOROUGH REEF',
	507:'TEMOTU PROVINCE',
	508:'AUSTRAL I.',
	509:'MARQUESAS IS.',
	510:'PALESTINE',
	511:'TIMOR-LESTE',
	512:'CHESTERFIELD IS.',
	513:'DUCIE I.',
	514:'MONTENEGRO',
	515:'SWAINS I.',
	516:'SAINT BARTHELEMY',
	517:'CURACAO',
	518:'SINT MAARTEN',
	519:'SABA & ST. EUSTATIUS',
	520:'BONAIRE',
	521:'SOUTH SUDAN (REPUBLIC OF)',
	522:'REPUBLIC OF KOSOVO'
}

def conv_qlog(nomefile):
	fileout = nomefile.removesuffix('.adi') + "-conv.adi"
	outfile = open(fileout, 'w')
	riga = ''
	with open(nomefile, 'r') as file:
		for line in file:
			line = line.strip()
			line = line.upper()
			riga = riga + line
			if line == '<EOH>':
				riga = ''
			if line == '<EOR>':
				riga = riga + '\r\n'
				outfile.write(riga)
				riga = ''
	outfile.close()
	file.close()
	return(fileout)



def campo(nome,riga): 
	field_start = riga.find(nome)
	if field_start == -1:
		return('n/a')
	else:
		field_start = riga.find('>',field_start)
		field_end = riga.find('<',field_start)
		return(riga[field_start +1:field_end:])

print("========== QSO conteggiati ==========")

logoriginale = sys.argv[1]


def checkapp(nomefile):
	logfile = ''
	with open(logoriginale) as origfile:
		for line in origfile:
			logapp = campo('PROGRAMID:',line)
			if (logapp == 'QLog') or (logapp == 'BBLOGGER'):
				logfile = conv_qlog(logoriginale)
				break
			else:
				logfile = logoriginale
	origfile.close()
	return(logfile)

logfile = checkapp(logoriginale)

with open(logfile) as file:
	rendiconto = open('calcolo-maratona.txt', 'w')
	for line in file:			
		havectry = 0 # controllo se abbiamo un country valido
		subline = line.split('<EOR>')
		for entry in subline:
			if len(entry) > 72:
				nominativo = campo('<CALL:',entry)
				country = campo('<COUNTRY:',entry)
				if country == 'n/a':
					dxccnr = campo('<DXCC:',entry)
					if dxccnr == 'n/a':
						break
					else:
						country = dxcc[int(dxccnr)]
						havectry = 1
				else:
					havectry = 1
			
				if havectry == 0:
					break
				
				modo = campo('<MODE:',entry)
				if modo in digitali:
					modo = "digi"
				if (modo == "SSB") or (modo == "CW"):
					modo = "SSB/CW"
				banda = campo('<BAND:',entry)
			
				data = campo('<QSO_DATE:',entry)
				ora = campo('<TIME_ON:',entry)
				zonacq = campo('<CQZ:',entry)
				if zonacq == 'n/a':
					print("==== il record non contiene zona CQ ===")
			
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

					print(qsoindex, end="", file=rendiconto)
					print(" - ", end="", file=rendiconto)
					print(qso, end="", file=rendiconto)
					print(" -- nuovo country", file=rendiconto)


				# altrimenti vediamo se ci serve per la zona
				elif zonacq not in zones and zonacq != 'n/a':
					#	lo aggiungiamo alla lista dei qualificanti
					qualificanti.append(qso)
					qsoindex = len(qualificanti)
					#	lo aggiungiamo alla lista zone
					zones[zonacq] = qsoindex
					print(qsoindex, end="", file=rendiconto)
					print(" - ", end="", file=rendiconto)
					print(qso, end="", file=rendiconto)
					print(" -- nuova zona", file=rendiconto)

					print(qsoindex, end="")
					print(" - ", end="")
					print(qso, end="")
					print(" -- nuova zona")

print("\n\n\n========== RIEPILOGO ==========")
print("\n\n\n========== RIEPILOGO ==========", file=rendiconto)

# siccome ARI Roma l'abbiamo considerata come un country, bisogna togliere 1 dal conteggio, se collegata
print("Countries		", end="")
print("Countries		", end="", file=rendiconto)


if "ARI Roma" in countries:
	punt_ctry = len(countries.keys())-1
else:
	punt_ctry = len(countries.keys())
print(punt_ctry)
print(punt_ctry, file=rendiconto)


print("Zone			", end="")
print("Zone			", end="", file=rendiconto)

punt_zone = len(zones.keys())
print(punt_zone)
print(punt_zone, file=rendiconto)


if "ARI Roma" in countries:
	punt_iq0rm = 3
else:
	punt_iq0rm = 0

print("IQ0RM			", end="")
print(punt_iq0rm)
print("-------------------------------")
print("Totale			", end="")
print(punt_ctry + punt_zone + punt_iq0rm)

print("IQ0RM			", end="", file=rendiconto)
print(punt_iq0rm, file=rendiconto)
print("-------------------------------", file=rendiconto)
print("Totale			", end="", file=rendiconto)
print(punt_ctry + punt_zone + punt_iq0rm, file=rendiconto)

print("\n\n\n========== Zone collegate ==========")
print("\n\n\n========== Zone collegate ==========", file=rendiconto)

for i in range (1,41):
	if str(i) in zones:
		print(i, end=" ")
		print(i, end=" ", file=rendiconto)
	i += 1
print()
print(file=rendiconto)

print("\n\n\n========== Zone non collegate ==========")
print("\n\n\n========== Zone non collegate ==========", file=rendiconto)


for i in range (1,41):
	if str(i) not in zones:
		print(i, end=" ")
		print(i, end=" ", file=rendiconto)
	i += 1
print()
print(file=rendiconto)

rendiconto.close()
