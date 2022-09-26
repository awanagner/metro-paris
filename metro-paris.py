#-*- coding: utf-8 -*-
#	INFORMAÇÕES DO PROBLEMA
# VELOCIDADE MEDIA DE UM TREM = 30km/h
# TEMPO MÉDIO PARA TROCAR DE ESTAÇÃO = 4 mins

## PROBLEMA DO METRO DE PARIS ##
## considerando a Vm do metrô ==> 30km/h ##
## tempo médio para troca de estação ==> 4 min ##

## NOME DAS ESTAÇÕES ##

E = ["La Défense", "Charles de Gaulle Étoile", "Concorde", "Palais Royal Musée du Louvre", "Reuilly-Diderot", 
	"Daumesnil", "Gare de Lyon", "Barbès Rochechouart", "Place de Clichy", "Victor Hugo", "Gabriel Péri",
	"Porte de Clignancourt", "Denfert Rochereau", "Porte d'Orléans"]

# lista de borders usadas para a busca #
border = []

# estaçoes visitadas ou nao #
visit = [0]*14
reply = []

stationChange = 0
km = 0

#	INITIAL STATION
def depart():
	print("DEPARTURE STATION:")
	for i in range(0, len(E)):
		print("{} - {}".format(i+1, E[i]))
	p = int(input())-1
	if(p < 0 or p > 14):
		depart()
	return p

#	FINAL STATION
def arrival():
	print("DESTINATION STATION:")
	for i in range(0, len(E)):
		print("{} - {}".format(i+1, E[i]))
	c = int(input())-1
	return c


### DISTANCES ##
H = [
#	 E1  E2  E3  E4  E5  E6  E7  E8  E9 E10  E11 E12 E13 E14
	(0,  11, 20, 27, 40, 43, 39, 28, 18, 10, 18, 30, 30, 32),# E1
	(11,  0,  9, 16, 29, 32, 28, 19, 11,  4, 17, 23, 21, 24),# E2
	(20,  9,  0,  7, 20, 22, 19, 15, 10, 11, 21, 21, 13, 18),# E3
	(27, 16,  7,  0, 13, 16, 12, 13, 13, 18, 26, 21, 11, 17),# E4
	(40, 29, 20, 13,  0,  3,  2, 21, 25, 31, 38, 27, 16, 20),# E5
	(43, 32, 22, 16,  3,  0,  4, 23, 28, 33, 41, 30, 17, 20),# E6
	(39, 28, 19, 12,  2,  4,  0, 22, 25, 29, 38, 28, 13, 17),# E7
	(28, 19, 15, 13, 21, 23, 22,  0,  9, 22, 18,  7, 25, 30),# E8
	(18, 11, 10, 13, 25, 28, 25,  9,  0, 13, 12, 12, 23, 28),# E9
	(10,  4, 11, 18, 31, 33, 29, 22, 13,  0, 20, 27, 20, 23),# E10
	(18, 17, 21, 26, 38, 41, 38, 18, 12, 20,  0, 15, 35, 39),# E11
	(30, 23, 21, 21, 27, 30, 28,  7, 12, 27, 15,  0, 31, 37),# E12
	(30, 21, 13, 11, 16, 17, 13, 25, 23, 20, 35, 31,  0,  5),# E13
	(32, 24, 18, 17, 20, 20, 17, 30, 28, 23, 39, 37,  5,  0) # E14
	]

# BLUE    1
# YELLOW  2
# GREEN   3
# RED     4

## LINK TABLE BETWEEN ##
L = [
#	E0  E1 E2 E3 E4 E5 E6 E7 E8 E9 E10 E11 E12 E13
	(0, 1,  0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0,  0),# E0
	(1, 0,  1, 0, 0, 0, 0, 0, 2,  2,  0,  0,  0,  0),# E1
	(0, 1,  0, 1, 0, 0, 0, 0, 4,  0,  0,  0,  4,  0),# E2
	(0, 0,  1, 0, 1, 0, 0, 3, 0,  0,  0,  0,  3,  0),# E3
	(0, 0,  0, 1, 0, 1, 2, 2, 0,  0,  0,  0,  0,  0),# E4
	(0, 0,  0, 0, 1, 0, 0, 0, 0,  0,  0,  0,  0,  0),# E5
	(0, 0,  0, 0, 2, 0, 0, 0, 0,  0,  0,  0,  0,  0),# E6
	(0, 0,  0, 3, 2, 0, 0, 0, 2,  0,  0,  3,  0,  0),# E7
	(0, 2,  4, 0, 0, 0, 0, 2, 0,  0,  4,  0,  0,  0),# E8
	(0, 2,  0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0,  0),# E9
	(0, 0,  0, 0, 0, 0, 0, 0, 4,  0,  0,  0,  0,  0),# E10
	(0, 0,  0, 0, 0, 0, 0, 3, 0,  0,  0,  0,  0,  0),# E11
	(0, 0,  4, 3, 0, 0, 0, 0, 0,  0,  0,  0,  0,  3),# E12
	(0, 0,  0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  3,  0) # E13
	]

def timeConvert(x):
	mins = x*2
	return mins

def colorLink(cor):
	if cor == 1:
		return "Azul"
	elif cor == 2:
		return "Amarela"
	elif cor == 3:
		return "Verde"
	elif cor == 4:
		return "Vermelha"

def print_border():
	print("BORDER:")
	for i in range(0, len(border)):
		if(visit[border[i][2]] == 0):
			print(border[i])

def Path(a):
	while a[3][2] != -1:
		reply.append(a[3][2])
		a = a[3] 

def SuccOf(a):
	for i in range (0, len(E)):
		if(L[a[2]][i] != 0 and visit[a[2]] == 0):
			#	G DO PROXIMIO
			g = timeConvert(a[3][1] + H[a[2]][i])
			#	H DO PROXIMO 
			h = timeConvert(H[i][arrivalPoint])
			#	PAI DO PROX
			FatherS = a
			#	COR DA LINHA 
			Line = L[a[2]][i]
			if(a[4] != Line):
				h += 4	#	+4 MIN // troca
			#	ADD A FRONTEIRA
			s = [h+g, g, i, FatherS, Line]
			border.append(s)
	visit[a[2]] = 1

def A_Star():
	k = 0
	while k > -1:	
		for i in range(0, len(border)):
			if(visit[border[i][2]] == 0):
				break
		if(border[i][2] == arrivalPoint):
			visit[border[i][2]] = 1
			reply.append(border[i][2])
			Path(border[i])
			break
		SuccOf(border[i])
		border.sort(key=lambda border: border[0])
		print_border()
		k += 1

### MAIN ###

departPoint = depart()
arrivalPoint = arrival()

print("DEPARTURE STATION: {}".format(E[departPoint]))
print("ARRIVAL STATION: {}".format(E[arrivalPoint]))

V = [0, 0, -1, -1, -1]

# E = [f, g, indxStation, FatherS, corDaLine]
a = [timeConvert(0 + H[departPoint][arrivalPoint]), 0, departPoint, V, None]

border.append(a)

A_Star()

final = reply[::-1] 

print("\n\nBEST PATH: E{} -> E{}".format(departPoint+1, arrivalPoint+1))
for i in range (0, len(final)):
	if i == 0:
		print("DEPARTURE: [E{} : {}] - (Line: {}) ...\n".format(final[i]+1, E[final[i]], colorLink(L[final[i]][final[i+1]])))
		km += (H[final[i]][final[i+1]])
	elif i == len(final)-1:
		print("...ARRIVAL: [E{} : {}]\n".format(final[i]+1, E[final[i]]))
	else:
		km += H[final[i]][final[i+1]]
		if L[final[i-1]][final[i]] != L[final[i]][final[i+1]]:
			print("STATION CHANGE:")
			stationChange += 1
		print("...COMING FROM (Line: {}) - GOING THROUGH [E{} : {}] - GOING TO (Line: {}) ...\n".format(colorLink(L[final[i-1]][final[i]]), final[i]+1, E[final[i]], colorLink(L[final[i]][final[i+1]])))

print("TRAVELED: {} KM WITH {} STATION CHANGE".format(km, stationChange))
print("ESTIMATED TIME: {} MINUTES".format(timeConvert(km) + 4*stationChange))

