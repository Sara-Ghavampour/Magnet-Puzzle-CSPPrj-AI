######### sara Ghavampour   9812762781

from square import *
from Board import *
from CSP_Solver import *
from time import time

def main():
    input_lines=open("input.txt").readlines()
    n,m=input_lines[0].split()[0],input_lines[0].split()[1]
    row_positive_bound=[int(number)for number in input_lines[1].split()]
    row_negative_bound=[int(number)for number in input_lines[2].split()]
    col_positive_bound=[int(number)for number in input_lines[3].split()]
    col_negative_bound=[int(number)for number in input_lines[4].split()]


    Board.row_positive_bound=row_positive_bound
    Board.row_negative_bound=row_negative_bound
    Board.col_positive_bound=col_positive_bound
    Board.col_negative_bound=col_negative_bound
    for i in range(5,len(input_lines)):
        row = [int(number)for number in input_lines[i].split()]
        sqr_list=[]
        for j in range(0,len(row)):
            sqr = square(i-5,j,row[j])
            sqr_list.append(sqr)

        Board.board.append(sqr_list)


    #print_board(Board.board)   


    # print("n , m : ",n, m )
    # print("row_positive_bound: ",Board.row_positive_bound)
    # print("row_negative_bound: ",Board.row_negative_bound)
    # print("col_positive_bound: ",Board.col_positive_bound)
    # print("col_negative_bound: ",Board.col_negative_bound)
    start = time()    
    backTrack_Csp(Board.board)
    end = time()
    print("time: ",end-start)


def print_board(board):
    for i in range (len(board)):
        print("row ",i ," : ")
        for j in range(len(board[0])):
            print(board[i][j].value,end=" ")
        print()    





if __name__== "__main__":
    main()






