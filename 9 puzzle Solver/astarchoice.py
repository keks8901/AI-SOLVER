#import additional libraries of time to record the performance 
#and copy to make copy of original puzzle when required
import copy,time

#function to represent puzzles path in the terminal
def print_puzzle(puzzle,goal,heuristic):
    #variable to keep track of generations expanded
    g = 0
    #for puzzle in path
    for p in puzzle:
        #print its h score
        print("h", heuristics_function(p,goal,heuristic))
        #print generation
        print("Generation: ", g)
        #print puzzle
        if p != puzzle[-1]:
            g += 1
            print(p[:3])
            print(p[3:6])
            print(p[6:9])
            print("    |")
            print("    |")
            print("    V")
        #the last one does not need arrows
        else:
            g += 1
            print(p[:3])
            print(p[3:6])
            print(p[6:9])

#function to find index of a particular integer in the puzzle
def find_index(puzzle,num):
    #get this integer index
    index = puzzle.index(num)
    #split it into i,j coordinates of a 3x3 matrix 
    i = index // 3
    j = index - i * 3
    #return both
    return i,j

#function to find all possible directions where the 0 can be moved in a specifed puzzle
def find_direction(puzzle):
    #predefined variables for easier conversion
    final_direction = []
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    dir = {
        (-1,0):"up",
        (1,0):"down",
        (0,-1):"left",
        (0,1):"right"
    }
    #get the coordinate of 0 
    i,j = find_index(puzzle, 0)
    #in all possible directions
    for d in directions:
        #find the possible ones for our puzzle
        if not ((i+d[0]<0) or (i+d[0]>2) or (j+d[1]<0) or (j+d[1]>2)):
            #append it to a list
            final_direction.append(dir[d])
    #retrun the list of all possible directions in text
    return final_direction

#fucntion that by using possible directions and the puzzle generates new puzzles 
def generate_puzzles(puzzle,possible_directions):
    #predefined variables for easier conversion
    possible_direction = []
    new_puzzles = []
    dir = {
        "up":(-1,0),
        "down":(1,0),
        "left":(0,-1),
        "right":(0,1)
    }
    #get the coordinate of 0 
    i,j = find_index(puzzle, 0)
    #get the coordinates of possible movments using the directions we know 
    for d in possible_directions:
        #append it a semparate list
        possible_direction.append((i+dir[d][0], j+dir[d][1]))
    #for each coordinate we construnct a puzzle
    for direction in possible_direction:
        #new puzzle
        new_puzzle = []
        #we copy the initial puzzle into new puzzle
        for p in puzzle:
            new_puzzle.append(p) 
        #get the coordinates 
        indx = i * 3 + j
        go_indx = direction[0] * 3 + direction[1]
        #change then with the correction of the direction
        new_puzzle[indx],new_puzzle[go_indx] = new_puzzle[go_indx],new_puzzle[indx]
        #append new puzzle to a list of new puzzles
        new_puzzles.append(new_puzzle)
    #return list of new puzzles
    return new_puzzles

#function that calculates the h(x) value
def heuristics_function(start,goal,heuristic):
    #0 at the start
    h = 0
    #depending on what user enters it is either calculated by

    #Manhattan Distance
    if heuristic == 1:
        #for each integer in puzzle
        for num in start:
            #find statring coordinates
            i,j = find_index(start,num)
            #find goal coordinates
            x,y = find_index(goal,num)
            #use formula
            h = h + abs(i-x) + abs(j-y)
    #or Misplaced Tiles
    elif heuristic == 2:
        #for each integer in puzzle
        for num in start:
            #find statring coordinates
            i,j = find_index(start,num)
            #find goal coordinates
            x,y = find_index(goal,num)
            #if they are not the same
            if i != x or j != y:
                #tile is misplaced therefore add 1 to h(x)
                h += 1
    #return the h(x) value for that grid           
    return h

#function to find the best move depending on the h(x) value
def find_min(possible_steps,goal,heuristic):
    #define a list of all h values
    h = []
    #for every direction of a puzzle
    for dir in possible_steps:
        #calculate h(x)
        num = heuristics_function(dir,goal,heuristic)
        #append it to the list that was defined
        h.append(num)
    #find the smallest h(x)
    min_value = min(h)
    #based on the number of h(x) find its index
    index = h.index(min_value)
    #based on the index find the corresponding puzzle
    best = possible_steps[index]
    #return the puzzle with the smallest h(x) value
    return best

#function that converts list of integers to strings
def convert_to_str(puzzle):
    #for each integer in list
    string_ints = [str(int) for int in puzzle]
    #convert into string and splpit with a comma
    str_of_ints = ",".join(string_ints)
    #return the string
    return str_of_ints

#solution function 
def solution(start,goal,heuristic):
    #solution is a copy of the start
    solution = copy.deepcopy(start)
    #g value to compare what generation the puzzle was made in
    g = 0
    #a dictionary of string puzzles and realted generations
    check = {convert_to_str(solution):1}
    #path of the solution
    path = [solution]

    #while the solution is not equal to the goal
    while solution != goal:
        #good list represents the list of free moves so that when moving the algorithm whould not end up in the loop
        #also this part has the draw back that is described in the paper documentation
        #for some reason it does not always work correctly, and i have not found a way to solve it
        good_list = []
        #get the current possible directions
        pos_dir = find_direction(solution)
        #get the current possible puzzles/moves
        step_list = generate_puzzles(solution,pos_dir)
        #loop to check if the puzzle has been previously used
        for step in step_list:
            #if it was in the previous generation
            if convert_to_str(step) in check:
                #but the current generation is different 
                if g < check[convert_to_str(step)]:
                    #assign it a new generation
                    check[convert_to_str(step)] = g 
                    #append it to good list of paths
                    good_list.append(step)
                #else skip and not assign it to the good list
                #otherwise there will be a loop
            #if puzzle has never been in the dictinary then
            else:
                #append a current genetration to it
                check[convert_to_str(step)] = g
                #append it to the good list
                good_list.append(step)
        #find the best move depending on its h(x)
        solution = find_min(good_list,goal,heuristic)
        #append it to path
        path.append(solution)
        #generation plus one
        g += 1
        #will run untill the puzzle is solved 
    
    #if solution is equal to goal then return the path, goal and the heuristic method that was used
    return path,goal,heuristic

#my start and goal puzzle states
strt = [4,3,1,6,7,2,0,8,5]
goal_puzzle = [0,1,2,3,4,5,6,7,8]

#ask user for the heuristic they want
print("Two versions of the A* algorithm: 1.Manhattan distances 2.Misplaced tiles ")
x = int(input())
#record performance
start_time = time.time()
#solve the puzzle
path,goal,heurisitc = solution(strt,goal_puzzle,x)
#print performace 
print("This operation took: ", time.time() - start_time)
#print step-by-step path from start to goal, using the solution variables
print_puzzle(path,goal,heurisitc)