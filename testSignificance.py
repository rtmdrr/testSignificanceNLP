import sys
import numpy as np
from scipy import stats
import statsmodels.api as sm



### Normality Check
# Shapiro-Wilk: Perform the Shapiro-Wilk test for normality.
# stats.shapiro(DATA)

# Anderson-Darling: Anderson-Darling test for data coming from a particular distribution
# stats.anderson(x[, dist])

# Kolmogorov-Smirnov: Perform the Kolmogorov-Smirnov test for goodness of fit.
# stats.kstest(rvs, cdf[, args, N, alternative, mode])

### Parametric tests
# Paired Student's t-test: Calculate the T-test on TWO RELATED samples of scores, a and b.
# stats.ttest_rel(a, b[, axis, nan_policy])

### A-Parametric tests

# Wilcoxon: Calculate the Wilcoxon signed-rank test.
# stats.wilcoxon(x[, y, zero_method, correction])
# Compute the Wilcoxon rank-sum statistic for two samples.
# stats.ranksums(x, y)

#McNemar?
# sm.stats.contingency_tables.mcnemar(table, exact=True, correction=True)[source]
#Cochren's Q?

#Permutation-randomization
#Repeat R times: randomly flip each m_i(A),m_i(B) between A and B with probability 0.5, calculate delta(A,B).
# let r be the number of times that delta(A,B)>=orig_delta(A,B)
# significance level: (r+1)/(R+1)

## decide on R as a function of the test set size


#Bootstrap


def main():
    data_A = []
    data_B = []
    n = 0
    condition = True
    while condition:
        data_A = raw_input("Upload a list of scores according to the results of algorithm A ")
        data_B = raw_input("Upload a list of scores according to the results of algorithm B ")
        n = len(data_A)
        alpha = raw_input("Enter significance level: ")
        print("Possible statistical tests: Shapiro-Wilk, Anderson-Darling, Kolmogorov-Smirnov, t-test, Wilcoxon, McNemar, Permutation, Bootstrap")
        test = raw_input("Enter name of statistical test: ")
        condition = (n!=len(data_B))


