import numpy as np

# Original array
arr = np.array([['1', '2', '3', '4'],
                ['4', '5', '6', '7'],
                ['7', '8', '9', '9'],
                ['4', '5', '6', '7']])

# Get the shape of the original array
num_rows, num_cols = arr.shape

# Create index arrays for the first row and column
row_indexes = np.arange(num_rows).reshape(-1, 1)
col_indexes = np.arange(num_cols).reshape(1, -1)

# Create an empty array with the desired shape
result = np.empty((num_rows + 1, num_cols + 1), dtype=str)

# Assign the index values to the first row and column
result[0, 1:] = col_indexes[0, :]
result[1:, 0] = row_indexes[:, 0]

# Assign the original array values to the remaining cells
result[1:, 1:] = arr

# Print the updated array
print(result)

## 
#
import numpy as np
arr = np.array([['X', '2', '3', '.', '1'],
                ['.', '.', '.', '.', '.'],
                ['7', '.', '9', '9', '.'],
                ['.', '.', '6', '.', '1'],
                ['2', '.', '5', '6', '.']])

# indices = np.argwhere(arr != '.')
indices = np.argwhere(np.logical_and(arr != 'X', arr != '.'))




## Test for checking common tuples in list
#
arr1 = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
arr2 = [[4, 5], [5, 6], [6, 7], [7, 8], [8, 9]]

# Convert the lists to sets
set1 = set(map(tuple, arr1))
set2 = set(map(tuple, arr2))

# Find the common items
common_items = set1.intersection(set2)

# Get the count of common items
count = len(common_items)

print(count)  # Output: 2

## Test for counting how many zeros
# 
import numpy as np
arr = np.array([['X', '2', '3', '.', '1'],
                ['.', '.', '.', '.', '.'],
                ['7', '.', '9', '9', '.'],
                ['.', '.', '6', '.', '1'],
                ['2', '.', '5', '6', '.']])
np.count_nonzero(arr == "0")