import sys
import re
import chardet
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  
    result = chardet.detect(raw_data)
    return result['encoding']

def zipf_function(rank, a, b, C):
    return C / (rank + b)**a

input_file=sys.argv[1]
encoding = detect_encoding(input_file)
ranking=[]
frequency=[]
with open(input_file, newline='', encoding=encoding) as infile:
        rank=1
        for line in infile:
            parts = line.split()  
            if len(parts) == 2:
                count, word = parts
                ranking.append(int(rank))
                frequency.append(int(count))
                rank +=1

#Fitting
popt, pcov = curve_fit(zipf_function, ranking, frequency, p0=[1.0, 0.0, 1000])

# Optimal parameters for a, b, e C
a_opt, b_opt, C_opt = popt
print(f'Parameter a: {a_opt}')
print(f'Parameter b: {b_opt}')
print(f'Constant C: {C_opt}')

fitted_frequency = zipf_function(ranking, a_opt, b_opt, C_opt)

plt.figure(figsize=(8,6))
plt.plot(ranking, frequency, 'o', label='Observed points')
plt.plot(ranking, fitted_frequency, label='Zipf adaptation', color='red')
plt.title("Adaptation of the Zipf's Law")
plt.xlabel('Rank')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,6))
plt.loglog(ranking, frequency, 'o', label='Observed points')
plt.loglog(ranking, fitted_frequency, label='Zipf adaptation', color='red')
plt.title("Adaptation of the Zipf's Law")
plt.xlabel('Rank')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()
