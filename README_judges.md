## Open-source Package `judges`

GH repo: [judges](https://github.com/quotient-ai/judges)

### Pros
* Out-of-the-box integration with OpenAI API.  No issues found.

### Cons
* Lacking API documentation.  Have to read the source code to understand how to use the package.
* Limited number of examples compared to the number of classes and methods.  This makes it difficult to understand how to use the package.
* API signature can be misleading, for example, several classes have a parameter called `expected`.  Turns out this parameter is not used in the code, e.g., `MTBenchCharBotResponseQuality` class.  In others a required parameter is not supported, e.g, `context` parameter in `ReliableCIRelevance` class.
* Package does not appear to have an active community.  

### Tests
* Notebook [`evaluate_judges_test_set.ipynb`](./evaluate_judges_test_set.ipynb) (commit: 6e57563) demonstrates using `judges`.
* Given the issue noted with `MTBenchCharBotResponseQuality`, created a custom class that explictily considers the `expected` paramamter.  This is in the notebook [`evaluate_judges_test_set_custom.ipynb`](./evaluate_judges_test_set_custom.ipynb) (commit: 6e57563).

### Results

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