# Predicting Employee Promotions: Diagnosing Promotion Process Non-Conformity


## Contact

**Tanya Gampert, PHR, CAPM, MS**  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/tanya-g-b2346b228/)  
[![Email](https://img.shields.io/badge/Email-Contact-red)](mailto:tanyagampert@gmail.com)  


---

**A logistic regression analysis revealing that 98.8% of promotion decisions are disconnected from measurable performance metrics.**

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)

---

## Project Overview

This capstone project builds an interpretable, standardized logistic regression model to leverage promotion probabilities for traditional 9-box grid classification based entirely on merit-based variables. Rather than using black-box AI systems, the analysis serves as an **audit** and **diagnostic tool** that exposes disconnects between stated merit criteria and actual promotion outcomes.

### Regulatory Context
Organizations are facing increased scrutinuty related to AI-derived employment decisions.  Recent lawsuits emphasize the need for **transparent, unbiased decision algorithms**. This framework provides the documentation, objectivity, and reproducibility required for compliance with emerging AI transparency regulations.

### Research Question
*Can logistic regression identify gaps between stated merit criteria and actual promotion decisions, enabling process standardization?* 

**Answer**: Yes! Truly meritocratic organizational processes can be validated by the standardized model.  However, organizations who do not consider merit metrics in promotion decisions in practice must investigate and reengineer the promotion process itself, with the goal of either adjusting the model to mirror the real-life process, or adjusting the process to reflect the model.  Once the model and real-life promotion process are harmonized, the standardized model can then be used going forward for both talent classification and identification of process non-conformity.

---

## View the Complete Analysis
### [Technical Analysis Notebook](notebooks/analysis.ipynb) 
*Full methodology and statistical validation*


### [Capstone Presentation](presentation/capstone_presentation.pdf)
*Presentation with business recommendations*

### [Interactive Dashboard](https://9box-dashboard.streamlit.app/)
*Explore the interactive talent classification tool*

---
## Business Impact & ROI

### Immediate Benefits
- **Talent Retention**: Reduce loss of high performers overlooked by current process
- **Process Efficiency**: Replace subjective promotion meetings with data-driven discussions
- **Legal Protection**: Maintain objective documentation for promotion decisions
- **Leadership Development**: Identify succession candidates based on merit rather than politics

### Strategic Value
- **Cultural Transformation**: Shift from politics-based to performance-based advancement
- **Competitive Advantage**: Optimize talent allocation while competitors lose high performers
- **Scalable Framework**: Apply methodology across departments and role levels
- **Continuous Improvement**: Monitor and adjust promotion processes using predictive insights


---

## Key Findings
*Logistic regression successfully identified promotion process gaps with significant business implications.*

### The Merit Paradox
Performance metrics show **negative relationships** with promotion outcomes:
- Higher performance ratings → *Lower* promotion probability 
- Greater KPI achievement → *Lower* promotion probability  
- More projects delivered → *Lower* promotion probability

**Business Translation**: The current process is actively penalizing employees who meet or exceed certain merit indicators.

### Process Dysfunction Quantified
**Only 1.2% of promotions** are explained by documented merit criteria.

**The other 98.8%** involves unmeasured factors:
- Politics and favortism
- Stacked/forced ranking
- Bias
- Budget constraints
- Leadership mandates

### Model Performance: Optimized for Wide Safety Net

| Metric | Value | Executive Interpretation |
|--------|-------|----------------|
| **Recall** | 89% | Identifies 9 out of 10 promotable employees |
| **Precision** | 19% | Requires human validation but casts wide safety net |
| **Business Impact** | High | Prevents talent loss through systematic identification |

*The model prioritizes catching talent over perfect accuracy.  It's better to review extra candidates than lose high performers.*

---

## Business Application: 9-Box Talent Framework

The model outputs **promotion probability scores** that map employees to strategic talent categories:

| | **Developing** | **Effective** | **Strong Performers** |
|---|---|---|---|
| **High Potential** | Emerging Talent (106) | Development Ready (566) | **Consistent Stars** (1,621) |
| **Moderate Potential** | At Risk (503) | Solid Performers (1,599) | Core Contributors (2,482) |
| **Low Potential** | Under Performers (749) | Limited Growth (1,003) | Technical Experts (541) |

### Executive Use Cases
- **Talent Review Calibration**: Standardize leadership discussions with objective data
- **Succession Planning**: Identify and develop high-potential employees systematically  
- **Resource Allocation**: Focus development investments on merit-based criteria
- **Legal Risk Reduction**: Maintain audit trails for promotion decisions

### **Live Demo**: [Interactive Dashboard](https://9box-dashboard.streamlit.app/)

---

## Business Recommendations

Based on the analysis findings, this organization should implement:

### Process Standardization
- **Establish merit-based promotion criteria** using measurable performance metrics
- **Implement structured decision frameworks** to reduce subjective bias 
- **Enable manager access to 9-box dashboard** to review and document promotion decisions deviating from model recommendations (potential score).

### Bias Audit & Compliance
- **Annual promotion process reviews** using predictive analytics to detect drift and diagnose process issues
- **Regulatory compliance preparation** for AI transparency laws related to automated employment decisions
- **Documentation trails** supporting promotion rationale with objective data

### Talent Risk Mitigation  
- **Proactive identification** of high-potential employees at risk of being overlooked
- **Leadership pipeline development** based on performance rather than politics
- **Retention strategies** for merit-based performers undervalued by the current process

---


## Next Steps & Implementation

### For Organizations
1. **Pilot Program**: Apply framework to one department for validation
2. **Leadership Training**: Educate managers on merit-based decision criteria  
3. **System Integration**: Connect with existing internal and external systems for automated data collection
4. **Monitoring Protocol**: Establish quarterly reviews for process effectiveness

### For Further Analysis
- **Coefficient Analysis**: Investigate specific factors driving negative performance relationships
- **Longitudinal Study**: Track promotion outcomes over time to measure process improvement 
- **Cross-Industry Validation**: Test framework across different organizational contexts

---


## Academic Context

**Program**: Master of Science in Data Analytics  
**Concentration**: Decision Process Engineering  
**Institution**: Western Governors University  
**Completion**: February 2026

**Project Significance**: Integration of statistical analysis deployed as a decision support tool to enable business process improvement.  

---

## Data & Ethics

**Dataset**: Synthetically generated dataset created specifically for this promotion analysis research. All employee information is artificially generated and privacy-compliant by design.

**Methodology**: Transparent, interpretable analytics designed for organizational audit and process improvement.

**Data Source**: [Kaggle - Corporate Workforce Metrics](https://www.kaggle.com/datasets/tanyagampert/corporate-workforce-metrics) *(Created by Tanya Gampert)*

---


*Last Updated: February 2026*