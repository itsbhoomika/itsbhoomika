# Link to colab notebook with outputs:
- https://colab.research.google.com/drive/1wijB5DZEg8d_zAywuaVC-Wf2pvXdIS4v#scrollTo=owBsntoEwMUD

# Predictive Modeling for Text-Rich Data Using a Supervised Learning Feedback Loop with LLMs

## Research Project – University of Illinois Urbana-Champaign

### Objective
Clinical trial datasets contain large amounts of unstructured text describing study design, interventions, eligibility criteria, and outcomes. Many of the factors influencing trial success are embedded in these narrative descriptions and are difficult to incorporate into traditional predictive models.

In this project at the Statistics Dept of UIUC, we investigated whether large language models (LLMs) can automatically extract structured attributes from clinical trial descriptions and convert them into predictive features. Our goal was to build a scalable pipeline that transforms unstructured clinical trial text into structured variables that can be used in predictive modeling.

### Data
We used publicly available cancer data from ClinicalTrials.gov, which contains detailed information about clinical studies. The raw dataset contains 115,480 clinical trials and 33 columns spanning trial status, dates, enrollment, sponsor details, interventions, and descriptive text fields. This mix of structured and unstructured data makes it well-suited for predictive modeling with both classical ML features and LLM-derived features.

Each trial record includes structured metadata and narrative descriptions such as:
1. study summary and detailed description
2. intervention information
3. eligibility criteria
4. disease conditions and study phase

After filtering ambiguous statuses, our dataset contained:
- 79% completed (success)
- 21% terminated/withdrawn/suspended (failure)
  
The task was to predict whether a trial would be completed based on its description and characteristics.

### Approach
We built an end-to-end pipeline that converts trial descriptions into structured predictors.

🔁 Pipeline Overview
<img width="1536" height="1024" alt="image_llm" src="https://github.com/user-attachments/assets/1137698e-c588-451e-a1c3-c672558651de" />

### Conclusion
Based on initial model results, we refined the LLM prompt to extract more granular features related to:
- study design characteristics
- intervention mechanisms
- patient eligibility constraints
- operational trial logistics
  
The refined prompt produced more consistent and informative structured features, demonstrating how model feedback can improve LLM-based feature extraction pipelines. This project demonstrates an end-to-end pipeline for transforming unstructured clinical trial descriptions into structured features using a large language model. The extracted features can be integrated with traditional machine learning models to support predictive analysis. The workflow illustrates how LLMs can assist in feature engineering for complex text-heavy datasets and how model feedback can guide iterative refinement of extracted variables.


