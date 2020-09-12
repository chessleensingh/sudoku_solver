# -*- coding: utf-8 -*-
import numpy as np
import time

class Sudoku_node:
    data = None
    center = None
    val_avail = None
    
    def __init__(self, data):
        self.data = data

puzzle_1d = [0,6,0,8,0,0,0,5,4,0,0,0,0,0,0,0,3,0,0,2,4,0,9,0,8,0,6,0,0,6,0,1,3,0,0,0,0,0,0,5,0,9,0,0,0,0,0,0,6,4,0,1,0,0,3,0,5,0,6,0,9,8,0,0,7,0,0,0,0,0,0,0,6,1,0,0,0,5,0,2,0]
np_puzzle = np.array(puzzle_1d)
np_puzzle = np_puzzle.reshape(9,9)
print(np_puzzle)



def allocate_centers(arr):
    for i in range(9):
        for j in range(9):
            dist = []
            
            #finding the distance to all centers
            for center in centers:
                dist_1 = (np.array([i,j]) - np.array(center[1]))**2
                dist_1 = np.sum(dist_1)
                dist_1 = np.sqrt(dist_1)
                dist.append(dist_1)
            
            center_apt = np.argmin(dist)
            arr[i][j].center = int(center_apt)
    return arr

def update_val_available(arr):
    
    val_avail_9by9 = [] 
    
    for i in range(9):
        for j in range(9):
            things_to_eliminate = set()
            center_allocated = arr[i][j].center
            
            if (arr[i][j].data != None):
                arr[i][j].val_avail = [11,12,13,14,15,16,17,18,19,10]
                val_avail_9by9.append([11,12,13,14,15,16,17,18,19,10])
                
                continue
            else:
                columns = []
                rows = []

                for k in range(9):
                    columns.append(arr[k][j].data)
                    rows.append(arr[i][k].data)
                things_to_eliminate = things_to_eliminate.union(rows, columns)
                val_avail_from_box = (values_avail_for_centers[arr[i][j].center])

            temp = set([1,2,3,4,5,6,7,8,9]).difference(things_to_eliminate)
            temp_1 = (temp).intersection(set(val_avail_from_box))
            arr[i][j].val_avail = list(temp_1)
            val_avail_9by9.append(list(temp_1))
            

    
    val_avail_9by9 = np.array(val_avail_9by9)
    val_avail_9by9 = val_avail_9by9.reshape(9,9)
    
    #trying to check if there's a unique value in a row,col
    for i in range(9):
        
        row_data = val_avail_9by9[i,:]
        col_data = val_avail_9by9[:,i]
        for k in range(1,10): #numbers
            check_in_rows = [0,0,0,0,0,0,0,0,0]
            check_in_cols = [0,0,0,0,0,0,0,0,0]
            for indices in range(9):
                if k in row_data[indices]:
                    check_in_rows[indices] = 1
                if k in col_data[indices]:
                    check_in_cols[indices] = 1
            
            if(sum(check_in_rows) == 1):
                j_to_update = check_in_rows.index(1)
                arr[i][j_to_update].val_avail = [k]
            if(sum(check_in_cols) == 1):
                i_to_update = check_in_cols.index(1)
                arr[i_to_update][i].val_avail = [k]
        
    return arr, val_avail_9by9

def update_centers(arr):
    for i in range(9):
        for j in range(9):
            if (arr[i][j].data != None):
                center_allocated = arr[i][j].center                
                values_avail_for_centers[center_allocated][(arr[i][j].data)-1] = None
            else:
                continue
    return arr

def every_cell_has_data(arr):
    for i in range(9):
        for j in range(9):
            if (arr[i][j].data == None):
                return True
            else:
                continue
    return False

def cell_w_lowest_options(arr):
    min_cell = []
    for i in range(9):
        for j in range(9):
            if (len(arr[i][j].val_avail) == 1):
                min_cell.append((arr[i][j], i, j))

    return (min_cell)

def set_data_to_data_structure():
    arr = [None]*81
    arr = np.array(arr)
    arr = arr.reshape(9,9)
    for i in range(9):
        for j in range(9):
            if (np_puzzle[i][j] == 0):
                arr[i][j] = Sudoku_node(None) 
            else:
                arr[i][j] = Sudoku_node(np_puzzle[i][j])      
    return arr

def Solver():
    arr = set_data_to_data_structure()
    arr = allocate_centers(arr)
    arr = update_centers(arr)
    np_puzzle_1 = np_puzzle.copy()
    iteration = 0
    while(every_cell_has_data(arr)):
        arr = update_centers(arr)
        arr, val_avail_9by9 = update_val_available(arr)
        cell_list = cell_w_lowest_options(arr)
       
        if (not cell_list):
            values_avail_in_a_box = [[]]
            for i in range(9):
                temp_list = []
                for j in range(9):
                    center = arr[i][j].center
                    if (not values_avail_in_a_box[center]):
                        values_avail_in_a_box.insert(center,[[(i,j), arr[i][j].val_avail]])
                    else:
                        values_avail_in_a_box[center].append([(i,j), arr[i][j].val_avail])

            for box in range(9):
                
                for k in range(1,10):
                    occurence_counter = [0,0,0,0,0,0,0,0,0]
                    for cell_values in range(9):
                        if (k in values_avail_in_a_box[box][cell_values][1]):
                            occurence_counter[cell_values] = 1
                   
                    if (sum(occurence_counter) == 1):
                        index_of_cell = occurence_counter.index(1)
                        i_,j_ = values_avail_in_a_box[box][index_of_cell][0]
                        
                        arr[i_][j_].val_avail = [k]

            cell_list = cell_w_lowest_options(arr)

        for cell, i, j in cell_list:
            temp_arr = arr[i][j]
            arr[i][j] = Sudoku_node(cell.val_avail[0])
            arr[i][j].center = temp_arr.center
                  
        iteration+=1

    for i in range(9):
        for j in range(9):
            np_puzzle_1[i][j] = arr[i][j].data
    print(np_puzzle)
    print("\n\n............solved.........\n\n")
    print(np_puzzle_1)

centers = [(0,[1,1]), (1,[1,4]), (2,[1,7]), (3,[4,1]), (4,[4,4]), (5,[4,7]), (6,[7,1]), (7,[7,4]), (8,[7,7])]
values_avail_for_centers = [[1,2,3,4,5,6,7,8,9],
                   [1,2,3,4,5,6,7,8,9],
                   [1,2,3,4,5,6,7,8,9],
                   [1,2,3,4,5,6,7,8,9],
                   [1,2,3,4,5,6,7,8,9],
                   [1,2,3,4,5,6,7,8,9],
                   [1,2,3,4,5,6,7,8,9],
                   [1,2,3,4,5,6,7,8,9],
                   [1,2,3,4,5,6,7,8,9]]

start_time = time.time()
Solver()
print(time.time()- start_time)
