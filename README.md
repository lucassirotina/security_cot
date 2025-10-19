Assessing the Reliability of Prompted LLMs for CIS Control Validation: A Reproduction Study

In an increasingly digitalized world, it is crucial for organizations to enforce
proper security against cyber threats. This paper seeks to analyze the potential
of using a large language model (LLM) as a powerful tool for security profes-
sionals. Our study extends the existing paper on enforcing and validating CIS
critical security controls (CSC) with LLM Prompting. The authors use chain-
of-thought (COT) prompting for generating measures and metrics as well as
generated knowledge prompting to support implementation steps. Their evalu-
ation results indicate that prompt engineering can effectively semi-automate the
metric and neasure creation process. In our reproduction, we apply the same
prompting strategies on a different LLM and a current version of CSC controls
(8.1) and assess its effectiveness and reliability by using LLM to evaluate the
metrics and measures against a golden dataset, as in the original paper. Due to
our limitations, however, human security analysts don’t participate in the ex-
traction process as in the original work. We evaluate the generated results using
three criteria. Our evaluation shows that the LLM reliably generates semanti-
cally faithful and technically correct metrics. The evaluation criteria semantic
similarity scores were consistently high (mean 8.03), demonstrating the model’s
ability to capture the intended meaning of safeguards. The metrics correctness
also performed strongly (mean 8.65), indicating that the generated metrics were
logically coherent and contextually appropriate. In contrast, the metric novelty
scores were low (mean 2.15), reflecting a tendency to reproduce established
practices rather than introduce new or innovative measures. Taken together,
these results highlight the potential of LLMs to accelerate the generation of
accurate and standards-aligned security metrics, while also underscoring their
limitations in providing creative or original contributions. For reproducibility,
all source code and prompts for these experiments are available in the following
repository: https://github.com/lucassirotina/security_cot
