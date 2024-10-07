import sys
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

def heaps_function(words, k, beta):
    return k*(words**beta)

tokens=[]
types=[]
# Index/file to inspect
for i in range(1,6):
    file = sys.argv[i]
    f=open(file)
    tokens_i=0
    types_i=0
    for line in f:
            parts = line.split()  
            if len(parts) == 2:
                count, word = parts
                tokens_i+=int(count)
                types_i+=1
    tokens.append(tokens_i) 
    types.append(types_i)     

#print(f"Total number of the words (N): {tokens}")
#print(f"Number of distinct words (d): {types}")     

#Fitting
popt, pcov = curve_fit(heaps_function, tokens, types, p0=[1.0, 0.5])

# Optimal parameters for k, and beta
k_opt, beta_opt = popt
print(f'Parameter k: {k_opt}')
print(f'Parameter beta: {beta_opt}')

fitted_distinct_words = heaps_function(tokens, k_opt, beta_opt)

plt.figure(figsize=(8,6))
plt.plot(tokens, types, 'o', label='Observed points')
plt.plot(tokens, fitted_distinct_words, label='Heaps adaptation', color='red')
plt.title("Adaptation of the Heaps'Law")
plt.xlabel('Tokes')
plt.ylabel('Types')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,6))
plt.loglog(tokens, types, 'o', label='Observed points')
plt.loglog(tokens, fitted_distinct_words, label='Heaps adaptation', color='red')
plt.title("Adaptation of the Heaps'Law")
plt.xlabel('Tokens (log)')
plt.ylabel('Types (log)')
plt.legend()
plt.grid(True)
plt.show()

