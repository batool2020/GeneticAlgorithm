import random
from array import *
from typing import List, Optional, Callable, Tuple

# Creates a list containing 36 lists, each of 3 items, all set to 0
p = 38
r, c = 36, 4  # r:row, c:column
size = 100;
Matrix = [[0 for x in range(r)] for y in range(c)]
List = [[0 for x in range(r)] for y in range(c)]
Chromosome = []
Population = [Chromosome]
ChoiceMatrix: []
fitness = 0;


def read_selections() -> Matrix:
    with open("students_selections.txt") as textFile:
        Matrix = [line.split("-") for line in textFile]

    Matrix = [[s.rstrip(' \n ') for s in nested] for nested in Matrix]

    #print(Matrix)
    return Matrix


def convert_to_list(Matrix) -> List:
    Matrix = read_selections()
    List = Matrix.copy()
    for i in range(r):
        del List[i][0]

    for i in range(r):
        for j in range(c - 1):
            List[i][j] = int(List[i][j])

    ChoiceMatrix = List
    return List


def generate_Chromosome(length: int) -> Chromosome:  # need to pass list as argument
    projects = [x for x in range(p)]
    random.shuffle(projects)
    ch1 = projects[:36]
    print("generated new chromosome:  \n", ch1)
    return ch1


def generate_population(size: int) -> Population:
    return [generate_Chromosome(r) for i in range(size)]


def fitness(chromosome: Chromosome, choiceMatrix: list) -> int:
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
    numOfCrossedallels = 3
    length = len(ch1)

    pointOfCrossover = random.randint(0, length - 1)

    for i in range(numOfCrossedallels):
        pointer = (pointOfCrossover + i) % length
        a1 = ch1[pointer]  # allele that will cross from ch1 to ch2
        a2 = ch2[pointer]  # allele that will cross from ch2 to ch1

        for j in range(length):
            if a1 == ch2[j]:
                ch2[j] = ch2[pointer]   # make sure there are no duplicates
                break
        ch2[pointer] = a1   # carry out cross over

        for j in range(length):
            if a2 == ch1[j]:
                ch1[j] = ch1[pointer]   # make sure there are no duplicates
                break
        ch1[pointer] = a2   # carry out cross over

    return ch1, ch2


def mutation(ch1: Chromosome, num: int = 1, probability: float = 0.5) -> Chromosome:
    for i in range(num):
        m = random.randrange(p) + 1        # mutation allele
        index = random.randrange(r)     # new position for the mutation allele

        if random.random() > probability:
            for j in range(r):
                if m == ch1[j]:
                    ch1[j] = ch1[index]  # make sure there are no duplicates
                    break
            ch1[index] = m  # carry out mutation

    return ch1


def selection_pair(population: Population, choiceMatrix: List) -> [Chromosome, Chromosome]: # we can pass fitness function instead of list
    # fitnessList = []
    # temp = []
    # maxnum1 = 0;
    # maxnum2 = 0;
    # for i in range(size):
    #     print(population[i], " Fitness is : ", fitness(population[i], list))
    #     fitnessList.append(fitness(population[i], list))
    #
    # temp = fitnessList.copy()
    # maxnum1 = max(temp)
    # temp.remove(maxnum1)
    # maxnum2 = max(temp)
    # print("Max 1  is", population[fitnessList.index(maxnum1)], "\n", "Max 2 is ",
    #       population[fitnessList.index(maxnum2)])
    #
    # return population[fitnessList.index(maxnum1)], population[fitnessList.index(maxnum2)]

    return random.choices(
        population=population,
        weights=[fitness(gene, choiceMatrix) for gene in population],
        k=2
    )



def run_evolution(choiceMatrix: List, fitness_limit: int, generation_limit: int) -> [Population, int]:

    population = generate_population(size)

    #for i in range(generation_limit):
        # compare fitnesses and return the top 2 solutions \ if their fitenss is the best of all then break - need to figure it out - does sorted work?
        # population = sorted(population,key=fitness(population[i],list), reverse= True)

    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness(genome, choiceMatrix), reverse=True)

        # for x in range(size):
        #     if fitness(population[x], choiceMatrix) >= fitness_limit:
        #         print("should return the best 2 chromosomes")

        maxFitness = fitness(population[0], choiceMatrix)
        #print(f"max = {maxFitness}")
        if maxFitness >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_pair(population, choiceMatrix)
            ch1, ch2 = crossover(parents[0].copy(), parents[1].copy())
            ch1 = mutation(ch1)
            ch2 = mutation(ch2)
            next_generation += [ch1, ch2]

        population = next_generation


    population = sorted(population, key=lambda genome: fitness(genome, choiceMatrix), reverse=True)

    return population, i


# selection_pair(generate_population(size), convert_to_list(Matrix))
population, i = run_evolution(convert_to_list(Matrix), 100, 10000)
maxFitness = fitness(population[0], convert_to_list(Matrix))
print(f"max = {maxFitness}")
print(population[0])












