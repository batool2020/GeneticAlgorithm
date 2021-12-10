import random
from array import *
from typing import List, Optional, Callable, Tuple
import wx
import wx.grid as grid
import matplotlib.pyplot as plt

r, c = 0, 4  # r:row: number of student groups, c:column
p = 0  # number of project ideas
desiredFitness = 0  # when to stop the algorithm
maxGen = 0  # maximum loops
filePath = ""  # student choices file
size = 100  # initial population size
numOfCrossedallels = 6  # number of exchanged alleles during crossover
probability = 0.5       # probability of mutation
numOfMutations = 1      # number of possible mutations for each child


# Type specification
Matrix = [[0 for x in range(r)] for y in range(c)]
List = [[0 for x in range(r)] for y in range(c)]
Chromosome = []
Population = [Chromosome]
ChoiceMatrix: []

# Reads student choices file
def read_selections() -> Matrix:
    with open(filePath) as textFile: #"students_selections.txt"
        Matrix = [line.split("-") for line in textFile]

    Matrix = [[s.rstrip(' \n ') for s in nested] for nested in Matrix]
    return Matrix

# Converts file into a List
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

# Generates a single chromosome, a list of 36 unique integers from 1-38
def generate_Chromosome(length: int) -> Chromosome:  # need to pass list as argument
    projects = [x+1 for x in range(p)]
    random.shuffle(projects)        # randomize chromosome
    ch1 = projects[:36]
    print("generated new chromosome:  \n", ch1)
    return ch1

# Generate initial population of a given size.
def generate_population(size: int) -> Population:
    return [generate_Chromosome(r) for i in range(size)]

# returns a fitness score for the chromosome
def fitness(chromosome: Chromosome, choiceMatrix: list) -> int:
    score: int = 0
    for i in range(r):
        if chromosome[i] == choiceMatrix[i][0]:     # group gets the first choice
            score += 4
        elif chromosome[i] == choiceMatrix[i][1]:   # group gets the second choice
            score += 3
        elif chromosome[i] == choiceMatrix[i][2]:   # group gets the third choice
            score += 2

    if chromosome[33] == 19:  # group 33 is our graduation project group :)
        score += 2
    return score


# takes 2 chromosomes and combines them to produce 2 new chromosomes.
def crossover(ch1: Chromosome, ch2: Chromosome, numOfCrossedallels = 3) -> [Chromosome, Chromosome]:
    length = len(ch1)

    pointOfCrossover = random.randint(0, length - 1)  # where the exchange starts

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

    return ch1, ch2


# alters one or more alleles to a random unique value
def mutation(ch1: Chromosome, num: int = 1, probability: float = 0.5) -> Chromosome:
    for i in range(num):
        m = random.randrange(p) + 1  # mutation allele
        index = random.randrange(r)  # new position for the mutation allele

        if random.random() < probability:
            for j in range(r):
                if m == ch1[j]:
                    ch1[j] = ch1[index]  # make sure there are no duplicates
                    break
            ch1[index] = m  # carry out mutation

    return ch1


# selects 2 chromosomes from the population to be the next parents
def selection_pair(population: Population, choiceMatrix: List) -> [Chromosome, Chromosome]:
    return random.choices(
        population=population,  # the fitter the chromosome, the higher the probability it will be a parent
        weights=[fitness(gene, choiceMatrix) for gene in population],
        k=2
    )


# The driver function, keeps generating new children
# until the fitness requirement is met or a max number of generations is created
def run_evolution(choiceMatrix: List, fitness_limit: int, generation_limit: int, numOfCrossedallels, probability, numOfMutations, size) -> [Population, int]:
    population = generate_population(size)  # create initial population
    fitnesses =[]

    for i in range(generation_limit):       # sort chromosomes
        population = sorted(population, key=lambda genome: fitness(genome, choiceMatrix), reverse=True)

        maxFitness = fitness(population[0], choiceMatrix)
        if i % 100 == 0:
            print(f"max = {maxFitness}, I = {i}")
        if i% 10 == 0:
            fitnesses.append(maxFitness)
        if maxFitness >= fitness_limit:             # check if requirement is reached
            break

        next_generation = population[0:2]           # take the best 2 chromosomes to the next generation

        for j in range(int(len(population) / 2) - 1):
            parents = selection_pair(population, choiceMatrix)            # choose the next 2 parents
            ch1, ch2 = crossover(parents[0].copy(), parents[1].copy(), numOfCrossedallels)    # produce children
            ch1 = mutation(ch1, numOfMutations, probability)
            ch2 = mutation(ch2, numOfMutations, probability)
            next_generation += [ch1, ch2]           # add to next generation

        population = next_generation

    population = sorted(population, key=lambda genome: fitness(genome, choiceMatrix), reverse=True)

    return population, i, fitnesses    # return final population, and number of generations, and list of fitnesses.


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




class OtherFrame(wx.Frame):
    """
    Class used for creating frames other than the main one
    """

    def __init__(self, title, result, parent=None):
        wx.Frame.__init__(self, parent=parent, title=title, size=(500, 500))
        self.DisplayResults(result)
        self.Show()

    def DisplayResults(self, result):
        self.panel = MyPanel(self, result)
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
        self.ProjectsNum = wx.SpinCtrl(self, wx.ID_ANY, value='38')
        self.ProjectsNum.SetRange(0,1000)

        labelGroupsNum = wx.StaticText(self, wx.ID_ANY, 'Number of Groups ')
        self.GroupsNum = wx.SpinCtrl(self, wx.ID_ANY, value='36')
        self.GroupsNum.SetRange(0,1000)

        labelInitialPop = wx.StaticText(self, wx.ID_ANY, '# of Initial Population')
        self.InitialPop = wx.SpinCtrl(self, wx.ID_ANY, value="50", min=0, max=50)

        labelnumOfCrossedallels = wx.StaticText(self, wx.ID_ANY, 'Number of Crossed Alleles ')
        self.numOfCrossedallels = wx.SpinCtrl(self, wx.ID_ANY, value='3')

        labelMutationProb = wx.StaticText(self, wx.ID_ANY, 'Mutation Probability')
        self.MutationProb = wx.SpinCtrlDouble(self, wx.ID_ANY, value="50", min=0, max=100)

        labelMutationNum = wx.StaticText(self, wx.ID_ANY, 'Number of Mutations')
        self.MutationNum = wx.SpinCtrl(self, wx.ID_ANY, value="1", min=0, max=10)

        labelMaxFitness = wx.StaticText(self, wx.ID_ANY, 'Maximum Fitness')
        self.MaxFitness = wx.SpinCtrl(self, wx.ID_ANY, value="100", min=0, max=1000)
        self.MaxFitness.SetRange(0,1000)

        labelMaxGeneration = wx.StaticText(self, wx.ID_ANY, 'Maximum Generation')
        self.MaxGeneration = wx.SpinCtrl(self, wx.ID_ANY, value="200", min=0, max=1000000)
        self.MaxGeneration.SetRange(0,1000000)

        self.okBtn = wx.Button(self, wx.ID_ANY, 'Start')
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
        inputTwoSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputThreeSizer = wx.BoxSizer(wx.HORIZONTAL)
        inputFourSizer = wx.BoxSizer(wx.HORIZONTAL)
        submitBtnSizer = wx.BoxSizer(wx.HORIZONTAL)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        ProjectsNum = wx.BoxSizer(wx.HORIZONTAL)
        numOfCrossedallels = wx.BoxSizer(wx.HORIZONTAL)
        ChoicesNum = wx.BoxSizer(wx.HORIZONTAL)
        MaxFitness = wx.BoxSizer(wx.HORIZONTAL)
        MaxGeneration = wx.BoxSizer(wx.HORIZONTAL)
        InitialPop = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(title, 0, wx.ALL, 5)

        inputOneSizer.Add(labelProjectsNum, 0, wx.ALL, 5)

        inputOneSizer.Add(self.ProjectsNum, 1, wx.ALL | wx.EXPAND, 5)

        inputOneSizer.Add(labelGroupsNum, 0, wx.ALL, 5)
        inputOneSizer.Add(self.GroupsNum, 1, wx.ALL | wx.EXPAND, 5)

        inputOneSizer.Add(labelInitialPop, 0, wx.ALL, 5)
        inputOneSizer.Add(self.InitialPop, 1, wx.ALL | wx.EXPAND, 5)

        inputThreeSizer.Add(labelMaxFitness, 0, wx.ALL, 5)
        inputThreeSizer.Add(self.MaxFitness, 1, wx.ALL | wx.EXPAND, 5)

        inputTwoSizer.Add(labelnumOfCrossedallels, 0, wx.ALL, 5)
        inputTwoSizer.Add(self.numOfCrossedallels, 1, wx.ALL | wx.EXPAND, 5)

        inputThreeSizer.Add(labelMaxGeneration, 0, wx.ALL, 5)
        inputThreeSizer.Add(self.MaxGeneration, 1, wx.ALL | wx.EXPAND, 5)

        inputThreeSizer.Add(labelMutationProb, 0, wx.ALL, 5)
        inputThreeSizer.Add(self.MutationProb, 1, wx.ALL | wx.EXPAND, 5)

        inputThreeSizer.Add(labelMutationNum, 0, wx.ALL, 5)
        inputThreeSizer.Add(self.MutationNum, 1, wx.ALL | wx.EXPAND, 5)

        inputFourSizer.Add(labelFileName, 0, wx.ALL, 5)
        inputFourSizer.Add(self.OpenFileBtn, 1, wx.ALL | wx.EXPAND, 5)

        submitBtnSizer.Add(self.okBtn, 0, wx.ALL, 5)
        submitBtnSizer.Add(self.cancelBtn, 0, wx.ALL, 5)

        mainSizer.Add(titleSizer, 0, wx.CENTER)
        mainSizer.Add(wx.StaticLine(self, ), 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(inputOneSizer, 0, wx.ALL | wx.EXPAND, 5)
        mainSizer.Add(inputTwoSizer, 0, wx.ALL|wx.EXPAND, 5)
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
        global r, numOfCrossedallels, probability,numOfMutations
        global p,maxGen,desiredFitness, size
        if self.GroupsNum.GetValue() > 0:
            r = self.GroupsNum.GetValue()
        if self.ProjectsNum.GetValue() >= r:
            p = self.ProjectsNum.GetValue()
        if self.MaxFitness.GetValue() > 0 and self.MaxFitness.GetValue() < 4*p:
            desiredFitness = self.MaxFitness.GetValue()
        if self.MaxGeneration.GetValue() > 0:
            maxGen = self.MaxGeneration.GetValue()
        numOfCrossedallels = self.numOfCrossedallels.GetValue()
        probability = float(float(self.MutationProb.GetValue())/100.0)
        numOfMutations = self.MutationNum.GetValue()
        size = self.InitialPop.GetValue()



        print(f"p: {p}, r: {r}, fitness:{desiredFitness}, maxgen:{maxGen}")

        population, i, fitnesses = run_evolution(convert_to_list(Matrix), desiredFitness, maxGen,
                                                 numOfCrossedallels, probability, numOfMutations, size)

        print("Population is", population, "Times ", i)
        maxFitness = fitness(population[0], convert_to_list(Matrix))
        print(f"max = {maxFitness}  out of {maxGen}")
        print(population[0])

        xaxis = [x*10 for x in range(len(fitnesses))]
        plt.plot(xaxis,fitnesses)
        plt.ylabel('Fitnesses')
        plt.xlabel('Generation number')
        plt.show()

        res = population[0]
        res.append(i+1)
        res.append(maxFitness)
        frame = OtherFrame(title="Results", result=population[0])



class MyPanel(wx.Panel):
    def __init__(self, parent, result):
        super(MyPanel, self).__init__(parent)

        mygrid = grid.Grid(self)
        mygrid.CreateGrid(37,4)


        print(f"res: {result}")
        choiceMatrix = convert_to_list(Matrix)
        for i in range(r):
            for j in range(3):
                mygrid.SetCellValue(i, j, str(choiceMatrix[i][j]))

        for i in range(r):
            if choiceMatrix[i][0] == result[i]:
                mygrid.SetCellBackgroundColour(i, 0, wx.Colour(0, 255, 0))
            elif choiceMatrix[i][1] == result[i]:
                mygrid.SetCellBackgroundColour(i, 0, wx.Colour(255, 0, 0))
                mygrid.SetCellBackgroundColour(i, 1, wx.Colour(0, 255, 0))
            elif choiceMatrix[i][2] == result[i]:
                mygrid.SetCellBackgroundColour(i, 0, wx.Colour(255, 0, 0))
                mygrid.SetCellBackgroundColour(i, 1, wx.Colour(255, 0, 0))
                mygrid.SetCellBackgroundColour(i, 2, wx.Colour(0, 255, 0))
            else:
                mygrid.SetCellBackgroundColour(i, 0, wx.Colour(255, 0, 0))
                mygrid.SetCellBackgroundColour(i, 1, wx.Colour(255, 0, 0))
                mygrid.SetCellBackgroundColour(i, 2, wx.Colour(255, 0, 0))
                mygrid.SetCellValue(i, 3, str(result[i]))

        mygrid.SetCellValue(36, 0, "Max fit:")
        mygrid.SetCellValue(36, 1, str(result[37]))
        mygrid.SetCellValue(36, 2, "generations:")
        mygrid.SetCellValue(36, 3, str(result[36]))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mygrid, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SendSizeEvent()


# Run the program
if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()

