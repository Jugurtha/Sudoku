import pandas as pd
import itertools as it
import os
import sys



def calculate_possible_values(sub_grids : pd.DataFrame, nbr_sub_grids) -> dict:
    possibilities = {}
    for l in range(nbr_sub_grids):
        for c in range(nbr_sub_grids):
            #print(f'\n{(l,c)}:')
            #print(sub_grids.loc[l,c])
            possible_values = numbers.difference({i for i in sub_grids.loc[l,c].stack().values})
            for sl in sub_grids.loc[l,c].index.values.tolist():
                for sc in sub_grids.loc[l,c].columns.values.tolist():
                    if sub_grids.loc[l,c].loc[sl,sc] == 0:
                        new = {(sl,sc): possible_values.difference(set(grid.loc[sl,:].values)).difference(set(grid.loc[:,sc].values))}
                        possibilities.update(new)
                        #print(f'{new}')
            #print()
    return possibilities


def nbr_unique_possibility(possibilities : dict) -> int:
    nbr = 0
    for possible_values in possibilities.values():
        if len(possible_values) == 1:
            nbr += 1
    return nbr



def cells_with_nbr_possibilities(possibilities : dict, nbr: int) -> int:
    count = 0
    keys = dict()
    for cell, possible_values in possibilities.items():
        if len(possible_values) == nbr:
            keys.update({cell: possible_values})
            count += 1
    return (count, keys)


if __name__ == '__main__':
    grid_width = 9
    sub_grid_width = grid_width // 3
    nbr_sub_grids = grid_width // sub_grid_width

    grid = pd.DataFrame({
        i:[0]*grid_width for i in range(grid_width)
    }, index=[i for i in range(grid_width)])

    sub_grids = pd.DataFrame({
        i: [ grid.loc[j*sub_grid_width : j*sub_grid_width+sub_grid_width-1,i*sub_grid_width:i*sub_grid_width+sub_grid_width-1] for j in range(sub_grid_width) ] for i in range(nbr_sub_grids)
    }, index=[i for i in range(grid_width // sub_grid_width)])
    
    numbers = {*range(1,10)}#{*range(1,10)}
    #print(numbers)

    grid.loc[0,0] = 2
    grid.loc[1,2] = 9
    grid.loc[2,4] = 7
    grid.loc[2,5] = 4
    grid.loc[0,6] = 8
    grid.loc[1,7] = 6
    grid.loc[1,8] = 5
    grid.loc[2,7] = 9
    grid.loc[3,1] = 3
    grid.loc[5,0] = 6
    grid.loc[5,1] = 2
    grid.loc[3,3] = 7
    grid.loc[3,4] = 6
    grid.loc[4,4] = 8
    grid.loc[5,4] = 5
    grid.loc[5,5] = 9
    grid.loc[3,7] = 5
    grid.loc[3,8] = 1
    grid.loc[5,7] = 3
    grid.loc[6,1] = 7
    grid.loc[7,0] = 1
    grid.loc[7,1] = 6
    grid.loc[8,2] = 8
    grid.loc[6,3] = 1
    grid.loc[6,4] = 9
    grid.loc[7,6] = 5
    grid.loc[8,8] = 4

    pid = -1
    print('\nGrid : \n',grid,'\n')
    sys.stdout.flush()
    possibilities = calculate_possible_values(sub_grids, nbr_sub_grids)
    nbr_uniques = nbr_unique_possibility(possibilities)
    #print(f'Number of unique possibility cells : {nbr_uniques}')
    
    while nbr_uniques> 0:
        for cell, possible_values in possibilities.items():
            if len(possible_values) == 1:
                #print(cell,possible_values)
                grid.loc[cell[0],cell[1]]= possible_values.pop()
        #print(grid)
        possibilities = calculate_possible_values(sub_grids, nbr_sub_grids)
        nbr_uniques = nbr_unique_possibility(possibilities)
        #print(f'Number of unique possibility cells : {nbr_uniques}')
        if nbr_uniques == 0 and cells_with_nbr_possibilities(possibilities,2)[0] != 0:
            sub_grid_zeros = {}
            for l in range(nbr_sub_grids):
                for c in range(nbr_sub_grids):
                    s = sub_grids.loc[l,c].stack().value_counts(sort=True)
                    if 0 in s:
                        new = {(l,c): s[0]}
                        sub_grid_zeros.update(new)

            current_sub_grid = sorted(sub_grid_zeros, key=sub_grid_zeros.get)[0]
            current_cells = set(it.product(sub_grids.loc[current_sub_grid[0],current_sub_grid[1]].index.values,sub_grids.loc[current_sub_grid[0],current_sub_grid[1]].columns.values))
            t = {i: len(possibilities[i]) if i in possibilities else 10 for i in current_cells}
            #print(t)
            #print(t[sorted(t, key=t.get)[0]])
            smallest_nbr_possibility = t[sorted(t, key=t.get)[0]]
            if smallest_nbr_possibility == 0:
                break
            possible_current_cells = list(current_cells.intersection(set(cells_with_nbr_possibilities(possibilities,smallest_nbr_possibility)[1].keys())))
            
            #print('possible_current_cells : ',possible_current_cells)
            if not possible_current_cells:
                break
            current_cell = possible_current_cells[0]
            
            for c in range(len(possible_current_cells)):
                current_cell = possible_current_cells[c]
                pid = os.fork()
                if pid == 0: #if in child process
                    break

            if pid != 0: #if in paarent process
                break
            
            #print(current_cell,possibilities[current_cell])
            chosen_possibility = list(possibilities[current_cell])[0]
            if len(possibilities[current_cell]) != 1:
                for c in range(len(list(possibilities[current_cell]))):
                    chosen_possibility = list(possibilities[current_cell])[c]
                    pid = os.fork()
                    if pid == 0: #if in child process
                        break

            if pid != 0: #if in paarent process
                break
                
            grid.loc[current_cell[0],current_cell[1]]= chosen_possibility
            #print(grid)
            possibilities = calculate_possible_values(sub_grids, nbr_sub_grids)
            nbr_uniques = nbr_unique_possibility(possibilities)
            #print(f'Number of unique possibility cells : {nbr_uniques}')
            
    if pid != 0:
        os.wait()

    if not possibilities:
        print('\nSolution : \n',grid,'\n')
        sys.stdout.flush()
            





            
    '''
    #print('\n----------------\ncells_with_nbr_possibilities(possibilities,2) = ',cells_with_nbr_possibilities(possibilities,2))
    print('Number of zeros: ',grid.stack().value_counts()[0])
    sub_grid_zeros = {}
    for l in range(nbr_sub_grids):
        for c in range(nbr_sub_grids):
            s = sub_grids.loc[l,c].stack().value_counts(sort=True)
            #new = {(l,c): s[0] if 0 in s else 0}
            if 0 in s:
                new = {(l,c): s[0]}
                sub_grid_zeros.update(new)
                #print(f'number of 0 in {new}')

    #print(sorted(sub_grid_zeros, key=sub_grid_zeros.get))
    current_sub_grid = sorted(sub_grid_zeros, key=sub_grid_zeros.get)[0]
    #print(sub_grids.loc[current_sub_grid[0],current_sub_grid[1]].index.values)
    #print(sub_grids.loc[current_sub_grid[0],current_sub_grid[1]].columns.values)
    current_cells = set(it.product(sub_grids.loc[current_sub_grid[0],current_sub_grid[1]].index.values,sub_grids.loc[current_sub_grid[0],current_sub_grid[1]].columns.values))
    print(current_cells)
    print(list(current_cells.intersection(set(cells_with_nbr_possibilities(possibilities,2)[1].keys())))[0])
    '''
    


            


    



