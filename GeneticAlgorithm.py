import random
from array import *
from typing import List

# Creates a list containing 36 lists, each of 3 items, all set to 0
p = 38
r, c = 36, 4  # r:row, c:column
size = 5;
Matrix = [[0 for x in range(r)] for y in range(c)] 
List = [[0 for x in range(r)] for y in range(c)]
Chromosome = []
Population = [[ Chromosome ]] * size
choiceMatrix: []

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




print(fitness(generate_Chromosome(36), convert_to_list(read_selections())))
#Chromosome = generate_Chromosome(36)
#print("Final Choromose", Chromosome)

Population = generate_population(size)




