import numpy as np

# Define the matrix A
A = np.array([[2, 5],
              [6, 7]])

# Define the vector B
B = np.array([100, 150])

# Solve for x
x = np.linalg.solve(A, B)

# Extract x1 and x2
x1, x2 = x

# x1, x2 = A

print(f"x1 = {x1}")
print(f"x2 = {x2}")


