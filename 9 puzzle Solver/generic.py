#import solve function from previous excercise 
from astarchoice import solution

#fuction to check if the puzzle is solvable
def solvable(puzzle):
    #inversions of puzzle (when a tile precedes another tile with a lower number on it)
    #if the number of inversions is odd the puzzle is unsolvable
    inversions = 0

    #in puzzle
    for i in range(8):
        #calculate number of inveresions
        for j in range(i+1, 9):
            if puzzle[j] and puzzle[i] and puzzle[i] > puzzle[j]:
                inversions += 1

    #return True if even, False if not
    return inversions % 2 == 0

#make varaibles for user input
start = []
goal = []

#ask user to enter the starting puzzle 
print("Enter the 8 puzzle problem: \n")

#one by one read users input
for i in range(9):
    x = int(input())
    start.append(x) 
    
#ask user to enter the goal puzzle 
print("Enter the 8 puzzle goal: \n")

#one by one read users input
for i in range(9):
    x = int(input())
    goal.append(x) 

#check if the puzzle is solvable 
if solvable(start) != True:
    #if not exit from the program
    print("Unsolvable Puzzle")
    quit()
else:
    #if solvable then solve the puzzle using the algorithm from previous excercise
    #using "Manhattan Distance"
    print(solution(start,goal,1))

