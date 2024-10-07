import sys
import chardet
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  
    result = chardet.detect(raw_data)
    return result['encoding']

def zipf_function(rank, a, b, C):
    return C / (rank + b) ** a

input_file = sys.argv[1]
encoding = detect_encoding(input_file)

ranking = []
frequency = []

with open(input_file, newline='', encoding=encoding) as infile:
    rank = 1
    for line in infile:
        parts = line.split()  
        if len(parts) == 2:
            count, word = parts
            ranking.append(int(rank))
            frequency.append(int(count))
            rank += 1

# Fitting the curve using curve_fit
popt, pcov = curve_fit(zipf_function, ranking, frequency, p0=[1.0, 0.0, 1000])

# Optimal parameters for a, b, and C
a_opt, b_opt, C_opt = popt
print(f'Parameter a: {a_opt}')
print(f'Parameter b: {b_opt}')
print(f'Constant C: {C_opt}')

# Generate a smooth range of rank values for plotting the fitted curve
ranking_sorted = np.sort(ranking)
ranking_range = np.linspace(min(ranking_sorted), max(ranking_sorted), 500)

# Compute the fitted frequency using the smooth range of ranks
fitted_frequency = zipf_function(ranking_range, a_opt, b_opt, C_opt)

# Plotting observed points and fitted curve
plt.figure(figsize=(8,6))
plt.plot(ranking, frequency, 'o', label='Observed points')  # Observed data points
plt.plot(ranking_range, fitted_frequency, '-', label='Zipf adaptation', color='red')  # Fitted curve with smooth ranks
plt.title("Adaptation of Zipf's Law")
plt.xlabel('Rank')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()

# Log-log plot
plt.figure(figsize=(8,6))
plt.loglog(ranking, frequency, 'o', label='Observed points')  # Log-log scale for observed points
plt.loglog(ranking_range, fitted_frequency, '-', label='Zipf adaptation', color='red')  # Fitted curve in log-log scale
plt.title("Adaptation of Zipf's Law (Log-Log)")
plt.xlabel('Rank')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()
