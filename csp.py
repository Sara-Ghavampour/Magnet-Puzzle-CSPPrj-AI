import math
from state import *
import copy
def backtrack(board, domain):
    n = len(board)
    m = len(board[0])
    
    if (finished(board)):
        print_state(board)
        return True
    
    ## if all variables checked and didnt satisfy the constraints
    if (checked_cells(board, n, m) == n*m):
        return False

    # print_state(board)
    
    ## choose a variable based on lenght of domain (MRV)
    
    x1, y1 = mrv(board, domain)  
    x2, y2 = get_other_pole(x1, y1)
    
    if ((x1 == 0 and y1 == 0) or (x1 == n/2 and y1 == m/2)):
        contradiction, ac3_domain = ac3(board, domain)
        domain = ac3_domain
        
        if contradiction:
            return False
    
    ## check constraints of problem
    if (not is_safe(board, x1, y1, x2, y2)):
        return False
    
    ## (LCV)
    lcv_domain = lcv(domain, x1, y1)
    
    ## loop on domain
    for d in lcv_domain:
        new_board = copy.deepcopy(board)
        new_domain = copy.deepcopy(domain)
        
        if (d == '+'):
            d_prime = '-'
        elif (d == '-'):
            d_prime = '+'
        elif (d == ' '):
            d_prime = ' '
        
        ## assign value to board
        new_board[x1][y1] = d
        new_board[x2][y2] = d_prime
        
        ## forward check
        flag, nd = forward_check(new_board, new_domain, x1, y1, x2, y2)
        
        if (flag):
            if (backtrack(new_board, nd)):
                return True
    
    
    return False


def is_safe(board, x1, y1, x2, y2):
    
    n = len(board)
    m = len(board[0])
    
    neighbors = get_neighbors(x1, y1)
    
    for pair in neighbors:
        if(pair[2] == '1'):
            if (board[pair[0]][pair[1]]==board[x1][y1]):
                return False
        else:
            if (board[pair[0]][pair[1]]==board[x2][y2]):
                return False
    
    #check plus and minus counts constraint
    
    for i in range (0, n):
        p_count = 0
        m_count = 0
        all_init = True
        for j in range (0, m):
            if (board[i][j] != '+' and board[i][j] != '-' and board[i][j] != ' '):
                all_init = False
            if (board[i][j]=='+'):
                p_count+=1
            elif (board[i][j]=='-'):
                m_count+=1
        
        if (all_init):
            # print('all init')
            if(p_count != State.bound_y[0][i] or m_count != State.bound_y[1][i]):
                return False
        else:
            if(p_count > State.bound_y[0][i] or m_count > State.bound_y[1][i]):
                return False
        
    for i in range (0, m):
        p_count = 0
        m_count = 0
        all_init = True

        for j in range (0, n):
            if (board[j][i] != '+' and board[j][i] != '-' and board[j][i] != ' '):
                all_init = False
            if (board[j][i]=='+'):
                p_count+=1
            elif (board[j][i]=='-'):
                m_count+=1
        if (all_init):
            # print('all init')
            if(p_count != State.bound_x[0][i] or m_count != State.bound_x[1][i]):
                return False
        else:
            if(p_count > State.bound_x[0][i] or m_count > State.bound_x[1][i]):
                return False     
    
    
    
    return True
        
def ac3(board, domain):
    queue = []
    
    n = len(board)
    m = len(board[0])
    
    k = 1
    for i in range(0, n):
        for j in range(0, m):
            if (State.board[i][j] == k):
                if (board[i][j] != '+' and board[i][j] != '-' and board[i][j] != ' '):
                    queue.append([i, j])
                k+=1
    
    
    contradiction = False
    
    while (len(queue) > 0 and not contradiction):
        v = queue.pop(0)
        neighbors = get_neighbors(v[0], v[1])
        
        for n in neighbors:
            x = n[0]
            y = n[1]
            if (board[x][y] != '+' and board[x][y] != '-' and board[x][y] != ' '):
                flag, new_domain = revise(v, n, domain)
                domain = new_domain
                if flag:
                    if len(new_domain)==0:
                        contradiction = False
                        break
                    queue.append([x, y])
    
    return contradiction, domain

def revise(x, neighbor, domain):
    x1, y1 = x
    x2, y2 = get_other_pole(x1, y1)
    
    x_n1, y_n1, mode = neighbor
    x_n2, y_n2 = get_other_pole(x_n1, y_n1)
    
    removed = False
    if mode == '1':
        for v in domain[x_n1][y_n1]:
            found = False
        
            if (v == '+'):
                d = '-'
            elif (v == '-'):
                d = '+'
            else:
                d = v
                
            if d in domain[x1][y1]:found = True

            if (not found and v != d):
                if v in domain[x_n1][y_n1]:domain[x_n1][y_n1].remove(v)
                if d in domain[x_n2][y_n2]:domain[x_n2][y_n2].remove(d)

                removed = True
                
    if mode == '2':
        for v in domain[x_n1][y_n1]:
            found = False
        
            if (v == '+'):
                d = '-'
            elif (v == '-'):
                d = '+'
            else:
                d = v
                
            if d in domain[x2][y2]:found = True
                    
            if (not found and v != d):
                if v in domain[x_n1][y_n1]:domain[x_n1][y_n1].remove(v)
                if d in domain[x_n2][y_n2]:domain[x_n2][y_n2].remove(d)

                removed = True
    
    return removed, domain

                
    
def print_state(board):
    n = len(board)
    m = len(board[0])
    print('-------------------')
    for i in range(0, n):
        for j in range(0, m):
            print(board[i][j], end=' ')
        print()
     
    print('-------------------')
     
def forward_check(board, domain, x1, y1, x2, y2):
    n = len(board)
    m = len(board[0])
    
    neighbors = get_neighbors(x1, y1)
    
        
    value_1 = board[x1][y1]
    value_2 = board[x2][y2]
    for pair in neighbors:
        mode = pair[2]
        if (value_1 =='+' or value_1 =='-'):
            if (mode == '1'):
                if (board[pair[0]][pair[1]] == value_1):
                    return False, None
                elif (board[pair[0]][pair[1]] != ' ' and board[pair[0]][pair[1]] != value_2):
                    x, y = get_other_pole(pair[0], pair[1])
                    if (x != None and y != None):                        
                        if value_2 in domain[x][y]:domain[x][y].remove(value_2)
                        if value_1 in domain[pair[0]][pair[1]]:domain[pair[0]][pair[1]].remove(value_1)
                        if len(domain[x][y])==0:
                            return False, None
                        if len(domain[pair[0]][pair[1]])==0:
                            return False, None
                        
            elif (mode == '2'):
                if (board[pair[0]][pair[1]] == value_2):
                    return False, None
                elif (board[pair[0]][pair[1]] != ' ' and board[pair[0]][pair[1]] != value_1):
                    x, y = get_other_pole(pair[0], pair[1])
                    if (x != None and y != None):                        
                        if value_1 in domain[x][y]:domain[x][y].remove(value_1)
                        if value_2 in domain[pair[0]][pair[1]]:domain[pair[0]][pair[1]].remove(value_2)
                        if len(domain[x][y])==0:
                            return False, None
                        if len(domain[pair[0]][pair[1]])==0:
                            return False, None
                        
    
        
    return True, domain

def get_neighbors(x1, y1):
    x2, y2 = get_other_pole(x1, y1)
    n = len(State.board)
    m = len(State.board[0])
    
    neighbors = [[x1-1, y1, '1'], [x1+1, y1, '1'], [x1, y1-1, '1'], [x1, y1+1, '1'], 
                 [x2-1, y2, '2'], [x2+1, y2, '2'], [x2, y2-1, '2'], [x2, y2+1, '2']]
    
    for i in range(0, 8):
        x = neighbors[i][0]
        y = neighbors[i][1]
        
        if (x < 0 or x >= n or y < 0 or y >= m or (x == x1 and y == y1) or (x == x2 and y == y2)):
            neighbors[i] = None
            
    res = []
    for n in neighbors:
        if (n != None):
            res.append(n)
            
    return res
            

def get_other_pole(x, y):
    num = State.board[x][y]
    n = len(State.board)
    m = len(State.board[0])
    if (y-1 >= 0 and State.board[x][y-1] == num):
        return x, y-1
    elif (y+1 < m and State.board[x][y+1] == num):
        return x, y+1
    elif (x-1 >= 0 and State.board[x-1][y] == num):
        return x-1, y
    elif (x+1 < n and State.board[x+1][y] == num):
        return x+1, y
    
    return None, None


def checked_cells(board, n, m):
    count = 0
    for i in range(0, n):
        for j in range(0, m):
            if (board[i][j] == '+' or board[i][j] == '-' or board[i][j] == ' '):
                count+=1
    
    return count

    
def finished(board):
    
    n = len(board)
    m = len(board[0])
    
    for i in range (0, n):
        plus_count = 0
        minus_count = 0
        for j in range(0, m):
            if (board[i][j] == '+'):
                plus_count += 1
            elif (board[i][j] == '-'):
                minus_count += 1
        if ((plus_count != State.bound_y[0][i]) or
            (minus_count != State.bound_y[1][i])):
            return False
        
    for i in range (0, m):
        plus_count = 0
        minus_count = 0
        for j in range(0, n):
            if (board[j][i] == '+'):
                plus_count += 1
            elif (board[j][i] == '-'):
                minus_count += 1
        if ((plus_count != State.bound_x[0][i]) or
            (minus_count != State.bound_x[1][i])):
            return False
                
    return True

def mrv(board, domain):
    min = math.inf
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            size = len(domain[i][j])
            if (board[i][j] != '+' and 
                    board[i][j] != '-' and 
                    board[i][j] != ' '):
                if (size < min):
                    min = size
                    return i, j
                
                
def lcv(m_domain, x1, y1):
    domain = copy.deepcopy(m_domain)
    neighbors = get_neighbors(x1, y1)
    constraint_counts = []
    for d in domain:
        if (d == '+'):
            d_prime = '-'
        elif (d == '-'):
            d_prime = '+'
        else :
            d_prime = ' '
        constraint_count = 0
        for n in neighbors:
            x = n[0]
            y = n[1]
            mode = n[2]
            
            if mode == '1':
                if d_prime in domain[x][y]:
                    constraint_count+=1
                    if len(domain[x][y])==1:
                        constraint_count+=10
            elif mode == '2':
                if d in domain[x][y]:
                    constraint_count+=1
                    if len(domain[x][y])==1:
                        constraint_count+=10
        
        constraint_counts.append(constraint_count)
        
    for i in range(0, len(constraint_counts)-1):
        for j in range (i+1, len(constraint_counts)):
            if (constraint_counts[i] > constraint_counts[j]):
                temp = constraint_counts[j]
                constraint_counts[j] = constraint_counts[i]
                constraint_counts[i] = temp
                
                temp = domain[x1][y1][j]
                domain[x1][y1][j] = domain[x1][y1][i]
                domain[x1][y1][i] = temp
    
    
    return domain[x1][y1]    
            
    
                