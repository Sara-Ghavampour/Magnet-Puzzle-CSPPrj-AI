import math
from square import *
def assignment_is_done(board):  # check termination of backtracking  # is complete
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j].magnet_value==None : 
                return False

    return True 



def print_board(board):
    for i in range (len(board)):
        print("row ",i ," : ")
        for j in range(len(board[0])):
            print(board[i][j].value,end=" ")
        print()    


def mrv_Heuristic(board):
    min = math.inf 
    for i in range (len(board)):
        for j in range(len(board[0])):
            #print("len(board[i][j].domain_square) ",len(board[i][j].domain_square))
            if len(board[i][j].domain_square) < min  and len(board[i][j].domain_square) != 0: 
                min = len(board[i][j].domain_square)
                sqr=board[i][j]

    return sqr


def get_the_pair(sqr,board):
    pairSqr = None
    n = len(board)
    m = len(board[0])
    x= sqr.x
    y=sqr.y
    if x-1>=0 and board[x-1][y].value == sqr.value :
        pairSqr=board[x-1][y]
    elif x+1<n and board[x+1][y].value == sqr.value :
        pairSqr=board[x+1][y]
    elif y-1>=0 and board[x][y-1].value == sqr.value :
        pairSqr = board[x][y-1]
    elif y+1<n and board[x][y+1].value == sqr.value :
        pairSqr=board[x][y+1]

    return pairSqr


def backTrack_Csp(board):
    # print('csppp')
    # print_board(board)
    if assignment_is_done(board)==True:
        print("assignment_is_done: ")
        print_board(board)
        return True

    sqr = mrv_Heuristic(board)
    pairSqr = get_the_pair(sqr,board)
    print("Sqr : ",sqr.x,sqr.y,sqr.value)
    print("pairSqr : ",pairSqr.x,pairSqr.y,pairSqr.value)