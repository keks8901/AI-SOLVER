#imported libraries 
#time for performance measures
#copy to copy sudokus when needed
import time,copy 
#to use when deviding sudoku into parts
import numpy as np
#randint function for random mutations
from random import randint

'''This program split into parts for easier explanations'''

#########################################################################################################################
### PREDEFINED VARIABLES ###
#variable M used to solve sudokus before the evolutionary algorithm
M = 9
grid1 = [ [3, 0, 0, 0, 0, 5, 0, 4, 7], [0, 0, 6, 0, 4, 2, 0, 0, 1], [0, 0, 0, 0, 0, 7, 8, 9, 0], [0, 5, 0, 0, 1, 6, 0, 0, 2], [0, 0, 3, 0, 0, 0, 0, 0, 4], [8, 1, 0, 0, 0, 0, 7, 0, 0], [0, 0, 2, 0, 0, 0, 4, 0, 0], [5, 6, 0, 8, 7, 0, 1, 0, 0], [0, 0, 0, 3, 0, 0, 6, 0, 0],]
grid2 = [[0, 0, 2, 0, 0, 0, 6, 3, 4], [1, 0, 6, 0, 0, 0, 5, 8, 0], [0, 0, 7, 3, 0, 0, 2, 9, 0], [0, 8, 5, 0, 0, 1, 0, 0, 6], [0, 0, 0, 7, 5, 0, 0, 2, 3], [0, 0, 3, 0, 0, 0, 0, 5, 0], [3, 1, 4, 0, 0, 2, 0, 0, 0], [0, 0, 9, 0, 8, 0, 4, 0, 0], [7, 2, 0, 0, 4, 0, 0, 0, 9],]
grid3 = [[0, 0, 4, 0, 1, 0, 0, 6, 0], [9, 0, 0, 0, 0, 0, 0, 3, 0], [0, 5, 0, 7, 9, 6, 0, 0, 0], [0, 0, 2, 5, 0, 4, 9, 0, 0], [0, 8, 3, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 6, 0, 7], [0, 0, 0, 9, 0, 3, 0, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 0, 0, 0, 0, 1, 0],]
#I have transfered the grids from the file to the program straight away to easily work with them
#########################################################################################################################
### ALGORITHM TO SOLVE SUDOKU FOR THE EVOLUTIONARY ALGORITHM ###

#function to check if it is possible to solve the grid
def check_solvable(grid, row, col, val):
    #check simular numbers in row
    for j in range(0, 9):
        if grid[row][j] == val:
            #return false
            return False
    #check simular numbers in columns
    for i in range(0, 9):
        if grid[i][col] == val:
            #return false
            return False
    #fnial check of squares
    startRow = (row // 3) * 3
    startCol = (col // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[startRow+i][startCol+j] == val:
                return False
    #if everything is not repeating than retrun true
    return True

#function that finds the solved sudoku
def find_suduko(grid, row, col):
    #M variable is representation of how big sudoku is (for this function its 9x9)
    #check rows and columns in the grid
    #skip a turn
    if (row == M - 1 and col == M):
        #if ok return true
        return True
    #if column is succesful
    if col == M:
        #add one to row
        row += 1
        #reset columns
        col = 0
    #if the numbers are different
    if grid[row][col] > 0:
        #try again
        return find_suduko(grid, row, col + 1)
    #for numbers in the grif
    for num in range(1, M + 1, 1): 
        #get the new numbers of rows and columns
        if check_solvable(grid, row, col, num):
            grid[row][col] = num
            #if this particular sudoku grid is fine
            if find_suduko(grid, row, col + 1):
                #return true
                return True
        #else reset
        grid[row][col] = 0
    #try again when grid did not successed
    return False
 
#function that checks if sudoku is solved and returns the solved one if it exists
def solve_sudoku(grid):
    #solved sudoku variable 
    solved_sudoku = []
    #if it can be solved 
    if (find_suduko(grid, 0, 0)) == True:
        #append to the solved sudoku
        solved_sudoku = grid
    #if it cant solve it
    else:
        #print that sudoku is unsolvable
        print("Unsolvable Sudoku")
        #exit the program
        exit()
    #return the solved sudoku
    return solved_sudoku

#########################################################################################################################
### SUDOKU GRID RELATED FUNCTIONS ###

#function to print the grid in the terminal
def print_sudoku(grid):
    #top line of the grid
    print("-"*36)
    #layout of the grid 
    for i, row in enumerate(grid):
        #printing rows using special format
        print(("|" + " {}   {}   {} |"*3).format(*[x if x != 0 else " " for x in row]))
        if i == 8:
            print("-"*37)
        elif i % 3 == 2:
            print("|" + "---+"*8 + "---|")
        else:
            print("|" + "   +"*8 + "   |")
    #return grid
    return grid

#function that returns all rows of the grid
def get_rows(grid):
    #variable of row values
    row_values = []
    #for each line of the grid
    for line in grid:
        #append it to the row values variable
        row_values.append(line)
    #return the rows
    #due to list of lists format that i have picked it is very simple to get rows
    return row_values

#function that returns all columns of the grid
def get_columns(grid):
    #variable of column values
    column_values = []
    #get rows of the same grid
    row_values = get_rows(grid)
    #using np.array transpose function we get the colums
    numpy_array = np.array(row_values)
    transpose = numpy_array.T
    column_values = transpose.tolist() 

    #return the columns
    return column_values

#function that returns all squares of the grid
def get_squares(grid):
    #variable of square values
    square_values = []
    #again we need rows of the grid
    row_values = get_rows(grid)
    #hardcoding of splitting the excisting values of the grid into 3x3 squares
    square1 = [row_values[0][:3]+row_values[1][:3]+row_values[2][:3]]
    square2 = [row_values[3][:3]+row_values[4][:3]+row_values[5][:3]]
    square3 = [row_values[6][:3]+row_values[7][:3]+row_values[8][:3]]
    square4 = [row_values[0][3:6]+row_values[1][3:6]+row_values[2][3:6]]
    square5 = [row_values[3][3:6]+row_values[4][3:6]+row_values[5][3:6]]
    square6 = [row_values[6][3:6]+row_values[7][3:6]+row_values[8][3:6]]
    square7 = [row_values[0][6:9]+row_values[1][6:9]+row_values[2][6:9]]
    square8 = [row_values[3][6:9]+row_values[4][6:9]+row_values[5][6:9]]
    square9 = [row_values[6][6:9]+row_values[7][6:9]+row_values[8][6:9]]
    #make the end list of lists squares values
    square_values = (square1 + square2 + square3 + square4 + square5 + square6 + square7 + square8 + square9 )
    #return square values
    return square_values

#########################################################################################################################
### INDIVIDUAL OPERATIONS ###

#function that returns the total mistakes of the grid
def check_grid(grid):
    #get all the rows, columns and squares of a grid
    row_values = get_rows(grid)
    column_values = get_columns(grid)
    square_values = get_squares(grid)
    #mistake is 0 at the start
    mistake = 0
    #for rows
    for row in row_values:
        #translate it into paired list of lists where the 0 index is the integer in the grid 
        #and 1 index is how much time it repeats in the row
        r = [[x,row.count(x)] for x in set(row)]
        #for each pair
        for pair in r:
            #if 1 index is more then 1
            if pair[1] > 1:
                #record a mistake
                mistake = mistake + pair[1]-1
    #for column
    for column in column_values:
        #translate it into paired list of lists where the 0 index is the integer in the grid 
        #and 1 index is how much time it repeats in the column
        c = [[x,column.count(x)] for x in set(column)]
        #for each pair
        for pair in c:
            #if 1 index is more then 1
            if pair[1] > 1:
                #record a mistake
                mistake = mistake + pair[1]-1
    #for square
    for square in square_values:
        #translate it into paired list of lists where the 0 index is the integer in the grid 
        #and 1 index is how much time it repeats in the square
        s = [[x,square.count(x)] for x in set(square)]
        #for each pair
        for pair in s:
            #if 1 index is more then 1
            if pair[1] > 1:
                #record a mistake
                mistake = mistake + pair[1]-1
    #return mistake
    return mistake

#function that appends random integers in empty spaces of the grid
def mutate_grid(grid):
    #get a copy of the grid
    #otherwise it will change with every mutation and will not work
    grid_copy = copy.deepcopy(grid)
    #for line in the copy 
    for line in grid_copy:
        #for a row of 9 values
        for index in range(0,9):
            #if there is a 0 (which represent an empty cell in my algorithm)
            if line[index] == 0:
                #then change it to a random number between 1 and 9
                line[index] = randint(1,9)  
    #return the mutated grid  
    return grid_copy

#function that cleans the grid depending in the solved sudoku
def clean_grid(original, new):
    #get copies of the original(solved) and new(mutated) grids
    grid_copy = copy.deepcopy(new)
    original_copy = copy.deepcopy(original)
    #for lines in both grids
    for o, n in zip(original_copy,grid_copy):
        #and both values of each row
        for i1,i2 in zip(o,n):
            #if they are not equal then make the mutated value a 0, so that it can be mutated again
            if i1 != i2:
                n[o.index(i1)] = 0
                #make the same value a " " so that it will work through the full row and wont stop at the 1st apperence
                #of this integer
                o[o.index(i1)] = " "
    #return the cleaned grid
    return grid_copy

#########################################################################################################################
### POPULATION-LEVEL OPERATORS ###

#function that makes the population of the specified grid 
def make_population(grid, population_size):
    #list of all grids 
    grids = []
    #for the whole population
    for _ in range(0, population_size):
        #mutate the input grid and append it to the list of all grids
        #all mutations will be unique 
        grids.append(mutate_grid(grid))
    #return this list
    return grids

#function that finds 2 best grids in the population
def select_best_pair(population):
    #variables to work with
    all_the_grids = []
    number_of_mistakes = []   
    best_pair_of_grids = []
    #for grid in population
    for grid in population:
        #it makes 2 lists 
        #one with the grid 
        #and the other with the corresponding number of mistakes
        all_the_grids.append(grid)
        number_of_mistakes.append(check_grid(grid))
    #twice 
    for _ in range(0, 2):
        #get the index of the smallest mistake in the number_of_mistakes list
        index = number_of_mistakes.index(min(number_of_mistakes))
        #append the corresponding grid to the best pair list
        best_pair_of_grids.append(all_the_grids[index])
        #delete the current best grid (in terms of mistakes) so that the next best can be copied
        all_the_grids.pop(index)
        number_of_mistakes.pop(index)

    return best_pair_of_grids

#function that makes one grid out of the 2 best ones
def crossover(two_grids):
    g3 = []
    #split the list into 1st and 2nd grid
    g1 = two_grids[0]
    g2 = two_grids[1]
    #append one-by-one row of the 2 best into the 3rd
    g3.append(g1[0])
    g3.append(g2[1])
    g3.append(g1[2])
    g3.append(g2[3])
    g3.append(g1[4])
    g3.append(g2[5])
    g3.append(g1[6])
    g3.append(g2[7])
    g3.append(g1[8])
    #return the 3rd
    return g3

#########################################################################################################################
### EVOLUTION ALGORITHM ###

#the evolution algorithm
def evolution(grid, gen):
    #make the population
    population = make_population(grid, 10)
    #find the best pair
    best_pair = select_best_pair(population)
    #make one grid out of the best_pair
    best_grid = crossover(best_pair)

    #if the best pair has mistakes
    if check_grid(best_grid) != 0:
        #print generation number
        print ("THIS IS THE ", gen ," GENERATION")
        #add 1 to generation for the next step
        gen = gen + 1
        #print the amount of mistakes 
        print("Mistakes: ", check_grid(best_grid))
        #print the current grid
        print_sudoku(best_grid)
        #compare the current grid to the solved one to check what integers to keep in the grid
        n_b = clean_grid(solve_sudoku(grid), best_grid)
        #recursion with the new best grid and the new generation number
        evolution(n_b, gen)

    #if the best pair has no mistakes
    else:
        #print the solved sudoku 
        print("Solved Sudoku: ")
        print_sudoku(best_grid)
        #finish the algorithm
        return best_grid

#record start time 
start_time = time.time()
#do evolution 
evolution(grid2, 0)
#print how much time the solution took
print("Time spent: ",time.time() - start_time)
