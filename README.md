# Annotating Learner Errors for Automated Feedback

This is the repository for the following research paper at AIED 2025:

> Annotating Errors in English Learners' Written Language Production: Advancing Automated Written Feedback Systems
>
> Steven Coyne, Diana Galvan-Sosa, Ryan Spring, Camélia Guerraoui, Michael Zock, Keisuke Sakaguchi and Kentaro Inui
>
> In: Artificial Intelligence in Education. AIED 2025.

## Contents

```
appendix/
- Full typology of learner errors
- Guideline document for the error annotation and feedback writing task
- Guideline document used by teachers in the feedback rating task

feedback_dataset/
- Dataset of 456 learner sentences and feedback comments described in the paper, annotated by 2 annotators in 3 batches

rating_dataset/
- Dataset of 2312 manual expert ratings for the human-written feedback and AI-generated feedback. Each example was evalated by two of a group of 4 English teachers

templates/
- Collection of 149 manually-created feedback templates used in the experiment
- Ground-truth reference templates for the "train" (batches 1 and 2) and "test" (batch 3) settings

fb_setting_outputs/
- AI-generated feedback from 5 different systems, plus human feedback for reference. Separated into "train" (batches 1 & 2) and "test" (batch 3)

reference_tags/
- Map of ground-truth EXPECT and ERRANT tags for each example, used in the feedback generation experiments

prompts.py
- The prompts used by the feedback generation systems
```

Note that while feedback was written and generated for both "train" and "test" sets, the human evaluations were only performed on the test set (i.e., batch 3).

## Citation

```bibtex
@inproceedings{coyne-2025-annotating,
title = "Annotating Errors in English Learners' Written Language Production: Advancing Automated Written Feedback Systems",
author = "Coyne, Steven
    and Galvan-Sosa, Diana
    and Spring, Ryan
    and Guerraoui, Camélia
    and Zock, Michael
    and Sakaguchi, Keisuke
    and Inui, Kentaro",
booktitle="Artificial Intelligence in Education",
year = "2025",
publisher = "Springer Nature Switzerland",
address = "Cham",
}
```
