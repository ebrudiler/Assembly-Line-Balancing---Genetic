# -*- coding: utf-8 -*-

from random import randint as rnd
from random import uniform 
from random import shuffle
import matplotlib.pyplot as plt
N = 100 #chromosome size
M = 1000 #population size
crossOverRate = 0.8
mutationRate = 0.2
maxIteration = 500

def createChromosome():
  return [rnd(0, 1) for _ in range(N)]

def initializePopulation():
  return [createChromosome() for _ in range(M)]

def onePointCrossOver(chromosome1, chromosome2):
  index = rnd(1, N-2)
  newChromosome1, newChromosome2 = chromosome1.copy(), chromosome2.copy()
  
  for i in range(index):
    newChromosome1[i], newChromosome2[i] = newChromosome2[i], newChromosome1[i]
  return newChromosome1, newChromosome2

def crossOver(chromosome1, chromosome2):
  return onePointCrossOver(chromosome1, chromosome2)

def crossOverSelection(population):
  selectionList = []
  shuffle(population)
  for i in range(0, len(population), 2):
    if len(population) == i + 1:
      break
    if uniform(0, 1) < crossOverRate:
      selectionList.append((population[i], population[i+1]))
  return selectionList

def onePointMutation(chromosome):
  index = rnd(0, N-1)
  newChromosome = chromosome.copy()
  if newChromosome[index] == 0:
    newChromosome[index] = 1
  return newChromosome  

def mutation(chromosome):
  return onePointMutation(chromosome)

def mutationSelection(population):
  return [chromosome for chromosome in population if uniform(0, 1) < mutationRate]
  selectionList = []
  for chromosome in population:
    if uniform(0, 1) < mutationRate:
      selectionList.append(chromosome)
  return selectionList

def fitnessScore(chromosome):
   return sum(chromosome)

def roulet(population):
  fitnessList = []
  probabilityList = []
  for i in range(len(population)):
    fitnessList.append(fitnessScore(population[i]))
  for i in range(len(fitnessList)):
    probabilityList.append(fitnessList[i] / max(fitnessList))
  return probabilityList

def newPopulation(population, crossOverPopulation, mutatedPopulation):
  newPopulation = []
  oldPopulation = population + crossOverPopulation + mutatedPopulation
  uniquePopulation = [] 
  for i in oldPopulation:
    if i not in uniquePopulation:
      uniquePopulation.append(i)
  index = uniform(0, 1)
  probabilityList = roulet(oldPopulation)
  for i in range(len(probabilityList)):
    if len(newPopulation) == M:
      break
    index = uniform(0, 1)
    if index < probabilityList[i]:
      newPopulation.append(oldPopulation[i])
  return newPopulation



population = initializePopulation()
#print('Population', population)

bestFitnessScore = 0
fitnessScoreList = []
for curIter in range(maxIteration):
  crossOverSelectionList = crossOverSelection(population)
  crossOverPopulation = []
  #print('Cross Over Selection', crossOverSelectionList)
  for i in range(0, len(crossOverSelectionList), 2):
    crossed = crossOver(crossOverSelectionList[i][0], crossOverSelectionList[i][1])
    crossOverPopulation.append(crossed[0])
    crossOverPopulation.append(crossed[1])
  #print('Cross Over Population', mutatedPopulation)

  mutationSelectionList = mutationSelection(population)
  mutatedPopulation = []
  #print('Mutation Selection', mutationSelectionList)
  for i in range(len(mutationSelectionList)):
    mutatedPopulation.append(mutation(mutationSelectionList[i]))
  #print('Mutated Population', mutatedPopulation)

  population = newPopulation(population, crossOverPopulation, mutatedPopulation)
  
  population.sort(key=fitnessScore, reverse=True)
  bestOfIteration = fitnessScore(population[0])
  fitnessScoreList.append(bestOfIteration)
  if bestOfIteration > bestFitnessScore:
    bestFitnessScore = bestOfIteration
    print(fitnessScore(population[0]), curIter)

plt.plot(range(maxIteration), fitnessScoreList)
plt.show()