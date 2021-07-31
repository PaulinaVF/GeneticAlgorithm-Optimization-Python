import random #Utilizado al "girar" la ruleta y al generar población inicial
import math #Para utilizar logaritmo2 en el cálculo de bits por individuo
from math import pi
import matplotlib.pyplot as plt

roulette = []#Guarda lo límites de la ruleta para no tener que crearla cada vez que se utilice
fitness = []
popSize = 6#Tamaño de la población
bits = 0#Número de bits que conforman a cada individuo de la población
accuracy = 300#Exactitud que se busca en el resultado
population = []#Guarda a la población
replaced = 0.4 #Fraction of population to be replaced by crossover
aInterval = -1#Valor de inicio del intervalo
bInterval = 2#Valor final del intervalo
crossRate = 0.4
mutRate = 0.2

popSize = int(input('Tamaño de la población: '))
crossRate = float(input('Proporción para crossover: '))
mutRate = float(input('Proporción para mutación: '))

def buildRoulette (fitness):#Esta función únicamente crea la ruleta
    global roulette
    roulette = [0] * (len(fitness)+1)#Se crea de este tamaño porque va a ir almacenando la sumatoria que va generando
                            #el valor fitness de cada individuo de la población, se necesita uno extra porque el primer
                            #elemento de la lista es 0
    index = 1
    for data in fitness:#En esta función se va haciendo la sumatoria y guardando en la ruleta
        roulette[index] = data + roulette[index-1]
        index+=1

def spinRoulette ():#Esta función "gira" la ruleta que ya está creada
    global roulette
    chosen = random.uniform(0, max(roulette))#Se busca un valor entero entre 0 y el total de la sumatoria
    for limit in roulette:#En ruleta al irse guardando la sumatoria poco a poco esos datos se pueden considerar
                        #como límites, entonces se va a buscar bajo qué límite se encuentra el valor para conocer
                        #la posición del valor elegido
        position = roulette.index(limit)
        if (chosen < limit):#Sale del ciclo cuando supera el límite
            break
    position-=1#Como permitió que se superara el límite se le resta 1 a la posición
    return position

#Accuracy: Make sure that 2^n - 1 is bigger or equal to the accuracy required
def inicializePopulation(accuracy, popSize):
    global bits, population
    bits = int(math.ceil(math.log2(accuracy + 1))) #Con ceil se redondea hacia arriba el resultado del despeje de n
    for j in range(popSize):
        tempIndividual = []#Esta función guarda individuos temporales que se van a agregar a la población
        for i in range(bits):
            tempIndividual.append(random.randrange(0,2))#Se generan n bits aleatorios para el individuo temporal
        population.append(tempIndividual)#Se agrega el individuo a la población

def getFitness():# Función para calcular el valor "fitness" de cada individuo en la población
    global fitness
    decimalInd = []  # Se crea una lista para guardar el valor decimal dentro del intervalo de los
                            # individuos en la población

    def getDecimal():# Función para obtener el valor decimal de los individuos en la población
        global population, bits, aInterval, bInterval, popSize
        for individual in population:
            binaryStr = ""# Se limpia la cadena antes de empezar para que no se junten los individuos
            for bit in individual:# Dentro de este ciclo se convierte en cadena el contenido
                                        # de cada individuo (los bits 1 y 0)
                binaryStr=binaryStr+str(bit)
            binaryToDecimal = int(binaryStr,2)
            #Después se sigue la formula x = a + decimal(h) ((b - a)/(2^n - 1)) para encontrar el valor decimal
                            # dentro del intervalo de los individuos en la población:
            decimalInd.append(aInterval+binaryToDecimal*((bInterval-aInterval)/(2**bits-1)))
            #print (decimalInd)

    getDecimal()
    #Después de haber obtenido el valor decimal del individuo se calcula su valor de "fitness"
    for decimal in decimalInd:
        #fitness.append(math.sin(decimal)+2)
        fitness.append(decimal*math.sin(10*pi*decimal)+1.0)

def createNewPopulation(r, n, m):# r - crossover rate // n = population size // m = mutRate
    global fitness, population, bits # Será necesario manejar el fitness la población y el número de bits por individuo
    newPpltn = [] # Para guardar teporalmente a la nueva población antes de guardarla en "population[]"
    buildRoulette(fitness) # Se construye la ruleta solo una vez para esta población

    n_crossover = math.ceil(r*n/2)
    n_select = n - n_crossover*2

    def select (): # Selecciona a la cantidad de elementos que pasarán directamente (sin hacer crossover)
                    # y los guarda en la lista de la nueva población
        selectMembers = n_select
        for i in range(selectMembers):
            member = spinRoulette()
            newPpltn.append(population[member])
        #print('direct new: ')
        #print(newPpltn)
    def crossover (): # Selecciona a los elementos que van a pasar a la nueva población utilizando crossover, hace
                        # el crossover y los guarda en la lista de la nueva población
        #selectMembers = int(r*n/2)
        selectMembers = n_crossover
        for i in range(selectMembers):
            member1 = population[spinRoulette()]
            member2 = population[spinRoulette()]
            cutPoint = random.randrange(1, bits)
            newMember1 = [0] * bits
            newMember2 = [0] * bits
            i = 0
            while (i < cutPoint): # Para pasar los primeros bits del individuo original
                newMember1[i] = member1[i]
                newMember2[i] = member2[i]
                i+=1
            while (i < bits): # Para pasar la segunda parte haciendo el crossover con el otro individuo
                newMember1[i] = member2[i]
                newMember2[i] = member1[i]
                i += 1
            #print('Crossed Members:')
            #print(str(member1)+ ' and '+str(member2))
            #print('make: ' + str(newMember1) + ' and '+str(newMember2))
            newPpltn.append(newMember1) # Guarda el nuevo individuo generado
            newPpltn.append(newMember2) # Guarda el nuevo individuo generado
    def mutation ():
        mutIndividuals = math.ceil(n * m)
        for i in range(mutIndividuals):
            mutMember = random.randrange(0,n) # Posición del individuo que recibirá la mutación
            mutBit = random.randrange(0,bits) # Posición del bit del individuo a cambiar

            #Se utilizan condicionales para cambiar el bit seleccionado del individuo de 0 a 1 ó de 1 a 0
            if (newPpltn[mutMember][mutBit] == 0):
                newPpltn[mutMember][mutBit] = 1
            else:
                newPpltn[mutMember][mutBit] = 0
    select()
    #print('select: ' + str(newPpltn))
    crossover()
    #print('crossover: ' + str(newPpltn))
    mutation()
    population = []
    population = newPpltn #Se guarda la población nueva en la lista "population []"



#To check if it works:
iterat = 1000
promFitness = []
indIteracion = []

inicializePopulation(accuracy,popSize)
#print (population)
#print(fitness)
i = 1
while (i<=iterat):
 #   print(population)
    fitness = []
    getFitness()
    createNewPopulation(crossRate, popSize, mutRate)
 #   print(fitness)
    tempPromFit = sum(fitness) / popSize
    #print(tempPromFit)
    #print(i)
    promFitness.append(tempPromFit)
    indIteracion.append(i)

 #   print (sum(fitness))
    i+=1
    max_ind = fitness.index(max(fitness))
    #print(fitness[max_ind])

#max_ind = fitness.index(max(fitness))
#print(fitness[max_ind])
#print(population[fitness.index(max(fitness))])
print('Valor máximo: ' + str(max(fitness)) + ' | En posición: ' + str(fitness.index(max(fitness))))
binaryStr = ""  # Se limpia la cadena antes de empezar para que no se junten los individuos
for bit in population[fitness.index(max(fitness))]:
    binaryStr = binaryStr + str(bit)
binToDecimal = int(binaryStr, 2)
enRango = aInterval + (binToDecimal * ((bInterval - aInterval) / ((2 ** bits) - 1)))
print('x = '+str(enRango))
plt.plot(indIteracion, promFitness, "g")
plt.grid()

#plt.title('Representacion de dos funciones')
plt.xlabel('Iteración')
plt.ylabel('Promedio Fitness')

plt.show()