import math
from square import *
import copy
def assignment_is_done(board):  # check termination of backtracking  # is complete
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j].magnet_value==None : 
                return False

    return True 



def print_board(board):
    print("------------------------")
    for i in range (len(board)):
        
        for j in range(len(board[0])):
            print(board[i][j].magnet_value,end=" ")
        print()    
    print("------------------------")

def mrv_Heuristic(board):
    min = math.inf 
    for i in range (len(board)):
        for j in range(len(board[0])):
            #print("len(board[i][j].domain_square) ",len(board[i][j].domain_square))
            if len(board[i][j].domain_square) < min  and len(board[i][j].domain_square) != 0 and board[i][j].magnet_value==None: 
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
    print(" domain fo sqr: ",sqr.domain_square)
    print(" domain of pairsqr: ",pairSqr.domain_square)

    ### iterate the domain : 
    for i in range (1):
    #for i in range (len(sqr.domain_square)):
        sqr_value = board[sqr.x][sqr.y].domain_square[i]
        curr_board = copy.deepcopy(board)

        # sqr_copy = copy.deepcopy(sqr)
        # pairSqr_copy =copy.deepcopy(pairSqr) 
        if sqr_value=='+':
            pair_value='-'
        elif sqr_value=='-':
            pair_value='+'
        elif sqr_value=='0':
            pair_value='0'

        curr_board[sqr.x][sqr.y].magnet_value = sqr_value  ## sqr_copy
        curr_board[pairSqr.x][pairSqr.y].magnet_value = pair_value  ##pairSqr_copy
       
        print_board(curr_board)
        print("curr sgr value : ",curr_board[sqr.x][sqr.y].magnet_value )
        print("curr pairsgr value : ",curr_board[pairSqr.x][pairSqr.y].magnet_value)

        ## remove these values from domain
        print("new domain fo sqr before remove : ",curr_board[sqr.x][sqr.y].domain_square)
          

        if sqr_value in curr_board[sqr.x][sqr.y].domain_square:
            print("*")
            curr_board[sqr.x][sqr.y].domain_square.remove(sqr_value)
            print("new domain fo sqr afterrr remove: ",curr_board[sqr.x][sqr.y].domain_square,sqr.x)
        print("new domain of pairsqr before remove : ",curr_board[pairSqr.x][pairSqr.y].domain_square,pairSqr.x)  
        if pair_value in curr_board[pairSqr.x][pairSqr.y].domain_square:
            print("**")
            curr_board[pairSqr.x][pairSqr.y].domain_square.remove(pair_value)
            print("new domain of pairsqr  afterrr remove: ",curr_board[pairSqr.x][pairSqr.y].domain_square)

        print("new domain fo sqr: ",curr_board[sqr.x][sqr.y].domain_square)
        print("new domain of pairsqr : ",curr_board[pairSqr.x][pairSqr.y].domain_square)

        print("Sqr : ",sqr.x,sqr.y,curr_board[sqr.x][sqr.y].magnet_value)
        print("pairSqr : ",pairSqr.x,pairSqr.y,curr_board[pairSqr.x][pairSqr.y].magnet_value )