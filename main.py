import pandas as pd


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
    print(numbers)

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

    
    print(grid)
    
    possibilities = {}

    for l in range(nbr_sub_grids):
        for c in range(nbr_sub_grids):
            print(f'\n{(l,c)}:')
            print(sub_grids.loc[l,c])
            possible_values = numbers.difference({i for i in sub_grids.loc[l,c].stack().values})
            for sl in sub_grids.loc[l,c].index.values.tolist():
                for sc in sub_grids.loc[l,c].columns.values.tolist():
                    if sub_grids.loc[l,c].loc[sl,sc] == 0:
                        new = {(sl,sc): possible_values.difference(set(grid.loc[sl,:].values)).difference(set(grid.loc[:,sc].values))}
                        possibilities.update(new)
                        print(f'{new}')
            print()
    
    print(possibilities)
    
            


    



