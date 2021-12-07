import random
from array import *
from typing import List, Optional, Callable, Tuple

# Creates a list containing 36 lists, each of 3 items, all set to 0
p = 38
r, c = 36, 4  # r:row, c:column
size = 5;
Matrix = [[0 for x in range(r)] for y in range(c)] 
List = [[0 for x in range(r)] for y in range(c)]
Chromosome = []
Population = [[ Chromosome ]] * size
choiceMatrix: []
fitness=0;

def read_selections() -> Matrix:
 
    with open("students_selections.txt") as textFile:
        Matrix = [line.split("-") for line in textFile]
        
    Matrix = [[s.rstrip(' \n ') for s in nested] for nested in Matrix]

    print(Matrix)
    return Matrix



def convert_to_list(Matrix) -> List:
    
    Matrix = read_selections()
    List= Matrix.copy()
    for i in range(r):
        del List[i][0]

    for i in range(r):
        for j in range(c-1):
            List[i][j] = int(List[i][j])

    choiceMatrix = List
    return List

def generate_Chromosome(length: int) -> Chromosome:  #need to pass list as argument
    projects = [x for x in range(p)]
    random.shuffle(projects)
    ch1 = projects[:36]
    print("Final CH1 \n", ch1)
    return ch1



def generate_population(size: int) -> Population:
    return [generate_Chromosome(r) for i in range(size)]


def fitness(chromosome: Chromosome, choiceMatrix: List) -> int:
    score: int = 0
    for i in range(r):
        if chromosome[i] == choiceMatrix[i][0]:
            score += 3
        elif chromosome[i] == choiceMatrix[i][1]:
            score += 2
        elif chromosome[i] == choiceMatrix[i][2]:
            score += 1

    return score

def crossover(ch1: Chromosome, ch2: Chromosome) -> [Chromosome, Chromosome]:
    length = len(ch1)
    if length < 2:
        return ch1, ch2

    p = random.randint(1, length - 1)
    return ch1[0:p] + ch2[p:], ch1[0:p] + ch2[p:]

def mutation(ch1: Chromosome, num: int = 1, probability: float = 0.5) -> Chromosome:
    for i in range(num):
        index1 = random.randrange(r)
        index2 = random.randrange(r)

        if random() > probability:
            temp = ch1[index1]
            ch1[index1] = ch1[index2]
            ch1[index2] = temp
    

    return ch1



def selection_pair(population: Population, list: List)   -> [Chromosome, Chromosome]:   # we can pass fitness function instead of list
    fitnessList = []
    temp = []
    maxnum1 =0;
    maxnum2 = 0;
    for i in range(size):
        print(population[i], " Fitness is : ", fitness(population[i],list))
        fitnessList.append(fitness(population[i],list))

    temp = fitnessList.copy()
    maxnum1 = max(temp)
    temp.remove(maxnum1)
    maxnum2 = max(temp)
    print ("Max 1  is", population[fitnessList.index(maxnum1)] , "\n" , "Max 2 is ", population[fitnessList.index(maxnum2)])
    
    
    return  population[fitnessList.index(maxnum1)] ,  population[fitnessList.index(maxnum2)]

 
def run_evolution(population: Population, list: List, fitness_limit: int,generation_limit :int) -> [Population, int]:
    
    fitness_limit = 0;


    population = generate_population(size)

    for i in range(generation_limit):
        # compare fitnesses and return the top 2 solutions \ if their fitenss is the best of all then break - need to figure it out - does sorted work? 
       # population = sorted(population,key=fitness(population[i],list), reverse= True)

        for x in range(size):
            if fitness(population[x], list) >= fitness_limit:
                print("should return the best 2 chromosomes")
       
        #if fitness(population[0],list) >= fitness_limit:
           # break

        #next_generation = population[0:2]

        for j in range(int(len(population) / 2 ) - 1):
            parents = selection_pair(generate_population(size),convert_to_list(Matrix))
            ch1, ch2 = crossover(parents[0], parents[1])
            ch1 = mutation(ch1)
            ch2 = mutation(ch2)
            next_generation += [ch1][ch2]

        population = next_generation
    population = sorted(population, fitness(population[i],list), true)

    return population, i




selection_pair(generate_population(size),convert_to_list(Matrix))
run_evolution(generate_population(size),convert_to_list(Matrix),15, 6)
