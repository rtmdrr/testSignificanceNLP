import sys
import numpy as np
from scipy import stats




### Normality Check
# H0: data is normally distributed
def normality_check(data_A, data_B, name, alpha):

    if(name=="Shapiro-Wilk"):
        # Shapiro-Wilk: Perform the Shapiro-Wilk test for normality.
        shapiro_results = stats.shapiro([a - b for a, b in zip(data_A, data_B)])
        return shapiro_results[1]

    elif(name=="Anderson-Darling"):
        # Anderson-Darling: Anderson-Darling test for data coming from a particular distribution
        anderson_results = stats.anderson([a - b for a, b in zip(data_A, data_B)], 'norm')
        sig_level = 2
        if(float(alpha) <= 0.01):
            sig_level = 4
        elif(float(alpha)>0.01 and float(alpha)<=0.025):
            sig_level = 3
        elif(float(alpha)>0.025 and float(alpha)<=0.05):
            sig_level = 2
        elif(float(alpha)>0.05 and float(alpha)<=0.1):
            sig_level = 1
        else:
            sig_level = 0

        return anderson_results[1][sig_level]

    else:
        # Kolmogorov-Smirnov: Perform the Kolmogorov-Smirnov test for goodness of fit.
        ks_results = stats.kstest([a - b for a, b in zip(data_A, data_B)], 'norm')
        return ks_results[1]

## McNemar test
def calculateContingency(data_A, data_B, n):
    ABrr = 0
    ABrw = 0
    ABwr = 0
    ABww = 0
    for i in range(0,n):
        if(data_A[i]==1 and data_B[i]==1):
            ABrr = ABrr+1
        if (data_A[i] == 1 and data_B[i] == 0):
            ABrw = ABrw + 1
        if (data_A[i] == 0 and data_B[i] == 1):
            ABwr = ABwr + 1
        else:
            ABww = ABww + 1
    return np.array([[ABrr, ABrw], [ABwr, ABww]])

def mcNemar(table):
    statistic = float(np.abs(table[0][1]-table[1][0]))**2/(table[1][0]+table[0][1])
    pval = 1-stats.chi2.cdf(statistic,1)
    return pval


#Permutation-randomization
#Repeat R times: randomly flip each m_i(A),m_i(B) between A and B with probability 0.5, calculate delta(A,B).
# let r be the number of times that delta(A,B)<orig_delta(A,B)
# significance level: (r+1)/(R+1)
# Assume that larger value (metric) is better 
def rand_permutation(data_A, data_B, n, R):
    delta_orig = float(sum([ x - y for x, y in zip(data_A, data_B)]))/n
    r = 0
    for x in range(0, R):
        temp_A = data_A
        temp_B = data_B
        samples = [np.random.randint(1, 3) for i in xrange(n)] #which samples to swap without repetitions
        swap_ind = [i for i, val in enumerate(samples) if val == 1]
        for ind in swap_ind:
            temp_B[ind], temp_A[ind] = temp_A[ind], temp_B[ind]
        delta = float(sum([ x - y for x, y in zip(temp_A, temp_B)]))/n
        if(delta<=delta_orig):
            r = r+1
    pval = float(r+1.0)/(R+1.0)
    return pval


#Bootstrap
#Repeat R times: randomly create new samples from the data with repetitions, calculate delta(A,B).
# let r be the number of times that delta(A,B)<2*orig_delta(A,B). significance level: r/R
# This implementation follows the description in Berg-Kirkpatrick et al. (2012), 
# "An Empirical Investigation of Statistical Significance in NLP".
def Bootstrap(data_A, data_B, n, R):
    delta_orig = float(sum([x - y for x, y in zip(data_A, data_B)])) / n
    r = 0
    for x in range(0, R):
        temp_A = []
        temp_B = []
        samples = np.random.randint(0,n,n) #which samples to add to the subsample with repetitions
        for samp in samples:
            temp_A.append(data_A[samp])
            temp_B.append(data_B[samp])
        delta = float(sum([x - y for x, y in zip(temp_A, temp_B)])) / n
        if (delta > 2*delta_orig):
            r = r + 1
    pval = float(r)/(R)
    return pval




def main():
    if len(sys.argv) < 3:
        print("You did not give enough arguments\n ")
        sys.exit(1)
    filename_A = sys.argv[1]
    filename_B = sys.argv[2]
    alpha = sys.argv[3]


    with open(filename_A) as f:
        data_A = f.read().splitlines()

    with open(filename_B) as f:
        data_B = f.read().splitlines()

    data_A = list(map(float,data_A))
    data_B = list(map(float,data_B))

    print("\nPossible statistical tests: Shapiro-Wilk, Anderson-Darling, Kolmogorov-Smirnov, t-test, Wilcoxon, McNemar, Permutation, Bootstrap")
    name = raw_input("\nEnter name of statistical test: ")

    ### Normality Check
    if(name=="Shapiro-Wilk" or name=="Anderson-Darling" or name=="Kolmogorov-Smirnov"):
        output = normality_check(data_A, data_B, name, alpha)

        if(float(output)>float(alpha)):
            answer = raw_input("\nThe normal test is significant, would you like to perform a t-test for checking significance of difference between results? (Y\N) ")
            if(answer=='Y'):
                # two sided t-test
                t_results = stats.ttest_rel(data_A, data_B)
                # correct for one sided test
                pval = t_results[1]/2
                if(float(pval)<=float(alpha)):
                    print("\nTest result is significant with p-value: {}".format(pval))
                    return
                else:
                    print("\nTest result is not significant with p-value: {}".format(pval))
                    return
            else:
                answer2 = raw_input("\nWould you like to perform a different test (permutation or bootstrap)? If so enter name of test, otherwise type 'N' ")
                if(answer2=='N'):
                    print("\nbye-bye")
                    return
                else:
                    name = answer2
        else:
            answer = raw_input("\nThe normal test is not significant, would you like to perform a non-parametric test for checking significance of difference between results? (Y\N) ")
            if (answer == 'Y'):
                answer2 = raw_input("\nWhich test (Permutation or Bootstrap)? ")
                name = answer2
            else:
                print("\nbye-bye")
                return

    ### Statistical tests

    # Paired Student's t-test: Calculate the T-test on TWO RELATED samples of scores, a and b. for one sided test we multiply p-value by half
    if(name=="t-test"):
        t_results = stats.ttest_rel(data_A, data_B)
        # correct for one sided test
        pval = float(t_results[1]) / 2
        if (float(pval) <= float(alpha)):
            print("\nTest result is significant with p-value: {}".format(pval))
            return
        else:
            print("\nTest result is not significant with p-value: {}".format(pval))
            return

    # Wilcoxon: Calculate the Wilcoxon signed-rank test.
    if(name=="Wilcoxon"):
        wilcoxon_results = stats.wilcoxon(data_A, data_B)
        if (float(wilcoxon_results[1]) <= float(alpha)):
            print("\nTest result is significant with p-value: {}".format(wilcoxon_results[1]))
            return
        else:
            print("\nTest result is not significant with p-value: {}".format(wilcoxon_results[1]))
            return

    if(name=="McNemar"):
        print("\nThis test requires the results to be binary : A[1, 0, 0, 1, ...], B[1, 0, 1, 1, ...] for success or failure on the i-th example.")
        f_obs = calculateContingency(data_A, data_B, len(data_A))
        mcnemar_results = mcNemar(f_obs)
        if (float(mcnemar_results) <= float(alpha)):
            print("\nTest result is significant with p-value: {}".format(mcnemar_results))
            return
        else:
            print("\nTest result is not significant with p-value: {}".format(mcnemar_results))
            return

    if(name=="Permutation"):
        R = max(10000, int(len(data_A) * (1 / float(alpha))))
        pval = rand_permutation(data_A, data_B, len(data_A), R)
        if (float(pval) <= float(alpha)):
            print("\nTest result is significant with p-value: {}".format(pval))
            return
        else:
            print("\nTest result is not significant with p-value: {}".format(pval))
            return


    if(name=="Bootstrap"):
        R = max(10000, int(len(data_A) * (1 / float(alpha))))
        pval = Bootstrap(data_A, data_B, len(data_A), R)
        if (float(pval) <= float(alpha)):
            print("\nTest result is significant with p-value: {}".format(pval))
            return
        else:
            print("\nTest result is not significant with p-value: {}".format(pval))
            return

    else:
        print("\nInvalid name of statistical test")
        sys.exit(1)





if __name__ == "__main__":
    main()










