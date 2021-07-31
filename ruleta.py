#Funcionamiento de la ruleta
#Paulina Vara Figueroa
import random

roulette = []
fitness = [1.3, 2.6, 5.2, 10.4, 20.8]

contadores=[0]*(len(fitness)) #Solo para verificar-----------------------

def buildRoulette (fitness):
    global roulette
    roulette = [0] * (len(fitness)+1)#
    index = 1
    for data in fitness:
        roulette[index] = data + roulette[index-1]
        index+=1

def spinRoulette ():
    global roulette
    global contadores #Para Verificar---------------------------
    chosen = random.uniform(0, max(roulette))
    for limit in roulette:
        position = roulette.index(limit)
        if (chosen < limit):
            break
    position-=1
    contadores[position]+=1 #Para verificar----------------------



#----------------------------------------------------------------------------Pruebaaa
buildRoulette(fitness)
i = 0
while (i<100000):
    i+=1
    spinRoulette()
i = 0
for dato in fitness:
    print(str(dato) + ' ' + str(contadores[i]) + 'veces')
    i+=1
#-----------------------------------------------------------------------------Pruebaaa