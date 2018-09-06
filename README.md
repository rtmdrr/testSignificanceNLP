# testSignificanceNLP
This script implements the statistical significance tests described in [(Dror et al., 2018)](http://aclweb.org/anthology/P18-1128):

**"The Hitchhiker's Guide to Testing Statistical Significance in Natural Language Processing."** Rotem Dror, Gili Baumer, Segev Shlomov and Roi Reichart. *In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (ACL2018)*.

In the paper we focus on the setup where the performance of two algorithms, A and B, applied on a dataset X, is compared using an evaluation measure M. When making such comparison, one should check for statistical significance of the differenece in performance between the two algorithms. The currect common practice in NLP states that if the difference in results is statistically significant then one can claim superiority of one algorithm over another.

**For recomendation on which statistical test to use based on evaluation measure see** [this appendix](https://arxiv.org/pdf/1809.01448.pdf)


## Getting Started 

The script is written in Python 2.7.

### Input
Use the following command to run the script:
```
python testSignificance.py result_file_A result_file_B alpha
```
The input consists of two files with the results of applying each algorithm (A and B) on the data X and the desirable significance level (alpha). The results for each algorithm should be in the following form (the result for each sample in X separated by lines) :
```
46.1726
68.5210
51.1151
45.8590
55.2119
36.5653
37.4119
39.8117
51.7002
```
Where, for example, 46.1726 could be the accuracy of algorithm A on the first sample in dataset X. 
After this, the interactive script will ask the user to point out the statistical test to apply.

### Output
The output of the script is the p-value of the statistical test and a statement on the significance of the result.

### Example
You can use the two datasets resA.txt and resB.txt to run the following example:
```
python testSignificance.py data_A_normal.txt data_B_normal.txt 0.05

Possible statistical tests: Shapiro-Wilk, Anderson-Darling, Kolmogorov-Smirnov, t-test, Wilcoxon, McNemar

Enter name of statistical test: 
t-test

Test result is significant with p-value: 0.00487195100707

```

### Citation
If you make use of this code for research purposes, we'll appreciate citing the following:
```
@InProceedings{P18-1128,
  author = 	"Dror, Rotem
		and Baumer, Gili
		and Shlomov, Segev
		and Reichart, Roi",
  title = 	"The Hitchhiker's Guide to Testing Statistical Significance in Natural Language Processing",
  booktitle = 	"Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
  year = 	"2018",
  publisher = 	"Association for Computational Linguistics",
  pages = 	"1383--1392",
  location = 	"Melbourne, Australia",
  url = 	"http://aclweb.org/anthology/P18-1128"
}
```


## Release History
* 0.1.0 

## Contact Information
This file and the code was written by Rotem Dror. The methods are described in the above paper [(Dror et al., 2018)](http://aclweb.org/anthology/P18-1128).
For questions please write to: rtmdrr@campus.technion.ac.il


