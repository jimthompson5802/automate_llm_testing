# Testbed for Automated Testing of LLM Ouputs

## Experiment Overview

### Objective

Establish a pipeline to test various methods for automating the evaluation of generated text.  The goal is to evaluate the quality of the generated text and its semantic alignment to a reference or "target" response.  Initially, the focus will be on evaluating how metrics are computed and their ability to determine "good" vs "bad" responses.

### Experiment Setup
* Curated set of raw documents.
* Curated test set of "prompt" and "target response", i.e, correct response, pairs
* Tokenizer
* Embedding Model
* Vector Store

### Experimental Procedure
* Chunk a set of documents and place in a Vector Store.
* Using the prompts from the curated test set, retrieve the top N chunks from the Vector Store.
* Evaluate retrieved text to target response to determine if the retrieved text are semantically aligned with the target response.
* Compute overall metrics for the evaluation method.
* Repeat for different evaluation methods.

### Test Cases: Phase 1
For now two test cases are considered:
* **Baseline**: Prompts and target responses are constructed to have alignment. The target response is highly related to the prompt.  This should result in metrics indicating high quality.
* **Reversed**: Prompts and target responses are constructed to have misalignment. The target response is not related to the prompt. This should lead to metrics indicating low quality.

### Test Cases: Phase 2

In this phase, instead of target responses being verbatim content of the raw documents, the target responses will be rewritten text that is "semantically equivalent" to the raw documents.  This should test the robustness of the evaluation methods.  For this phase both **Baseline** and **Reversed** test cases will be considered.


## Observations

Click on links to see more details.

* Package [`judges`](./README_judges.md)


## Hardware and Software Setup

### Hardware
* Macbook Pro 16" (Nov 2024)
* Apple Silicon M4 Max - 16 cores
* Apple Silicon GPU - 40 cores
* 48 GB RAM


### Software
* macOS 15.3.1 (Sequoia)
* `brew install libmagic` to faciliate document loading.
* `requirements.txt` contains the necessary Python packages.
