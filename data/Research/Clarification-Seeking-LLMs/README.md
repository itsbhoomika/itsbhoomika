## Overview

All Code Files Link: https://drive.google.com/drive/u/0/folders/1oYp5PF9D24aeYMnBi1Fou9l66Bsn4MH0

This project develops and evaluates systems where LLMs identify ambiguity in questions and generate high-quality facets that explain disambiguation question-answer pairs. The research employs a three-stage training pipeline using Gemini 2.5 Flash API and Qwen 2.5 7B for facet generation with Gemini serving as an evaluation judge.

# Facet Generation for Question Disambiguation

A machine learning research project focused on improving facet generation in question disambiguation systems using large language models (LLMs).

## Research Goals

- Develop methodologies for improving facet generation in question disambiguation systems
- Train models to better understand and categorize different types of ambiguity
- Create comprehensive evaluation frameworks for assessing facet quality
- Implement iterative improvement through preference optimization

## Taxonomy Categories

The system categorizes ambiguity across three main types:

1. **Entity Reference** - Ambiguity arising from unclear entity references
2. **Underspecified Common Nouns** - Questions with vague or incomplete noun specifications
3. **Degree of an Action** - Ambiguity in the extent or intensity of actions

## Methodology

### Three-Stage Training Pipeline

#### Stage 1: Data Preparation
- Generate diverse facet candidates
- Apply backwards filtering for validation
- Ensure generated facets can explain gold standard QA pairs

#### Stage 2: Supervised Fine-Tuning
- Train on curated datasets
- Focus on taxonomy-facet alignment
- Improve ambiguity detection capabilities

#### Stage 3: Iterative Preference Optimization
- Implement Direct Preference Optimization (DPO)
- Generate multiple output hypotheses
- Learn preferences through multi-criteria scoring

### Backwards Filtering

A core validation technique that tests whether generated facets can actually explain or generate the gold standard QA pairs used for disambiguation. This provides automatic quality control by ensuring retained facets explain gold answers by design.

## Evaluation Framework

The system assesses six core quality metrics:

1. **Taxonomy Accuracy** - Correct classification of ambiguity types
2. **Facet Coverage** - Completeness of generated facets
3. **Facet-Taxonomy Alignment** - Consistency between facets and assigned categories
4. **Ambiguity Detection** - Ability to identify ambiguous questions
5. **QA Alignment Quality** - How well facets explain disambiguation QA pairs
6. **Double Validation** - Quality checks during both preparation and improvement phases

## Technical Stack

- **Primary Model**: Qwen 2.5 7B (facet generation)
- **Evaluation Judge**: Gemini
- **Programming Language**: Python
- **Data Processing**: pandas
- **Dataset Size**: ~1000 samples

### Data Structure

The dataset contains:
- Questions
- Taxonomies
- Facets
- Disambiguation questions
- QA pairs

## Key Features

- **Multi-path Hypothesis Generation**: Integration with Stargate algorithm for exploring different solution paths
- **Comprehensive Error Handling**: Retry logic and rate limiting management
- **Scalable Evaluation**: Progressive testing from small samples to full dataset
- **Privacy-Conscious**: Designed for sensitive research data management

## Current Status

- ✅ Three-stage training pipeline implemented
- ✅ Comprehensive evaluation framework developed
- ✅ Backwards filtering validation technique established
- ✅ Small-scale testing completed
- 🔄 Scaling to complete dataset in progress
- 🔄 Research proposal document in development

## Future Work

- [ ] Complete full dataset evaluation
- [ ] Implement Stargate algorithm integration
- [ ] Develop iterative DPO over multiple rounds
- [ ] Address over-application of Entity Reference category
- [ ] Explore multi-criteria preference learning
- [ ] Publish research findings

## Installation

```bash
# Clone the repository
git clone [repository-url]

# Install dependencies
pip install -r requirements.txt

# Configure API keys
# Add your API keys for Qwen and Gemini in config file
```

## Usage

```python
# Example usage for facet generation
from facet_generator import FacetGenerator

generator = FacetGenerator(model="qwen-2.5-7b")
facets = generator.generate(question="Your ambiguous question here")

# Run evaluation
from evaluator import FacetEvaluator

evaluator = FacetEvaluator(judge_model="gemini")
results = evaluator.evaluate(facets, gold_qa_pairs)
```

## Research Principles

1. **Double Validation**: Check facet quality during both initial preparation and iterative improvement
2. **Comprehensive Evaluation**: Assess multiple dimensions rather than single metrics
3. **Systematic Approach**: Test on small samples before scaling up
4. **Backwards Verification**: Use gold QA pairs as validation criteria

## Contributing

This is an academic research project conducted through UIUC. For questions or collaboration opportunities, please contact the research team.
```

## Acknowledgments

- University of Illinois, Urbana-Champaign
- Research advisor and team members
- [Add other acknowledgments]

## Contact

For questions about this research, please contact:
- itsbhoomika.r@gmail.com

---

**Note**: This repository contains sensitive research data and is intended for academic use only.
