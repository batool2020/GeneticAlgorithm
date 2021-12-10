import random
from array import *
from typing import List, Optional, Callable, Tuple
import wx

data = []
r=0
p=0
desiredFitness=0
maxGen=0
filePath = ""

# Creates a list containing 36 lists, each of 3 items, all set to 0
c=4
size = 100
Matrix = [[0 for x in range(r)] for y in range(c)]
List = [[0 for x in range(r)] for y in range(c)]
Chromosome = []
Population = [Chromosome]
ChoiceMatrix: []



class MyApp(wx.App):
    def __init__(self):
        super().__init__(clearSigInt=True)

        # init frame
        self.InitFrame()

    def InitFrame(self):
        frame = MyFrame()
        frame.Show()


class MyFrame(wx.Frame):
    def __init__(self, title="Projects Distribution - Genetic Algorithm", size=(100, 100)):
        super().__init__(None, title=title, size=size)
        # initialize the frame's contents
        self.OnInit()

    def OnInit(self):
        self.panel = MyForm(self)
        self.Fit()


class MyForm(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent=parent)

        # Add a panel so it looks correct on all platforms

        bmp = wx.ArtProvider.GetBitmap(id=wx.ART_INFORMATION,
                                       client=wx.ART_OTHER, size=(16, 16))
        title = wx.StaticText(self, wx.ID_ANY, 'Hello ! Projects Distribution - Genetic Algorithm')

        labelFileName = wx.StaticText(self, wx.ID_ANY, 'You Can Upload a file!')
       # self.FileName = wx.TextCtrl(self, wx.ID_ANY, value=' ')

        labelProjectsNum = wx.StaticText(self, wx.ID_ANY, 'Projects Number')
        self.ProjectsNum = wx.SpinCtrl(self, wx.ID_ANY, value=' ')

        labelGroupsNum = wx.StaticText(self, wx.ID_ANY, 'Number of Gropus ')
        self.GroupsNum = wx.SpinCtrl(self, wx.ID_ANY, value=' ')

        labelChoicesNum = wx.StaticText(self, wx.ID_ANY, 'Number of choices for each Group ')
        self.ChoicesNum = wx.SpinCtrl(self, wx.ID_ANY, value=' ')

        labelMaxFitness = wx.StaticText(self, wx.ID_ANY, 'Maximum Fitness')
        self.MaxFitness = wx.SpinCtrl(self, wx.ID_ANY, value="0", min=0, max=100)

        labelMaxGeneration = wx.StaticText(self, wx.ID_ANY, 'Maximum Generation')
        self.MaxGeneration = wx.SpinCtrl(self, wx.ID_ANY, value="0", min=0, max=100)

        self.okBtn = wx.Button(self, wx.ID_ANY, 'OK')
        self.cancelBtn = wx.Button(self, wx.ID_ANY, 'Cancel')
        self.OpenFileBtn = wx.Button(self, wx.ID_ANY, 'Open File')

        self.okBtn.Bind(wx.EVT_BUTTON, self.Okfunc)
        self.cancelBtn.Bind(wx.EVT_BUTTON, self.Cancelfunc)
        self.OpenFileBtn.Bind(wx.EVT_BUTTON, self.OpenFilefunc)
        # self.Bind(wx.EVT_BUTTON, self.onOK, okBtn)
        # self.Bind(wx.EVT_BUTTON, self.onCancel, cancelBtn)
        # self.Bind(wx.EVT_BUTTON, self.onCancel, OpenFile)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputOneSizer = wx.BoxSizer(wx.HORIZONTAL)
        # inputTwoSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputThreeSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputFourSizer = wx.BoxSizer(wx.HORIZONTAL)
        submitBtnSizer = wx.BoxSizer(wx.HORIZONTAL)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        ProjectsNum = wx.BoxSizer(wx.HORIZONTAL)
        GroupsNum = wx.BoxSizer(wx.HORIZONTAL)
        ChoicesNum = wx.BoxSizer(wx.HORIZONTAL)
        MaxFitness = wx.BoxSizer(wx.HORIZONTAL)
        MaxGeneration = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(title, 0, wx.ALL, 5)

        inputOneSizer.Add(labelProjectsNum, 0, wx.ALL, 5)

        inputOneSizer.Add(self.ProjectsNum, 1, wx.ALL | wx.EXPAND, 5)

        inputOneSizer.Add(labelGroupsNum, 0, wx.ALL, 5)
        inputOneSizer.Add(self.GroupsNum, 1, wx.ALL | wx.EXPAND, 5)

        inputThreeSizer.Add(labelChoicesNum, 0, wx.ALL, 5)
        inputThreeSizer.Add(self.ChoicesNum, 1, wx.ALL | wx.EXPAND, 5)

        inputThreeSizer.Add(labelMaxFitness, 0, wx.ALL, 5)
        inputThreeSizer.Add(self.MaxFitness, 1, wx.ALL | wx.EXPAND, 5)

        inputThreeSizer.Add(labelMaxGeneration, 0, wx.ALL, 5)
        inputThreeSizer.Add(self.MaxGeneration, 1, wx.ALL | wx.EXPAND, 5)

        inputFourSizer.Add(labelFileName, 0, wx.ALL, 5)
        inputFourSizer.Add(self.OpenFileBtn, 1, wx.ALL | wx.EXPAND, 5)

        submitBtnSizer.Add(self.okBtn, 0, wx.ALL, 5)
        submitBtnSizer.Add(self.cancelBtn, 0, wx.ALL, 5)

        mainSizer.Add(titleSizer, 0, wx.CENTER)
        mainSizer.Add(wx.StaticLine(self, ), 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(inputOneSizer, 0, wx.ALL | wx.EXPAND, 5)
        # mainSizer.Add(inputTwoSizer, 0, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(inputThreeSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(inputFourSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(wx.StaticLine(self), 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(submitBtnSizer, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()




    def OpenFilefunc(self, event):
        # Create open file dialog
        global filePath
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "Text files (*.txt)|*.txt",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        filePath = openFileDialog.GetPath()
        print(openFileDialog.GetPath())
        openFileDialog.Destroy()

    def Cancelfunc(self, event):
        # self.GetParent() will get the frame which
        # has the .Close() method to close the program
        self.GetParent().Close()

    def Okfunc(self, event):
        '''
        this here will procure data from all buttons
        '''
        global r
        global p,maxGen,desiredFitness
        if self.GroupsNum.GetValue() > 0:
            r = self.GroupsNum.GetValue()
        if self.ProjectsNum.GetValue() >= r:
            p = self.ProjectsNum.GetValue()
        if self.MaxFitness.GetValue() > 0 and self.MaxFitness.GetValue() < 4*p:
            desiredFitness = self.MaxFitness.GetValue()
        if self.MaxGeneration.GetValue() > 0:
            maxGen = self.MaxGeneration.GetValue()

        #data.append(self.ChoicesNum.GetValue())


        print(f"p: {p}, r: {r}, fitness:{desiredFitness}, maxgen:{maxGen}")

    def onOK(self, event):
        # Do something
        print('onOK handler')
        data = self.getData()
        self.GetParent().Close()


# Run the program
if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()




def read_selections() -> Matrix:
    with open(filePath) as textFile: #"students_selections.txt"
        Matrix = [line.split("-") for line in textFile]

    Matrix = [[s.rstrip(' \n ') for s in nested] for nested in Matrix]

    # print(Matrix)
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
            score += 4
        elif chromosome[i] == choiceMatrix[i][1]:
            score += 3
        elif chromosome[i] == choiceMatrix[i][2]:
            score += 2

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
                ch2[j] = ch2[pointer]  # make sure there are no duplicates
                break
        ch2[pointer] = a1  # carry out cross over

        for j in range(length):
            if a2 == ch1[j]:
                ch1[j] = ch1[pointer]  # make sure there are no duplicates
                break
        ch1[pointer] = a2  # carry out cross over
        #print("CH1 - CH2  CROSS OVER", ch1, "\n", ch2, "\n")

    return ch1, ch2


def mutation(ch1: Chromosome, num: int = 1, probability: float = 0.5) -> Chromosome:
    for i in range(num):
        m = random.randrange(p) + 1  # mutation allele
        index = random.randrange(r)  # new position for the mutation allele

        if random.random() > probability:
            for j in range(r):
                if m == ch1[j]:
                    ch1[j] = ch1[index]  # make sure there are no duplicates
                    break
            ch1[index] = m  # carry out mutation
    # print("CH1 MUTATION", ch1,"\n")

    return ch1


def selection_pair(population: Population, choiceMatrix: List) -> [Chromosome, Chromosome]:  # we can pass fitness function instead of list
    return random.choices(
        population=population,
        weights=[fitness(gene, choiceMatrix) for gene in population],
        k=2
    )


def run_evolution(choiceMatrix: List, fitness_limit: int, generation_limit: int) -> [Population, int]:
    population = generate_population(size)

    # for i in range(generation_limit):
    # compare fitnesses and return the top 2 solutions \ if their fitenss is the best of all then break

    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness(genome, choiceMatrix), reverse=True)

        maxFitness = fitness(population[0], choiceMatrix)
        if i % 100 == 0:
            print(f"max = {maxFitness}, I = {i}")
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

population, i = run_evolution(convert_to_list(Matrix), desiredFitness, maxGen)

print("Population is", population, "Times ", i)
print("Data", data, "\n")
maxFitness = fitness(population[0], convert_to_list(Matrix))
print(f"max = {maxFitness}  out of {maxGen}")
print(population[0])

#____________________________________________________________________
# import random
# from array import *
# from typing import List, Optional, Callable, Tuple
#
# # Creates a list containing 36 lists, each of 3 items, all set to 0
# p = 38      # number of project ideas
# r, c = 36, 4  # r:row: number of student groups, c:column
# size = 100;
# Matrix = [[0 for x in range(r)] for y in range(c)]
# List = [[0 for x in range(r)] for y in range(c)]
# Chromosome = []
# Population = [Chromosome]
# ChoiceMatrix: []
# fitness = 0;
#
#
# def read_selections() -> Matrix:
#     with open("students_selections.txt") as textFile:
#         Matrix = [line.split("-") for line in textFile]
#
#     Matrix = [[s.rstrip(' \n ') for s in nested] for nested in Matrix]
#
#     #print(Matrix)
#     return Matrix
#
#
# def convert_to_list(Matrix) -> List:
#     Matrix = read_selections()
#     List = Matrix.copy()
#     for i in range(r):
#         del List[i][0]
#
#     for i in range(r):
#         for j in range(c - 1):
#             List[i][j] = int(List[i][j])
#
#     ChoiceMatrix = List
#     return List
#
#
# def generate_Chromosome(length: int) -> Chromosome:  # need to pass list as argument
#     projects = [x for x in range(p)]
#     random.shuffle(projects)
#     ch1 = projects[:36]
#     print("generated new chromosome:  \n", ch1)
#     return ch1
#
#
# def generate_population(size: int) -> Population:
#     return [generate_Chromosome(r) for i in range(size)]
#
#
# def fitness(chromosome: Chromosome, choiceMatrix: list) -> int:
#     score: int = 0
#     for i in range(r):
#         if chromosome[i] == choiceMatrix[i][0]:
#             score += 4
#         elif chromosome[i] == choiceMatrix[i][1]:
#             score += 3
#         elif chromosome[i] == choiceMatrix[i][2]:
#             score += 2
#
#     return score
#
#
# def crossover(ch1: Chromosome, ch2: Chromosome) -> [Chromosome, Chromosome]:
#     numOfCrossedallels = 3
#     length = len(ch1)
#
#     pointOfCrossover = random.randint(0, length - 1)
#     #numOfCrossedallels = length - pointOfCrossover
#     for i in range(numOfCrossedallels):
#         pointer = (pointOfCrossover + i) % length
#         a1 = ch1[pointer]  # allele that will cross from ch1 to ch2
#         a2 = ch2[pointer]  # allele that will cross from ch2 to ch1
#
#         for j in range(length):
#             if a1 == ch2[j]:
#                 ch2[j] = ch2[pointer]   # make sure there are no duplicates
#                 break
#         ch2[pointer] = a1   # carry out cross over
#
#         for j in range(length):
#             if a2 == ch1[j]:
#                 ch1[j] = ch1[pointer]   # make sure there are no duplicates
#                 break
#         ch1[pointer] = a2   # carry out cross over
#
#     return ch1, ch2
#
#
# def mutation(ch1: Chromosome, num: int = 1, probability: float = 0.2) -> Chromosome:
#     for i in range(num):
#         m = random.randrange(p) + 1        # mutation allele
#         index = random.randrange(r)     # new position for the mutation allele
#
#         if random.random() > probability:
#             for j in range(r):
#                 if m == ch1[j]:
#                     ch1[j] = ch1[index]  # make sure there are no duplicates
#                     break
#             ch1[index] = m  # carry out mutation
#
#     return ch1
#
#
# def selection_pair(population: Population, choiceMatrix: List) -> [Chromosome, Chromosome]: # we can pass fitness function instead of list
#     # fitnessList = []
#     # temp = []
#     # maxnum1 = 0;
#     # maxnum2 = 0;
#     # for i in range(size):
#     #     print(population[i], " Fitness is : ", fitness(population[i], list))
#     #     fitnessList.append(fitness(population[i], list))
#     #
#     # temp = fitnessList.copy()
#     # maxnum1 = max(temp)
#     # temp.remove(maxnum1)
#     # maxnum2 = max(temp)
#     # print("Max 1  is", population[fitnessList.index(maxnum1)], "\n", "Max 2 is ",
#     #       population[fitnessList.index(maxnum2)])
#     #
#     # return population[fitnessList.index(maxnum1)], population[fitnessList.index(maxnum2)]
#
#     return random.choices(
#         population=population,
#         weights=[fitness(gene, choiceMatrix) for gene in population],
#         k=2
#     )
#
#
#
# def run_evolution(choiceMatrix: List, fitness_limit: int, generation_limit: int) -> [Population, int]:
#
#     population = generate_population(size)
#
#     #for i in range(generation_limit):
#         # compare fitnesses and return the top 2 solutions \ if their fitenss is the best of all then break - need to figure it out - does sorted work?
#         # population = sorted(population,key=fitness(population[i],list), reverse= True)
#
#     for i in range(generation_limit):
#         population = sorted(population, key=lambda genome: fitness(genome, choiceMatrix), reverse=True)
#
#         # for x in range(size):
#         #     if fitness(population[x], choiceMatrix) >= fitness_limit:
#         #         print("should return the best 2 chromosomes")
#
#         maxFitness = fitness(population[0], choiceMatrix)
#         if i%100 == 0:
#             print(f"max = {maxFitness}, I = {i}")
#         if maxFitness >= fitness_limit:
#             break
#
#         next_generation = population[0:2]
#
#         for j in range(int(len(population) / 2) - 1):
#             parents = selection_pair(population, choiceMatrix)
#             ch1, ch2 = crossover(parents[0].copy(), parents[1].copy())
#             ch1 = mutation(ch1)
#             ch2 = mutation(ch2)
#             next_generation += [ch1, ch2]
#
#         population = next_generation
#
#
#     population = sorted(population, key=lambda genome: fitness(genome, choiceMatrix), reverse=True)
#
#     return population, i
#
#
# # selection_pair(generate_population(size), convert_to_list(Matrix))
# print("X")
# population, i = run_evolution(convert_to_list(Matrix), 100, 10000)
# maxFitness = fitness(population[0], convert_to_list(Matrix))
# print(f"max = {maxFitness}")
# print(population[0])
#
#
#
#
#
#
#
#
#
#
#
#
