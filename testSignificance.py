import sys
import numpy as np
from scipy import stats
import pandas as pd

# additional packages
import statsmodels.api as sm



### Normality Check
def normality_check(data_A, data_B, name, alpha):

    if(name=="Shapiro-Wilk"):
        # Shapiro-Wilk: Perform the Shapiro-Wilk test for normality.
        shapiro_results = stats.shapiro(data_A-data_B)
        return shapiro_results[1]

    elif(name=="Anderson-Darling"):
        # Anderson-Darling: Anderson-Darling test for data coming from a particular distribution
        anderson_results = stats.anderson(data_A-data_B, 'norm')
        sig_level = 2
        if(alpha <= 0.01):
            sig_level = 4
        elif(alpha>0.01 and alpha<=0.025):
            sig_level = 3
        elif(alpha>0.025 and alpha<=0.05):
            sig_level = 2
        elif(alpha>0.05 and alpha<=0.1):
            sig_level = 1
        else:
            sig_level = 0

        return anderson_results[1][sig_level]

    else:
        # Kolmogorov-Smirnov: Perform the Kolmogorov-Smirnov test for goodness of fit.
        ks_results = stats.kstest(data_A-data_B, 'norm')
        return ks_results[1]

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

#Permutation-randomization
#Repeat R times: randomly flip each m_i(A),m_i(B) between A and B with probability 0.5, calculate delta(A,B).
# let r be the number of times that delta(A,B)>=orig_delta(A,B)
# significance level: (r+1)/(R+1)
def rand_permutation(data_A, data_B, n, R):
    delta_orig = float(sum([ x - y for x, y in zip(data_A, data_B)]))/n
    r = 0
    for x in range(0, R):
        temp_A = data_A
        temp_B = data_B
        samples = [np.random.randint(1, 2) for i in range(n)] #which samples to swap without repetitions
        swap_ind = [i for i, val in enumerate(samples) if val == 1]
        for ind in swap_ind:
            temp_B[ind], temp_A[ind] = temp_A[ind], temp_B[ind]
        delta = float(sum([ x - y for x, y in zip(temp_A, temp_B)]))/n
        if(delta>=delta_orig):
            r = r+1
    pval = float(r+1)/(R+1)
    return pval


#Bootstrap
#Repeat R times: randomly create new samples from the data with repetitions, calculate delta(A,B).
# let r be the number of times that delta(A,B)>=orig_delta(A,B)
# significance level: (r+1)/(R+1)
def Bootstrap(data_A, data_B, n, R):
    delta_orig = float(sum([x - y for x, y in zip(data_A, data_B)])) / n
    r = 0
    for x in range(0, R):
        temp_A = []
        temp_B = []
        samples = np.random.randint(0,n,n) #which samples to swap with repetitions
        for samp in samples:
            temp_A.append(data_A[samp])
            temp_B.append(data_B[samp])
        delta = float(sum([x - y for x, y in zip(temp_A, temp_B)])) / n
        if (delta >= delta_orig):
            r = r + 1
    pval = float(r+1)/(R+1)
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


    # data_A = raw_input("Enter the results of algorithm A as list of scores ")
    # data_B = raw_input("Enter the results of algorithm B as list of scores ")
    # alpha = raw_input("Enter desirable significance level: ")

    print("Possible statistical tests: Shapiro-Wilk, Anderson-Darling, Kolmogorov-Smirnov, t-test, Wilcoxon, McNemar, Permutation, Bootstrap")
    name = raw_input("Enter name of statistical test: ")

    ### Normality Check
    if(name=="Shapiro-Wilk" or name=="Anderson-Darling" or name=="Kolmogorov-Smirnov"):
        output = normality_check(data_A, data_B, name, alpha)
        if(output <= alpha):
            answer = raw_input("The normal test is significantly positive, would you like to perform a t-test for checking significance of difference between results? (Y\N) ")
            if(answer=='Y'):
                t_results = stats.ttest_rel(data_A, data_B)
                if(t_results[1]<=alpha):
                    print("Test result is significant with p-value: {}".format(t_results[1]))
                    return
                else:
                    print("Test result is not significant with p-value: {}".format(t_results[1]))
                    return
            else:
                answer2 = raw_input("Would you like to perform a different test (permutation or bootstrap)? If so enter name of test, otherwise type 'N' ")
                if(answer2=='N'):
                    print("p-value of normality check is: {}", output)
                    return
                else:
                    name = answer2
        else:
            answer = raw_input("The normal test is not significant, would you like to perform a non-parametric test for checking significance of difference between results? (Y\N) ")
            if (answer == 'Y'):
                answer2 = raw_input("Which test (Permutation or Bootstrap)? ")
                name = answer2
            else:
                print("p-value of normality check is: {}", output)
                return

    ### Statistical tests

    # Paired Student's t-test: Calculate the T-test on TWO RELATED samples of scores, a and b.
    elif(name=="t-test"):
        t_results = stats.ttest_rel(data_A, data_B)
        if (t_results[1] <= alpha):
            print("Test result is significant with p-value: {}".format(t_results[1]))
            return
        else:
            print("Test result is not significant with p-value: {}".format(t_results[1]))
            return

    # Wilcoxon: Calculate the Wilcoxon signed-rank test.
    elif(name=="Wilcoxon"):
        wilcoxon_results = stats.wilcoxon(data_A, data_B)
        if (wilcoxon_results[1] <= alpha):
            print("Test result is significant with p-value: {}".format(wilcoxon_results[1]))
            return
        else:
            print("Test result is not significant with p-value: {}".format(wilcoxon_results[1]))
            return

    elif(name=="McNemar"):
        print("This test requires the results to be binary : A[1, 0, 0, 1, ...], B[1, 0, 1, 1, ...] for success or failure on the i-th example.")
        f_obs = calculateContingency(data_A, data_B, len(data_A))
        mcnemar_results = sm.stats.contingency_tables.mcnemar(f_obs, True)
        if (mcnemar_results.pvalue <= alpha):
            print("Test result is significant with p-value: {}".format(mcnemar_results.pvalue))
            return
        else:
            print("Test result is not significant with p-value: {}".format(mcnemar_results.pvalue))
            return

    elif(name=="Permutation"):
        R = max(10, 000, len(data_A) * (1 / float(alpha)))
        pval = rand_permutation(data_A, data_B, len(data_A), R)
        if (pval <= alpha):
            print("Test result is significant with p-value: {}".format(pval))
            return
        else:
            print("Test result is not significant with p-value: {}".format(pval))
            return


    elif(name=="Bootstrap"):
        R = max(10, 000, len(data_A) * (1 / float(alpha)))
        pval = Bootstrap(data_A, data_B, len(data_A), R)
        if (pval <= alpha):
            print("Test result is significant with p-value: {}".format(pval))
            return
        else:
            print("Test result is not significant with p-value: {}".format(pval))
            return

    else:
        print("Invalid name of statistical test")
        sys.exit(1)





if __name__ == "__main__":
    main()











