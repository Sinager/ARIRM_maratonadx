#
#	Analizzatore Log per Maratona DX ARI Roma 2025
#	IZ0MJE Stefano - pubblico dominio
# 	nessuna garanzia sull'accuratezza dei risultati
#
# una lista conterrà i QSO qualificanti, che vengono aggiunti soltanto se utili
# il QSO è qualificante se "new one" per le categorie che assegnano punteggio

# country e zone sono dizionari che portano come primo elemento country o zona e come secondo elemento l'ordinale di lista del QSO

# elementi necessari: country, zona, modo, nominativo, timestamp
# v 0.11 31 Dic 2025 - crea il file "calcolo-maratona.csv" in modo da poter essere incollato sul formato Excel ufficiale
# v 0.10 30 Dic 2025 - implementato sistema di controllo sulle zone dichiarate
# v 0.9 28 Dic 2025 - corretto errore su indicazione "nuova zona" - tnx IU0PXQ per la segnalazione
# v 0.8 28 Dic 2025 - corretto errore conteggio zone - tnx IU0QME per la segnalazione
# v 0.7 28 Dic 2025 - aggiunto supporto per log generati da QRZLogbook
# v 0.6 15 Mar 2025 - corretto errore nel conteggio / elenco delle zone
# v 0.5 14 Mar 2025 - aggiunta generazione rapportino in file "calcolo-maratona.txt"
# v 0.4 14 Mar 2025 - aggiunto supporto per log generati da BBLOGGER
# v 0.3 13 Mar 2025 - aggiunto supporto per log generati da QLog e avviso su assenza zone (QARTest)
# v 0.2 12 Mar 2025 - aggiunto supporto per log che non inserisca il nome del country ma solo numero DXCC
# v 0.1 11 Mar 2025 - release iniziale


import sys
import os

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
	522:'REPUBLIC OF KOSOVO',
	999:'ARI ROMA'
}

# Dizionario DXCC <> ZONE
# POSSONO ESSERCI ANCORA ERRORI PERCHE' PARZIALMENTE COMPILATA DA AI GOOGLE GEMINI CHE HA FATTO UN PESSIMO LAVORO
dxcc_cq_zones = {
    1: [1, 2, 3, 4, 5],  # Canada
    2: [5],               # St. Paul Island
    3: [15],              # Monaco
    4: [39],              # Mauritius
    5: [33],              # Algeria
    6: [1],               # Alaska
    7: [15],              # Albania
    10: [23, 24],         # China
    11: [26],              # Andaman & Nicobar Islands
    12: [8],              # ANGUILLA
    13: [12, 13, 29, 30, 32, 38, 39],              # ANTARCTICA
    14: [15],				# CZECH REP.
    15: [16,17,18,19],      # ASIATIC RUSSIA
    16: [32],				# NEW ZEALAND SUBANTARCTIC ISLANDS
    17: [9],				# AVES IS.
    18: [21],				# AZERBAIJAN
    20: [31],              # BAKER & HOWLAND IS.
    21: [14],              # Balearic Islands
    22: [27],					# PALAU
    23: [0],					# BLENHEIM REEF deleted
    24: [33],              # Madeira Islands
    27: [16],              # BELARUS
    29: [33],              # Canary Islands
    31: [8],               # Bahamas
    32: [33],              # Ceuta & Melilla
    35: [29], 				# CHRISTMAS I.
    37: [8],               # Dominican Republic
    38: [29],				# COCOS (KEELING) IS.
    40: [40],              # Iceland
    42: [25],              # South Korea
    43: [8],               # Puerto Rico
    45: [20],          		# DODECANESE
    46: [28],				# EAST MALAYSIA
    48: [31],				# EAST KIRIBATI
    49: [36],				# EQUATORIAL GUINEA
    50: [6],               # Mexico
    52: [17],              # Tajikistan
    53: [37],              # ETHIOPIA
    54: [16],              # European Russia
    56: [11],					# FERNANDO DE NORONHA
    61: [8],               # British Virgin Islands
    62: [31],              # Nauru
    63: [9],               # FRENCH GUYANA
    64: [8],               # Montserrat
    65: [8],               # Anguilla
    66: [33],              # Western Sahara
    69: [8],              # CAYMAN IS.
    70: [8],               # Cuba
    71: [10],               # GALAPAGOS
    72: [8],              # DOMINICAN REPUBLIC
    74: [14],              # Faroe Islands
    75: [21],              # Georgia
    76: [7],               # Guatemala
    77: [8],               # Grenada
    78: [8],               # Haiti
    79: [8],               # Guadeloupe
    80: [7],               # Nicaragua
    82: [8],               # Jamaica
    84: [8],               # St. Kitts & Nevis
    86: [8],               # St. Lucia
    88: [7],               # PANAMA
    89: [8],               # TURKS & CAICOS IS.
    90: [10],               # TRINIDAD & TOBAGO
    91: [8],               # Turks & Caicos Islands
    94: [8],               # Antigua & Barbuda
    95: [8],               # Barbados
    96: [8],               # Dominica
    97: [8],				# ST. LUCIA
    98: [8],					# ST. VINCENT
    100: [13],             # Argentina
    103: [27],             # Guam
    104: [31],             # Baker & Howland Islands
    105: [8],              # Guantanamo Bay
    106: [14],              # GUERNSEY
    107: [35],             # Guinea
    108: [11],             # Brazil
    109: [35],				# Guinea-Bissau
    110: [31],             # Kure Island
    112: [12],             # Chile
    114: [14],             # ISLE OF MAN
    116: [9],              # Colombia
    117: [14],             # ITU HQ (4U1ITU)
    118: [40],             # Jan Mayen
    120: [10],             # Ecuador (HC8)
    122: [14],				# JERSEY
    123: [31],             # Johnston Island
    125: [12],             # Juan Fernandez Islands
    126: [31],             # Western Kiribati (T30)
    129: [9],              # Guyana
    130: [17],             # Kazakhstan
    132: [11],             # Paraguay
    134: [31],             # Kingman Reef
    135: [17],             # KYRGYZSTAN
    136: [9],              # PERU
    137: [25],				# REPUBLIC OF KOREA
    138: [31],             # Midway Island
    140: [9],				# SURINAME
    141: [14],             # France
    142: [22],             # Lakshadweep Islands
    143: [26],				# LAOS
    144: [13],             # Uruguay
    145: [15],             # LATVIA
    146: [16],             # LITHUANIA
    147: [15],             # Vatican City
    148: [9],              # Venezuela
    149: [14],             # AZORES
    150: [29, 30],         # Australia
    151: [30],             # Lord Howe Island
    152: [30],             # Mellish Reef
    153: [32],             # Norfolk Island
    154: [30],             # Willis Island
    155: [28],             # Christmas Island (VK9X)
    157: [17, 18, 19],     # Asiatic Russia
    158: [31],             # Eastern Kiribati (T32)
    159: [22],             # Maldives
    160: [32],             # Tonga
    162: [32],				# NEW CALEDONIA
    163: [15],             # Kaliningrad (UA2)
    166: [27],             # MARIANA IS.
    167: [28],             # Cocos (Keeling) Islands
    168: [22],             # Sri Lanka
    169: [39],             # MAYOTTE
    170: [32],             # New Zealand
    171: [32],             # Kermadec Islands
    172: [32],             # Chatham Islands
    173: [27],             # MICRONESIA
    175: [28],             # Indonesia
    176: [32],             # Fiji
    177: [27],             # Minami Torishima
    179: [16],             # MOLDOVA
    180: [32],             # Tokelau Islands
    181: [37],             # Mozambique
    182: [32],             # American Samoa
    185: [39],             # Reunion Island
    187: [35],             # Niger
    188: [32],				# NIUE
    189: [32],				# NORFOLK I.
    190: [32],             # Samoa
    191: [32],             # North Cook Islands
    192: [27],             # Ogasawara
    195: [36],             # Annobon Island
    197: [31],             # Palmyra & Jarvis Islands
    199: [21],             # Azerbaijan
    200: [0],				# PORTUGUESE TIMOR --- deleted
    201: [15],             # Albania
    202: [8],              # Puerto Rico
    203: [14],             # Andorra
    204: [31],             # Wake Island
    205: [28],             # Solomon Islands
    206: [15],             # AUSTRIA
    207: [39],             # Rodriguez Island
    208: [0],                # RUANDA URUNDI
    209: [14],             # Spain
    211: [32],             # Wallis & Futuna Islands
    212: [20],             # Bulgaria
    213: [8],             	# ST MARTIN
    214: [15],             # CORSICA
    215: [20],             # Cyprus
    216: [11],             # SAN ANDRES & PROVIDENCIA
    217: [12],             # San Felix & San Ambrosio
    218: [7],              # Belize
    219: [8],              # Cayman Islands
    221: [14],             # Denmark
    222: [31],             # Marquesas Islands
    223: [14],             # England
    224: [15],             # FINLAND
    225: [15],             # Sardinia
    226: [27],             # Micronesia
    227: [14],             # France
    228: [27],             # Palau
    229: [32],             # Austral Islands
    230: [14],             # Federal Republic of Germany
    232: [37],              # SOMALIA
    233: [14],				# GIBRALTAR
    234: [32],				# SOUTH COOK IS.
    235: [32],             # French Polynesia
    236: [20],             # GREECE
    237: [27],             # Mariana Islands
    239: [15],             # Hungary
    240: [13],				# SOUTH SANDWICH IS.
    242: [39],             # Tromelin Island
    243: [39],             # Crozet Island
    245: [14],             # Ireland
    247: [15],             # S.M.O.M. (1A0)
    248: [15, 33],         # Italy
    249: [8],             	# ST. KITTS & NEVIS
    250: [36],             # ST. HELENA
    251: [14],             # Isle of Man
    252: [14],             # Jersey
    253: [14],             # Guernsey
    254: [14],             # Luxembourg
    256: [33],          	# Madeira Islands
    257: [15],             # Malta
    259: [40],             # Svalbard
    260: [14],				# MONACO
    263: [14],             # Netherlands
    265: [14],             # Wales
    266: [14],             # Norway
    269: [15],             # POLAND
    270: [14],             # Belgium
    272: [14],             # Portugal
    273: [11],				# TRINDADE & MARTIM VAZ IS.
    274: [38],				# TRISTAN DA CUNHA & GOUGH I.
    275: [20],             # Romania
    277: [5],			 	# ST. PIERRE & MIQUELON
    278: [15],             # San Marino
    279: [14],             # Scotland
    281: [14],             # Spain
    284: [14],             # Sweden
    285: [8],             # VIRGIN IS.
    286: [37],             # Uganda
    287: [14],             # Switzerland
    288: [16],             # UKRAINE
    289: [5],              # United Nations HQ (4U1UN)
    291: [3, 4, 5],        # USA
    294: [14],             # WALES
    295: [15],             # Slovak Republic
    296: [15],             # Serbia
    297: [31],				# WAKE IS.
    298: [32],				# WALLIS & FUTUNA IS.
    299: [28],              # WEST MALAYSIA
    301: [31],				# W. KIRIBATI (GILBERT IS. )
    302: [33, 34, 37],				# WESTERN SAHARA
    304: [21],             # Bahrain
    305: [22],				# BANGLADESH
    306: [22],             # Bhutan
    308: [7], 				# COSTA RICA
    312: [24],             # Taiwan
    315: [22],             # Sri Lanka
    318: [23, 24],         # China
    321: [24],				# HONG KONG
    324: [22],             # India
    327: [28],             # Indonesia
    330: [21],				# IRAN
    333: [21],             # Iraq
    336: [20],             # Israel
    339: [25],             # Japan
    342: [20],             # Jordan
    345: [28],				#  	BRUNEI DARUSSALAM
    348: [21],             # Kuwait
    351: [20],             # Lebanon
    354: [20],             # LEBANON
    363: [23],             # Mongolia
    369: [22],             # Nepal
    370: [21],             # Oman
    372: [21],             # Pakistan
    375: [27],             # Philippines
    376: [21],             # Qatar
    378: [21],             # Saudi Arabia
    379: [39],				# SEYCHELLES
    381: [28],             # Singapore
    384: [20],             # Syria
    386: [24],              # Taiwan (Alt)
    387: [26],              # Thailand
    390: [20],             # Turkey
    391: [21],             # United Arab Emirates
    400: [33],				# ALGERIA
    401: [36],             # Angola
    402: [38],             # Botswana
    404: [36],             # Burundi
    406: [36],             # Cameroon
    409: [35],             # Cape Verde
    410: [36],				# CHAD
    411: [39],				# COMOROS
    412: [36],             # Central African Republic
    414: [36],             # Dem. Rep. of the Congo
    416: [35],             # BENIN
    420: [36],             # Gabon
    422: [35],             # Gambia
    424: [35],             # Ghana
    428: [35],             # Ivory Coast
    430: [37],             # Kenya
    432: [38],             # Lesotho
    434: [35],             # Liberia
    436: [34],             # Libya
    438: [39],             # Madagascar
    440: [37],             # Malawi
    442: [35],             # Mali
    444: [35],             # Mauritania
    446: [33],             # Morocco
    450: [35],             # Nigeria
    453: [39],				# REUNION I.
    454: [36],             # Rwanda
    456: [35],             # Senegal
    457: [39],             # Seychelles
    458: [35],             # Sierra Leone
    460: [32],             # Rotuma Island
    462: [38],             # South Africa
    464: [38],             # Namibia
    466: [34],             # Sudan
    468: [33],             # Tunisia
    470: [37],             # Tanzania
    472: [35],             # Togo
    474: [33],             # TUNISIA
    478: [34],             # EGYPT
    480: [38],             # Zimbabwe
    482: [36], 				# ZAMBIA
    483: [35],				# TOGO
    489: [32],             # Conway Reef
    490: [31],             # Banaba Island
    492: [21],             # Yemen
    497: [15],             # Croatia
    499: [15],             # Slovenia
    501: [15],             # Bosnia-Herzegovina
    502: [15],             # North Macedonia
    503: [15], 				# CZECH REPUBLIC
    504: [15],             # SLOVAK REPUBLIC
    505: [24],             # Pratas Island
    506: [27],             # Scarborough Reef
    507: [32],             # TEMOTU PROVINCE
    508: [32],             # AUSTRAL I.
    509: [31],             # MARQUESAS IS.
    510: [20],             # Palestine
    511: [28],             # Timor-Leste
    512: [30],             # Chesterfield Islands
    513: [32],             # Ducie Island
    514: [15],             # Montenegro
    516: [8],				# SAINT BARTHELEMY
    517: [9],             # CURACAO
    518: [8],              # SINT MAARTEN
    519: [9],              # SABA & ST. EUSTATIUS
    520: [9],              # BONAIRE
    521: [34],              # SOUTH SUDAN (REPUBLIC OF)
    522: [15],             # REPUBLIC OF KOSOVO
    999: [15]				# ARI ROMA
}

# lista entità nell'ordine dell'Excel Maratona
maratona_ctry = [999,246,247,260,4,165,207,49,195,176,489,460,468,474,293,107,24,199,18,75,514,315,117,289,511,336,436,215,470,450,438,444,187,483,190,286,430,456,82,492,432,440,400,62,159,129,497,424,257,482,348,458,299,46,369,414,404,381,454,90,402,160,370,306,391,376,304,372,318,506,386,505,157,203,422,60,181,112,217,47,125,13,446,70,104,272,256,149,144,211,252,401,409,411,230,375,51,510,191,234,188,501,281,21,29,32,245,14,434,330,179,52,53,27,135,262,280,227,79,169,516,162,512,84,508,36,175,509,277,453,99,124,276,213,41,131,10,298,63,223,114,265,122,279,106,294,185,507,239,287,251,120,71,78,72,116,161,216,137,88,80,387,295,378,248,225,382,77,109,97,95,98,339,177,192,363,259,118,342,291,105,166,20,103,123,174,197,110,138,9,515,297,6,182,285,202,43,266,100,254,146,212,136,354,206,224,5,167,503,504,209,221,237,222,163,91,344,263,517,520,519,518,108,56,253,273,140,61,302,305,499,379,219,284,269,466,478,236,180,45,40,282,301,31,48,490,232,278,22,390,242,76,308,37,406,214,408,412,420,410,428,416,442,54,126,15,292,130,288,94,66,249,464,173,168,345,1,150,111,153,38,147,171,189,303,35,12,96,65,89,172,513,141,235,238,240,241,64,33,321,324,11,142,50,204,480,312,143,152,309,3,327,333,158,384,145,86,275,74,296,148,17,452,502,522,521,7,233,283,250,205,274,69,270,170,34,133,16,132,462,201]

bandemhz = {
	'160M': 1.8,
	'80M':	3.5,
	'60M':	5,
	'40M':	7,
	'30M':	10,
	'20M':	14,
	'17M':	18,
	'15M':	21,
	'12M':	24,
	'10M':	28,
	'6M':	50
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

print("========== QSO valutati ==========")

logoriginale = sys.argv[1]


def checkapp(nomefile):
	logfile = ''
	with open(logoriginale) as origfile:
		for line in origfile:
			logapp = campo('PROGRAMID:',line)
			if (logapp == 'QLog') or (logapp == 'BBLOGGER') or (logapp == 'QRZLogbook'):
				logfile = conv_qlog(logoriginale)
				break
			else:
				logfile = logoriginale
	origfile.close()
	return(logfile)

logfile = checkapp(logoriginale)
dxccnr = ''

with open(logfile) as file:
	rendiconto = open('calcolo-maratona.csv', 'w')
	for line in file:
		line = line.upper()			
		subline = line.split('EOR>')
		for entry in subline:
			if len(entry) > 72:
				nominativo = campo('<CALL:',entry)
				print(nominativo,end='')
				dxccnr = campo('<DXCC:',entry)
				if nominativo == "IQ0RM":
					dxccnr = 999
				if dxccnr == 81:
					dxccnr = 230
				print('	> DXCC # ',end='')
				print(dxccnr, end=' - ')
				if (dxccnr == 'n/a') or (dxccnr == ''):
					country = campo('<COUNTRY:',entry)
					dxccnr = list(dxcc.keys())[list(dxcc.values()).index(country)]
				else:
					country = dxcc[int(dxccnr)]

				modo = campo('<MODE:',entry)
				if modo in digitali:
					modo = "digi"
				if modo in ["SSB","LSB","USB","CW"]:
					modo = "SSB/CW"
				banda = campo('<BAND:',entry)
				if banda not in bandemhz.keys():
					print(banda,end=' ')
					print(' Banda non valida per la maratona - QSO scartato')
					break
			
				data = campo('<QSO_DATE:',entry)
				ora = campo('<TIME_ON:',entry)
				zonacq = campo('<CQZ:',entry)
				
				if (zonacq == 'n/a') or (zonacq == ''):
					print('----- Manca zona CQ - inserisco la prima della lista per il country >',end='')
					zonacq = str(dxcc_cq_zones[int(dxccnr)][0])
					print(zonacq,end=' ')
				else:					
					dxcc_cq_zones[int(dxccnr)]
					# verifica se la zona a log corrisponde a quelle ufficiali
					if int(zonacq) not in dxcc_cq_zones[int(dxccnr)]:
						print(' ----- mancata corrispondenza')
						print('	Risulta zona CQ ',end='')
						print(zonacq,end=' vs. ')
						print(dxcc_cq_zones[int(dxccnr)])
						print('	sostuituisco con la prima della lista > ',end='')
						zonacq = str(dxcc_cq_zones[int(dxccnr)][0])
				print('Zona CQ ',end='')
				zonacq = zonacq.strip()
				print(zonacq,end='')
				
				qso = "['" + data.strip() + "','" + ora.strip() + "','" + banda.strip() + "','" + modo.strip() + "','" + nominativo.strip() + "','" + zonacq + "']"
				
				#print('---QSO da processare---')
				#print(qso,end=' ')
				ctryadd = (int(dxccnr),qso)
				zoneadd = (int(zonacq),qso)

				# se il country non è ancora nella matrice
				if int(dxccnr) not in countries.keys():
					#	lo aggiungiamo alla lista dei qualificanti
					countries.update({ctryadd})
					print(",manca country")
	
				# altrimenti vediamo se ci serve per la zona
				elif int(zonacq) not in zones.keys():
					#	lo aggiungiamo alla lista dei qualificanti
					zones.update({zoneadd})
					print(",manca zona")
				
				else:
					print(',celo')

# riepilogo a schermo
print("\n\n\n========== RIEPILOGO ==========")
print("\n========== Zone collegate ==========")

contazone = list(zones.keys())
print(contazone)

print("\n========== Zone non collegate ==========")

for i in range (1,41):
	if i not in contazone:
		print(i, end=" ")
	i += 1
print('\n')

print("\nZone			", end="")
punt_zone = len(zones.keys())
print(punt_zone)

# siccome ARI Roma l'abbiamo considerata come un country, bisogna togliere 1 dal conteggio, se collegata
print("Countries		", end="")

punt_ctry = len(countries.keys())
punt_iq0rm = 0

if 999 in list(countries.keys()):
	punt_ctry = punt_ctry -1
	punt_iq0rm = 3
	
print(punt_ctry)

print("IQ0RM			", end="")
print(punt_iq0rm)
print("-------------------------------")
print("Totale			", end="")
print(punt_ctry + punt_zone + punt_iq0rm)

# FILE CSV PER POPOLARE EXCEL MARATONA
#print("\n\n\n========== RIEPILOGO ==========", file=rendiconto)

print("Country,Giorno,Mese,GMT,Frequency,Mode,Callsign", file=rendiconto)

# countries

for entity in maratona_ctry:
	print(dxcc[entity],end=',', file=rendiconto)
	if entity in countries.keys():
		subqso = countries[entity].replace("'","").split(',')
		print(countries[entity][8:10],end=',', file=rendiconto)
		print(countries[entity][6:8],end=',', file=rendiconto)
		print(countries[entity][13:15],end='.', file=rendiconto)
		print(countries[entity][15:17],end=',', file=rendiconto)
		print(bandemhz[subqso[2]],end=',', file=rendiconto)
		print(subqso[3],end=',', file=rendiconto)
		print(subqso[4], file=rendiconto)
	else:
		print(',,,,,', file=rendiconto)

# zone
for i in range (1,41):
	print(i, end=",", file=rendiconto)
	if i in contazone:
		subqso = zones[i].replace("'","").split(',')
		print(zones[i][8:10],end=',', file=rendiconto)
		print(zones[i][6:8],end=',', file=rendiconto)
		print(zones[i][13:15],end='.', file=rendiconto)
		print(zones[i][15:17],end=',', file=rendiconto)
		print(bandemhz[subqso[2]],end=',', file=rendiconto)
		print(subqso[3],end=',', file=rendiconto)
		print(subqso[4], file=rendiconto)
	else:
		print(',,,,,', file=rendiconto)

	i += 1
print('\n')



rendiconto.close()
#os.remove(logfile)
