#  به نام خدا
# Akbar Ghaedi: @1403-08-20..@1403-08-25.v1.2
# SA: Simulated Annealing Homework
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

# SHOW_HELP = True        # show some comments to report program working
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

# solution = [ - - - - - ] 5 bits; Representation for 5 number of IDs: 5..1: 0 to 32 integer
#   if bit value = 0 then that location was not participated
#   if bit value = 1 then that location was participated
#   sample:
#     location: [ 5 4 3 2 1 ]
#     solution = 10: so binary = [ 0 1 0 1 0 ] => [ - 4 - 2 - ]
#     fitness = 25 + 15 = 40
#     weight limitation = 4 + 1 = 5

def SimulatedAnnealing():   # The main function to run Simulated Annealing algorithm
  
  # initialize
  t = 0   # loop iteration
  help(f"----- initialization -----")
  while(True):      # may be initialization solution was not satisfied problem limitation, so we use loop to find first satisfied solution
    t += 1
    curSolution = CreateInitializeSolution()
    help(f"curSolution = {curSolution}, b:[{Bin(curSolution)}]")
    solutionWeightLimitation = CalculateWeightLimitation(curSolution)
    if solutionWeightLimitation <= Max_Weight: # check initialize solution weight limitation to break loop
      break
    else:
      help(f"Reject Solution: limitation was not satisfied. iteration: {t}, solutionWeightLimitation = {solutionWeightLimitation}")
      
  bestSolution = curSolution
  bestFitness = CalculateFitness(curSolution)

  tFindBestSolution = 0
  t = 0   # loop iteration

  # loop to find best solution
  help(f"----- loop to find best solution -----")
  while(t < Max_iteration):
    t += 1
    help(f"----- iteration: {t} -----")

    newSolution = CreateSolution(curSolution)     # get nearest neighbor
    help(f"newSolution = {newSolution}, b:[{Bin(newSolution)}]")
    weightLimitation = CalculateWeightLimitation(newSolution)     # calculation of weight limitation
    if weightLimitation > Max_Weight: 
      help(f"Reject Solution: limitation was not satisfied. weightLimitation = {weightLimitation}")
      continue     # reject solution; check problem limitation

    newFitness, curFitness = CalculateFitness(newSolution), CalculateFitness(curSolution)   # calculation of fitness of current & new solutions
    help(f"newFitness = {newFitness}, weightLimitation = {weightLimitation}")

    # dE = newFitness - curFitness    # default
    dE = -(newFitness - curFitness)   # change to Maximization problem
    help(f"dE = {dE}")
    if dE <= 0:
      curSolution = newSolution
      # if newFitness < bestFitness:  # default
      if newFitness > bestFitness:    # change to Maximization problem
        bestSolution = newSolution                    # keep best solution
        bestFitness = newFitness                      # keep fitness of best solution as betFitness
        solutionWeightLimitation = weightLimitation   # keep weight Limitation of best solution
        tFindBestSolution = t     # the iteration that was found the best solution
    else:
      T = GetTemperature(t)
      help(f"Temprature = {T}")
      if random.random() < math.exp(-dE / T):     # Accept some bad solution randomly
        curSolution = newSolution
        help(f"Accept bad solution: {curSolution}")

    help("best: solution, fitness, iteration, tFindBestSolution: ", bestSolution, bestFitness, t, tFindBestSolution)

  return bestSolution, bestFitness, solutionWeightLimitation, t, tFindBestSolution

def CreateInitializeSolution():   # generate first randomly solution
  # solution as 5 bits number [? ? ? ? ?] and ? = 0/1
  return random.randrange(0, 31)     # initialize solution for 5 bits, randomly

def CreateSolution(solution):     # Create a neighbor solution with a small change: by change one bit
  pos = random.randint(0, 4)      # select 1 bit position, to change value
  mask = 1 << pos                 # creation of bit mask
  newSolution = solution ^ mask   # change 1 bit via xor operator to patricipate or not

  help(f"nearest niegborhood: {solution:2d} = b:[ {Bin(solution)} ] ---> {newSolution:2d} = b:[ {Bin(newSolution)} ]")
  return newSolution

def CalculateFitness(solution):     # fitness calculation of solution
  fitness = 0
  for i in range(0, 5):
    posValue = int(math.pow(2, i))
    if (posValue & solution) == posValue:
      item = items[i]
      fitness += item[2]
  return fitness

def CalculateWeightLimitation(solution):    # calculation of weight limitation
  weightLimitation = 0
  for i in range(0, 5):
    posValue = int(math.pow(2, i))
    if (posValue & solution) == posValue:
      item = items[i]
      weightLimitation += item[1]
  return weightLimitation

def GetTemperature(t):    # Generate temperature value based on iteration
  if t < 3:
    return Init_Temperature
  return Init_Temperature / math.log2(t)    # logarithmic timeing

def gpm(solution):    # Genotype-to-Phenotype Mapping: show bits as real world solution
  for i in range(0, 5):
    posValue = int(math.pow(2, i))
    if (posValue & solution) == posValue:
      print(f"item[{i}] = {items[i]}")

def help(*args, **kwargs):    # show comments if SHOW_HELP switch is True
  if SHOW_HELP:
      print(*args, **kwargs)

def Bin(val):     # binary representation of integer numbers: 'int' ---> 'bin' 5 bits
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
