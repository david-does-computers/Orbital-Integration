from scipy.stats import beta
k = 44
n = 51
alpha = 0.05
p_u, p_o = beta.ppf([alpha/2, 1 - alpha/2], [k, k + 1], [n - k + 1, n - k])

print(p_u, p_o)