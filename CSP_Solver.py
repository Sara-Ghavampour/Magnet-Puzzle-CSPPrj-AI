import math
from Board import Board
from square import *
import copy
def assignment_is_done(board):  # check termination of backtracking  # is complete
    for i in range(len(board)):  ## check if there is a variable that we didnt assign it's value
        for j in range(len(board[0])):
            if board[i][j].magnet_value==None : 
                return False
    if not satisfaction_test(board):  ## check if constraint for each row and col is satisfied
        return False
    return True 


def all_checked(board): ## check if there is a variable that we didnt assign it's value
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

def mrv_Heuristic(board): ## check if there is a variable that we didnt assign it's value
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


def check_consistency_with_neibours(board,sqr,pairSqr):  ### check if there is an unconsistency such as -- or ++ in neibours
    n = len(board)
    m = len(board[0])
    x= sqr.x
    y=sqr.y
    x_pair= pairSqr.x
    y_pair=pairSqr.y
    if sqr.magnet_value!=None :   ## check consistency_with_neibours for sqr
        if x-1>=0 and board[x-1][y].magnet_value == sqr.magnet_value : # left neibour
            return False
        elif x+1<n and board[x+1][y].magnet_value == sqr.magnet_value : # right neibour
            return False
        elif y-1>=0 and board[x][y-1].magnet_value == sqr.magnet_value :# downside neibour 
            return False
        elif y+1<n and board[x][y+1].magnet_value == sqr.magnet_value : # upside neibour 
            return False
    if pairSqr.magnet_value!=None : ## check consistency_with_neibours for pairSqr
        if x_pair-1>=0 and board[x_pair-1][y_pair].magnet_value == pairSqr.magnet_value :
            return False
        elif x_pair+1<n and board[x_pair+1][y_pair].magnet_value == pairSqr.magnet_value :
            return False
        elif y_pair-1>=0 and board[x_pair][y_pair-1].magnet_value == pairSqr.magnet_value :
            return False
        elif y_pair+1<n and board[x_pair][y_pair+1].magnet_value == pairSqr.magnet_value :
            return False    


    
    return True


def get_neibours(board,sqr):  ### get all neibours for a sqr
    n = len(board)
    m = len(board[0])
    x= sqr.x
    y=sqr.y
    neibours=[]

    if sqr.magnet_value!=None :   # if we assigned to this variable(sqr) -> now we can return the neibours for upcoming uses in forward check
        if x-1>=0 : # left neibour
            neibours.append(board[x-1][y])
        elif x+1<n : # right neibour
            neibours.append(board[x+1][y])
        elif y-1>=0 :# downside neibour 
            neibours.append(board[x][y-1])
        elif y+1<n : # upside neibour 
            neibours.append(board[x][y+1])

    return neibours



def is_consistent(board,sqr,pairSqr):  ## check satisfactilon for rows and cols and ++ or -- in neibours
    n = len(board)  ## rows
    m = len(board[0])  ## cols
    p_row =0
    n_row =0
    p_col=0
    n_col=0
    all_row_sqrs_assigned=True    # a flag that checks if a row is complete and there is an unconsistency returns false
    all_col_sqrs_assigned=True    # a flag that checks if a col is complete and there is an unconsistency returns false

    if check_consistency_with_neibours(board,sqr,pairSqr) == False :  ### check if there is an unconsistency such as -- or ++ in neibours
        return False

    for i in range(0,n):  ## rows ## check satisfaction for rows 
        p_row=0
        n_row=0
        all_row_sqrs_assigned=True
        for j in range(0,m):
            if board[i][j].magnet_value=='+': p_row+=1
            if board[i][j].magnet_value=='-': n_row+=1
            if board[i][j].magnet_value==None :   ## row is not assigned completely
                all_row_sqrs_assigned=False
        if(all_row_sqrs_assigned): # ## row is assigned completely:
            if p_row != Board.row_positive_bound[i] or n_row != Board.row_negative_bound[i]:
                return False
        else:  ## row is not assigned completely
            if p_row>Board.row_positive_bound[i] or n_row >Board.row_negative_bound[i]:
                return False


    for j in range(0,m): ## cols ## check satisfaction for cols
        p_col=0
        n_col=0
        all_col_sqrs_assigned=True
        for i in range (0,n):
            if board[i][j].magnet_value=='+': p_col+=1
            if board[i][j].magnet_value=='-': n_col+=1
            if board[i][j].magnet_value==None: all_col_sqrs_assigned = False ## col is not assigned completely

        if(all_col_sqrs_assigned):## col is assigned completely
            if p_col != Board.col_positive_bound[j] or n_col != Board.col_negative_bound[j]:
                return False
        else: ## col is not assigned completely
            if p_col> Board.col_positive_bound[j] or n_col> Board.col_negative_bound[j]:
                return False

    return True 



def satisfaction_test(board):  ## check if constraint for each row and col is satisfied
    n = len(board)  ## rows
    m = len(board[0])  ## cols
    p_row =0
    n_row =0
    p_col=0
    n_col=0
   

    for i in range(0,n):  ## rows
        p_row=0
        n_row=0
        for j in range(0,m):
            if board[i][j].magnet_value=='+': p_row+=1
            if board[i][j].magnet_value=='-': n_row+=1
        if p_row!=Board.row_positive_bound[i] or n_row !=Board.row_negative_bound[i]:
            return False


    for j in range(0,m): ## cols
        p_col=0
        n_col=0
        for i in range (0,n):
            if board[i][j].magnet_value=='+': p_col+=1
            if board[i][j].magnet_value=='-': n_col+=1

        if p_col!= Board.col_positive_bound[j] or n_col!= Board.col_negative_bound[j]:
            return False

    return True         

def forward_check(board,sqr,pairSqr):
    sqr_neighbors=get_neibours(board,sqr)
    pairSqr_neighbors=get_neibours(board,pairSqr)
    #print("sqr_neighbors , pairSqr_neighbors: ",sqr_neighbors,pairSqr_neighbors)
    for i in range(0,len(sqr_neighbors)): # FC for sqr 
        if sqr.magnet_value in sqr_neighbors[i].domain_square:
            sqr_neighbors[i].domain_square.remove(sqr.magnet_value)
    for i in range(0,len(pairSqr_neighbors)): # FC for pairSqr 
        if pairSqr.magnet_value in pairSqr_neighbors[i].domain_square:
            pairSqr_neighbors[i].domain_square.remove(pairSqr.magnet_value)    

def lcv(board,sqr,pairSqr): # for each var choose value that leads to least constraints fer neihbors  # returns a sorted array as domain
    sqr_magnet_value=sqr.magnet_value
    pairSqr_magnet_value = None
    constraints_list=[]
    value_constraints_list=[]  ## each value for each constraint
    constraint = 0
    sqr_neighbors = get_neibours(board,sqr)
    pairSqr_neighbors = get_neibours(board,pairSqr)
    for value in sqr.domain_square:
        if value == '+':
            pairSqr_magnet_value='-'

        elif value == '-':
            pairSqr_magnet_value='+'

        else:      # '0' 
            pairSqr_magnet_value='0'  

        constraint=0 

        for neighbor in sqr_neighbors:  ## check if sqr neighbors have cinstraint with pair sqr value
            if pairSqr_magnet_value in neighbor.domain_square:
                constraint+=1
                if len(neighbor.domain_square) ==1 :  ## if a neighbor has one value in domain and it leads to constraint so its a really bad move
                    constraint +=1000
        for neighbor in pairSqr_neighbors:## check if pair sqr neighbors have cinstraint with  sqr value
            if sqr_magnet_value in neighbor.domain_square:
                constraint+=1
            if len(neighbor.domain_square)==1 :  ## if a neighbor has one value in domain and it leads to constraint so its a really bad move
                    constraint +=1000

        constraints_list.append(constraint)
        value_constraints_list.append(value)
    new_sqr_domain=[] # sorted domain based on lcv
    for i in range(0,len(constraints_list)-1): # sort constraints_list and value_constraints_list
        for j in range(i+1,len(constraints_list)):
            if constraints_list[i]>constraints_list[j]: ## j is less
                t = constraints_list[i]
                constraints_list[i] = constraints_list[j]
                constraints_list[j]=t

                t = value_constraints_list[i]
                value_constraints_list[i] = value_constraints_list[j]
                value_constraints_list[j]=t

    # after sort we have to fill new_sqr_domain
    for i in range(0,len(value_constraints_list)):
        if value_constraints_list[i] not in new_sqr_domain: # if value is not added yet
            new_sqr_domain.append(value_constraints_list[i])
        if len(new_sqr_domain)==3: break # stop after filling    new_sqr_domain becuase length is 3 : + - 0 

    sqr.domain_square = new_sqr_domain  ## assign new domain to sqr
   # print("sqr.domain_square in lcv : ",sqr.domain_square)






def backTrack_Csp(board):
    
    if assignment_is_done(board)==True:   # check termination of backtracking  # is complete
        print("assignment_is_done: ")
        print_board(board)
        return True
    if all_checked(board): ## check if there is a variable that we didnt assign it's value
        return False
    sqr = mrv_Heuristic(board)   # select a variable via mrv heuristic
          
    pairSqr = get_the_pair(sqr,board)   # get the pair for this var
    if not is_consistent(board,sqr,pairSqr): ## check satisfaction for rows and cols and ++ or -- in neibours
        return False
    # print("Sqr : ",sqr.x,sqr.y,sqr.value)
    # print("pairSqr : ",pairSqr.x,pairSqr.y,pairSqr.value)
    # print(" domain fo sqr: ",sqr.domain_square)
    # print(" domain of pairsqr: ",pairSqr.domain_square)

    ### iterate the domain : 
    lcv(board,sqr,pairSqr) ## change domain by lcv heuristic to choose lcv
    for i in range (len(sqr.domain_square)):
    
        sqr_value = board[sqr.x][sqr.y].domain_square[i]
        curr_board = copy.deepcopy(board)


        if sqr_value=='+':
            pair_value='-'
           
        elif sqr_value=='-':
            pair_value='+'
        elif sqr_value=='0':
            pair_value='0'

        curr_board[sqr.x][sqr.y].magnet_value = sqr_value  ## sqr_copy
        curr_board[pairSqr.x][pairSqr.y].magnet_value = pair_value  ##pairSqr_copy
       
        # print_board(curr_board)
        # print("curr sgr value : ",curr_board[sqr.x][sqr.y].magnet_value )
        # print("curr pairsgr value : ",curr_board[pairSqr.x][pairSqr.y].magnet_value)

        ## remove these values from domain
       
        if curr_board[sqr.x][sqr.y].magnet_value in curr_board[sqr.x][sqr.y].domain_square:
            
            curr_board[sqr.x][sqr.y].domain_square.remove(curr_board[sqr.x][sqr.y].magnet_value)
        
        if curr_board[pairSqr.x][pairSqr.y].magnet_value in curr_board[pairSqr.x][pairSqr.y].domain_square:
           
            curr_board[pairSqr.x][pairSqr.y].domain_square.remove(curr_board[pairSqr.x][pairSqr.y].magnet_value )
        #if is_consistent(curr_board,curr_board[pairSqr.x][pairSqr.y],curr_board[pairSqr.x][pairSqr.y]):
        forward_check(curr_board,curr_board[sqr.x][sqr.y],curr_board[pairSqr.x][pairSqr.y])
        if(backTrack_Csp(curr_board)):
            return True
    return False

