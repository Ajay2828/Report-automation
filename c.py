import math

n = 61
r = 6

num_combinations = math.factorial(n) / (math.factorial(r) * math.factorial(n - r))
print(num_combinations)