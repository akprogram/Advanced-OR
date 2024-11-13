#  به نام خدا
# Akbar Ghaedi: @1403-08-20..@1403-08-23.v1.0.0
# SA: simulated Annealing Homework
# prof: Dr. Salimifard
# Metahuristic and AI
# pgu.ac.ir

'''
sample solution:
  --------------
  iteration = 100
  first iteration of Find Best Solution = 12
  best Fitness = 70
  Weight Limitation = 10
  best Solution = b:[1 1 0 1 1]
  solution:
  item[0] = (1, 3, 20)
  item[1] = (2, 4, 25)
  item[3] = (4, 1, 15)
  item[4] = (5, 2, 10)
'''
import math
import random

# SHOW_HELP = True
SHOW_HELP = False

# item: (id, weight, amount): "id" can be removed; but, we keep it for presentation
items = [(1, 3, 20),
         (2, 4, 25),
         (3, 5, 30),
         (4, 1, 15),
         (5, 2, 10)]

Max_Weight = 10
Init_Temperature = 250
Max_iteration = 100

# solution = [- - - - -] 5 bits; Representation for 5 number of IDs: 5..1: 0 to 32 integer
#   if bit value = 0 then that location was not participated
#   if bit value = 1 then that location was participated
#   sample:
#     location: [5 4 3 2 1]
#     solution = 10: so binary = [0 1 0 1 0] => [- 4 - 2 -]
#     fitness = 25 + 15 = 40
#     weight limitation = 4 + 1 = 5

def SimulatedAnnealing():
  
  # initialize
  curSolution = CreateInitializeSolution()
  bestSolution = curSolution
  bestFitness = CalculateFitness(curSolution)
  solutionWeightLimitation = CheckWeightLimitation(curSolution)
  tFindBestSolution = 0
  t = 0

  # loop to find best solution
  while(t < Max_iteration):
    t += 1
    help(f"----- iteration: {t} -----")

    newSolution = CreateSolution(curSolution)
    help(f"newSolution = {newSolution}, b:[{Bin(newSolution)}]")
    weightLimitation = CheckWeightLimitation(newSolution)
    if weightLimitation > Max_Weight: continue     # reject solution; check problem limitation

    newFitness, curFitness = CalculateFitness(newSolution), CalculateFitness(curSolution)
    help(f"newFitness = {newFitness}, weightLimitation = {weightLimitation}")

    # dE = newFitness - curFitness    # default
    dE = -(newFitness - curFitness)   # change to Maximization problem
    help(f"dE = {dE}")
    if dE <= 0:
      curSolution = newSolution
      # if newFitness < bestFitness:  # default
      if newFitness > bestFitness:    # change to Maximization problem
        bestSolution = newSolution
        bestFitness = newFitness
        solutionWeightLimitation = weightLimitation
        tFindBestSolution = t
    else:
      T = GetTemperature(t)
      help(f"Temprature = {T}")
      if random.random() < math.exp(-dE / T):
        curSolution = newSolution
        help(f"Accept bad solution: {curSolution}")

    help("best: solution, fitness, iterationو tFindBestSolution: ", bestSolution, bestFitness, t, tFindBestSolution)

  return bestSolution, bestFitness, solutionWeightLimitation, t, tFindBestSolution

def CreateInitializeSolution():
  # solution as 5 bits number [? ? ? ? ?] and ? = 0/1
  return random.randrange(0, 31)     # initialize solution for 5 bits

def CreateSolution(solution):
  pos = random.randint(0, 4)    # Creation of nearest neighbor: by change one bit
  mask = 1 << pos
  newSolution = solution ^ mask
  return newSolution

def CalculateFitness(solution):
  fitness = 0
  for i in range(0, 5):
    posValue = int(math.pow(2, i))
    if (posValue & solution) == posValue:
      item = items[i]
      fitness += item[2]
  return fitness

def CheckWeightLimitation(solution):
  weightLimitation = 0
  for i in range(0, 5):
    posValue = int(math.pow(2, i))
    if (posValue & solution) == posValue:
      item = items[i]
      weightLimitation += item[1]
  return weightLimitation

def GetTemperature(t):
  if t < 3:
    return Init_Temperature
  return Init_Temperature / math.log2(t)

def gpm(solution):    # Genotype-to-Phenotype Mapping
  for i in range(0, 5):
    posValue = int(math.pow(2, i))
    if (posValue & solution) == posValue:
      print(f"item[{i}] = {items[i]}")

def help(*args, **kwargs):
  if SHOW_HELP:
      print(*args, **kwargs)

def Bin(val):
  s = f"{val:05b}"
  return ' '.join(s)

#------------ Run Program ------------
bestSolution, bestFitness, solutionWeightLimitation, iteration, tFindBestSolution = SimulatedAnnealing()
print("--------------")
print(f"iteration = {iteration}")
print(f"first iteration of Find Best Solution = {tFindBestSolution}")
print(f"best Fitness = {bestFitness}")
print(f"Weight Limitation = {solutionWeightLimitation}")
print(f"best Solution = b:[{Bin(bestSolution)}]")
print("solution:")
gpm(bestSolution)
