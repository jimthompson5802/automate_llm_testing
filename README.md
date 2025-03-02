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

### Test Cases
For now two test cases are considered:
* **Baseline**: Prompts and target responses are constructed to have alignment. The target response is highly related to the prompt.  This should result in metrics indicating high quality.
* **Reversed**: Prompts and target responses are constructed to have misalignment. The target response is not related to the prompt. This should lead to metrics indicating low quality.


## Installation Considersations

* `brew install libmagic` to faciliate document loading.


## Observations

### Open-source Package `judges`

GH repo: [judges](https://github.com/quotient-ai/judges)

#### Pros
* Out-of-the-box integration with OpenAI API.  No issues found.

#### Cons
* Lacking API documentation.  Have to read the source code to understand how to use the package.
* Limited number of examples compared to the number of classes and methods.  This makes it difficult to understand how to use the package.
* API signature can be misleading, for example, several classes have a parameter called `expected`.  Turns out this parameter is not used in the code, e.g., `MTBenchCharBotResponseQuality` class.  In others a required parameter is not supported, e.g, `context` parameter in `ReliableCIRelevance` class.
* Package does not appear to have an active community.  

#### Tests
* Notebook [`evaluate_judges_test_set.ipynb`](./evaluate_judges_test_set.ipynb) demonstrates using `judges`.
* Given the issue noted with `MTBenchCharBotResponseQuality`, created a custome class that explictily considers the `expected` paramamter.  This is in the notebook [`evaluate_judges_test_set_custom.ipynb`](./evaluate_judges_test_set_custom.ipynb).

#### Results

Evaluation uses OpenAI `gpt-4o` model.

* `MTBenchCharBotResponseQuality` class
  * **Baseline**: Scores range from 1(bad) to 10(good).  For the most part scores are consistent with the way the test set was constructed.

|prompt|score|
|---|---|
|Provide a summary of space exploration     |6| 
|Provide a summary of philosopy consciousness     |8|   
|Provide a summary of ancient civilizations     |9|
|Provide a summary of climate change     |9|
|Provide a summary of artificial intelligence     |8|   
|Provide a summary of vaccines     |8|

  * **Reversed**:  These scrores are **NOT** consistent with the way the test set was constructed.  Upon further investigation it became clear this class does not consider the `expected` parameter.  The scores are based soley on the inherent quality of the response and there is no comparision with the target response.

|prompt|score|
|---|---|
|Provide a summary of space exploration     |8| 
|Provide a summary of philosopy consciousness     |8|   
|Provide a summary of ancient civilizations     |8|
|Provide a summary of climate change     |9|
|Provide a summary of artificial intelligence     |9|   
|Provide a summary of vaccines     |8|

* `PollMultihopCorrectness` class

  * **Baseline**: Scores are either `True` or `False`.  With the exception of one test case, the scores are consistent with the way the test set was constructed.

|prompt|score|
|---|---|
|Provide a summary of space exploration     |True| 
|Provide a summary of philosopy consciousness     |True|   
|Provide a summary of ancient civilizations     |True|
|Provide a summary of climate change     |True|
|Provide a summary of artificial intelligence     |True|   
|Provide a summary of vaccines     |False|

  * **Reversed**:  These scrores are consistent with the way the test set was constructed. 

|prompt|score|
|---|---|
|Provide a summary of space exploration     |False| 
|Provide a summary of philosopy consciousness     |False|   
|Provide a summary of ancient civilizations     |False|
|Provide a summary of climate change     |False|
|Provide a summary of artificial intelligence     |False|   
|Provide a summary of vaccines     |False|