import sys
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

def heaps_function(words, k, beta):
    return k * (words ** beta)

tokens = []
types = []
# Index/file to inspect
for i in range(1, 9):
    file = sys.argv[i]
    f = open(file)
    tokens_i = 0
    types_i = 0
    for line in f:
        parts = line.split()  
        if len(parts) == 2:
            count, word = parts
            tokens_i += int(count)
            types_i += 1
    tokens.append(tokens_i) 
    types.append(types_i)     

# Fitting
popt, pcov = curve_fit(heaps_function, tokens, types, p0=[1.0, 0.5])

# Optimal parameters for k, and beta
k_opt, beta_opt = popt
print(f'Parameter k: {k_opt}')
print(f'Parameter beta: {beta_opt}')

# Create a smooth range of token values for plotting the fitted curve
tokens_sorted = np.sort(tokens)
tokens_range = np.linspace(min(tokens_sorted), max(tokens_sorted), 500)
fitted_distinct_words = heaps_function(tokens_range, k_opt, beta_opt)

# Plotting observed points and fitted curve
plt.figure(figsize=(8,6))
plt.plot(tokens, types, 'o', label='Observed points')  # Observed data points
plt.plot(tokens_range, fitted_distinct_words, '-', label='Heaps adaptation', color='red')  # Fitted curve based on smooth token values
plt.title("Adaptation of Heaps' Law")
plt.xlabel('Tokens')
plt.ylabel('Types')
plt.legend()
plt.grid(True)
plt.show()

# Log-log plot
plt.figure(figsize=(8,6))
plt.loglog(tokens, types, 'o', label='Observed points')  # Log-log scale for observed points
plt.loglog(tokens_range, fitted_distinct_words, '-', label='Heaps adaptation', color='red')  # Fitted curve in log-log scale
plt.title("Adaptation of Heaps' Law (Log-Log)")
plt.xlabel('Tokens (log)')
plt.ylabel('Types (log)')
plt.legend()
plt.grid(True)
plt.show()