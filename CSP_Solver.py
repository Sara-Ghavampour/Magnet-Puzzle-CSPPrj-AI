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


def check_consistency_with_neibours(board,sqr,pairSqr):  ### ?????
    n = len(board)
    m = len(board[0])
    x= sqr.x
    y=sqr.y
    x_pair= pairSqr.x
    y_pair=pairSqr.y
    if x-1>=0 and board[x-1][y].magnet_value == sqr.magnet_value :
        return False
    elif x+1<n and board[x+1][y].magnet_value == sqr.magnet_value :
        return False
    elif y-1>=0 and board[x][y-1].magnet_value == sqr.magnet_value :
        return False
    elif y+1<n and board[x][y+1].magnet_value == sqr.magnet_value :
        return False

    if x_pair-1>=0 and board[x_pair-1][y_pair].magnet_value == pairSqr.magnet_value :
        return False
    elif x_pair+1<n and board[x_pair+1][y_pair].magnet_value == pairSqr.magnet_value :
        return False
    elif y_pair-1>=0 and board[x_pair][y_pair-1].magnet_value == pairSqr.magnet_value :
        return False
    elif y_pair+1<n and board[x_pair][y_pair+1].magnet_value == pairSqr.magnet_value :
        return False    


    else :
        return True


def is_consistent(board,sqr,pairSqr):
    n = len(board)  ## rows
    m = len(board[0])  ## cols
    p_row =0
    n_row =0
    p_col=0
    n_col=0
    if check_consistency_with_neibours(board,sqr,pairSqr) == False :
        return False

    for i in range((0,n)):  ## rows
        p_row=0
        n_row=0
        for j in range(0,m):
            if board[i][j].magnet_value=='+': p_row+=1
            if board[i][j].magnet_value=='-': n_row+=1
        if p_row>board.row_positive_bound or n_row >board.row_negative_bound:
            return False


    for j in range(0,m): ## cols
        p_col=0
        n_col=0
        for i in range (0,n):
            if board[i][j].magnet_value=='+': p_col+=1
            if board[i][j].magnet_value=='-': n_col+=1

        if p_col> board.col_positive_bound or n_col> board.col_negative_bound:
            return False

    return True    



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
    for i in range (len(sqr.domain_square)):
    #for i in range (len(sqr.domain_square)):
        sqr_value = board[sqr.x][sqr.y].domain_square[i]
        curr_board = copy.deepcopy(board)

        # sqr_copy = copy.deepcopy(sqr)
        # pairSqr_copy =copy.deepcopy(pairSqr) 
        if sqr_value=='+':
            pair_value='-'
            # curr_board[sqr.x][sqr.y].domain_square.remove(sqr_value)
            # curr_board[pairSqr.x][pairSqr.y].domain_square.remove(pair_value)
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
          
        print("new domain of pairsqr before remove before if: ",curr_board[pairSqr.x][pairSqr.y].domain_square,pairSqr.x)  
        if curr_board[sqr.x][sqr.y].magnet_value in curr_board[sqr.x][sqr.y].domain_square:
            print("*")
            curr_board[sqr.x][sqr.y].domain_square.remove(sqr_value)
            print("new domain fo sqr afterrr remove: ",curr_board[sqr.x][sqr.y].domain_square,sqr.x)
        print("new domain of pairsqr before remove : ",curr_board[pairSqr.x][pairSqr.y].domain_square,pairSqr.x)  
        print(" some arbittt: ",curr_board[3][3].domain_square , 3)  
        if curr_board[pairSqr.x][pairSqr.y].magnet_value in curr_board[pairSqr.x][pairSqr.y].domain_square:
            print("**")
            curr_board[pairSqr.x][pairSqr.y].domain_square.remove(pair_value)
            print("new domain of pairsqr  afterrr remove: ",curr_board[pairSqr.x][pairSqr.y].domain_square)

        print("new domain fo sqr: ",curr_board[sqr.x][sqr.y].domain_square)
        print("new domain of pairsqr : ",curr_board[pairSqr.x][pairSqr.y].domain_square)

        print("Sqr : ",sqr.x,sqr.y,curr_board[sqr.x][sqr.y].magnet_value,curr_board[sqr.x][sqr.y].value)
        print("pairSqr : ",pairSqr.x,pairSqr.y,curr_board[pairSqr.x][pairSqr.y].magnet_value,curr_board[pairSqr.x][pairSqr.y].value )



# def backTrack_Csp(board):
#     # print('csppp')
#     # print_board(board)
#     if assignment_is_done(board)==True:
#         print("assignment_is_done: ")
#         print_board(board)
#         return True

#     sqr = mrv_Heuristic(board)
#     pairSqr = get_the_pair(sqr,board)
#     print("Sqr : ",sqr.x,sqr.y,sqr.value)
#     print("pairSqr : ",pairSqr.x,pairSqr.y,pairSqr.value)
#     print(" domain fo sqr: ",sqr.domain_square)
#     print(" domain of pairsqr: ",pairSqr.domain_square)

#     ### iterate the domain : 
#     for i in range (len(sqr.domain_square)):
#     #for i in range (len(sqr.domain_square)):
#         sqr_value = board[sqr.x][sqr.y].domain_square[i]
#         curr_board = copy.deepcopy(board)

#         # sqr_copy = copy.deepcopy(sqr)
#         # pairSqr_copy =copy.deepcopy(pairSqr) 
#         if sqr_value=='+':
#             pair_value='-'
#             # curr_board[sqr.x][sqr.y].domain_square.remove(sqr_value)
#             # curr_board[pairSqr.x][pairSqr.y].domain_square.remove(pair_value)
#         elif sqr_value=='-':
#             pair_value='+'
#         elif sqr_value=='0':
#             pair_value='0'

#         curr_board[sqr.x][sqr.y].magnet_value = sqr_value  ## sqr_copy
#         curr_board[pairSqr.x][pairSqr.y].magnet_value = pair_value  ##pairSqr_copy
       
#         print_board(curr_board)
#         print("curr sgr value : ",curr_board[sqr.x][sqr.y].magnet_value )
#         print("curr pairsgr value : ",curr_board[pairSqr.x][pairSqr.y].magnet_value)

#         ## remove these values from domain
#         print("new domain fo sqr before remove : ",curr_board[sqr.x][sqr.y].domain_square)
          
#         print("new domain of pairsqr before remove before if: ",curr_board[pairSqr.x][pairSqr.y].domain_square,pairSqr.x)  
#         if curr_board[sqr.x][sqr.y].magnet_value in curr_board[sqr.x][sqr.y].domain_square:
#             print("*")
#             curr_board[sqr.x][sqr.y].domain_square.remove(sqr_value)
#             print("new domain fo sqr afterrr remove: ",curr_board[sqr.x][sqr.y].domain_square,sqr.x)
#         print("new domain of pairsqr before remove : ",curr_board[pairSqr.x][pairSqr.y].domain_square,pairSqr.x)  
#         print(" some arbittt: ",curr_board[3][3].domain_square , 3)  
#         if curr_board[pairSqr.x][pairSqr.y].magnet_value in curr_board[pairSqr.x][pairSqr.y].domain_square:
#             print("**")
#             curr_board[pairSqr.x][pairSqr.y].domain_square.remove(pair_value)
#             print("new domain of pairsqr  afterrr remove: ",curr_board[pairSqr.x][pairSqr.y].domain_square)

#         print("new domain fo sqr: ",curr_board[sqr.x][sqr.y].domain_square)
#         print("new domain of pairsqr : ",curr_board[pairSqr.x][pairSqr.y].domain_square)

#         print("Sqr : ",sqr.x,sqr.y,curr_board[sqr.x][sqr.y].magnet_value,curr_board[sqr.x][sqr.y].value)
#         print("pairSqr : ",pairSqr.x,pairSqr.y,curr_board[pairSqr.x][pairSqr.y].magnet_value,curr_board[pairSqr.x][pairSqr.y].value )