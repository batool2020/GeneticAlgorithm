import random
from array import *
from typing import List

# Creates a list containing 36 lists, each of 3 items, all set to 0
r, c = 36, 4  # r:row, c:column
size = 5;
Matrix = [[0 for x in range(r)] for y in range(c)] 
List = [[0 for x in range(r)] for y in range(c)]
Chromosome = []
Population = [[ Chromosome ]] * size

def read_selections() -> Matrix:
 
    with open("students_selections.txt") as textFile:
        Matrix = [line.split("-") for line in textFile]
        
    Matrix = [[s.rstrip(' \n ') for s in nested] for nested in Matrix]
        
    return Matrix



def convert_to_list(Matrix) -> List:
    
    Matrix = read_selections()
    List= Matrix.copy()
    for i in range(r):
        del List[i][0]


    for i in range(r):
        for j in range(c-2):
            List[i][j] = int(List[i][j])
    


    return List

def generate_Chromosome(length: int) -> Chromosome:  #need to pass list as argument
    x = 0;
    temp =[]
    Geneom = [0] * length
    # here we generate chromosomes randomمy and the genes values are chosen according to matrix values

    # Fill the chromosome with first column of list
    # Compare and zeros
    # Fill the zero indeces with 2nd column of the list 
    # iterate for 3 times -- number of columns 

    List = convert_to_list(Matrix)
    for y in range(c-1):
        for i in range(length): 
                # fill the zero indeces with next column numbers in list
            if Geneom[i] == 0:
                Geneom[i]=List[i][y]
         #Compare and zero filling      #   check for duplicates and replace them with zeros

        for i in range(length):
            for j in range(i):
                if Geneom[i]==Geneom[j] and Geneom[i] !=0:
                    Geneom[i]=0
        
        print("Chromosome after zeros round: ", y, "  ", Geneom)   # this one to check that num of zeros is decreasing everytime. 

        # convert the 2d list to 1d
    temp1 = [b for sub in List for b in sub]
    # print("TEMP1", temp1)

    # Get the remaining items in list and not used in chromosome from 1 to 38
    for item in range(1,38):
        if item not in Geneom or item not in temp1:
            temp.append(item)


    # Fill the remaining Groups with remaining projects
    for i in range (length):
        if Geneom[i] == 0:
            Geneom[i] = temp[x]
            x=x+1
    Geneom[i] = int(Geneom[i])

    print(" List temp items  " , temp)

    return Geneom
            




def generate_population(size: int) -> Population:
    return [generate_Chromosome(r) for i in range(size)]



#Chromosome = generate_Chromosome(36)
#print("Final Choromose", Chromosome)

Population = generate_population(size)




