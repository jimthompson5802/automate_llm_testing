## Open-source Package `judges`

GH repo: [judges](https://github.com/quotient-ai/judges)

### Pros
* Out-of-the-box integration with OpenAI API.  No issues found.

### Cons
* Lacking API documentation.  Have to read the source code to understand how to use the package.
* Limited number of examples compared to the number of classes and methods.  This makes it difficult to understand how to use the package.
* API signature can be misleading, for example, several classes have a parameter called `expected`.  Turns out this parameter is not used in the code, e.g., `MTBenchCharBotResponseQuality` class.  In others a required parameter is not supported, e.g, `context` parameter in `ReliableCIRelevance` class.
* Package does not appear to have an active community.  

### Phase 1 Test Cases
* Notebook [`evaluate_judges_test_set.ipynb`](./evaluate_judges_test_set.ipynb) (commit: 6e57563) demonstrates using `judges`.
* Given the issue noted with `MTBenchCharBotResponseQuality`, created a custom class that explictily considers the `expected` paramamter.  This is in the notebook [`evaluate_judges_test_set_custom.ipynb`](./evaluate_judges_test_set_custom.ipynb) (commit: 6e57563).

### Results

Evaluation uses OpenAI `gpt-4o` model.

#### Out-of-the-box classes

`MTBenchCharBotResponseQuality` class

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

`PollMultihopCorrectness` class

* **Baseline**: Scores are either `True` or `False`.  In the case of the `False` test case, the reason given is the response was incomplete when compared to the target response.  A manual inspection of the response confirms this.  Given this then the scores are consistent with the way the test set was constructed and how responses were returned.

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


#### Custom class

As a result of the deficiency noted with `MTBenchCharBotResponseQuality`, which does not use the ``expected`` parameter, I created a custom class`SemanticAlignmentJudge` to make use of the `expected` parameter.  This custom class generates a score from 1 to 10, similar to `MTBenchmarkCharBotResponseQuality`.

`SemanticAlignmentJudge` class

* **Baseline**: The scores good alignment with the target response.  The reason given for the score of "8" for the vaccine prompt is information is missing from the retrieved text compared to the target response.  A manual inspection of the response confirms this.

|prompt|score|
|---|---|
|Provide a summary of space exploration     |10| 
|Provide a summary of philosopy consciousness     |10|   
|Provide a summary of ancient civilizations     |10|
|Provide a summary of climate change     |10|
|Provide a summary of artificial intelligence     |10|   
|Provide a summary of vaccines     |8|

* **Reversed**:  The expected scores should have been numeric.  With the exception of one test case, which scored "2", the others scored "True".  This is not the exepected behavior.  One possible reason is that "1" is a "truthy" value in Python.  It is possible that a component of `judges` is translating "1" to "True".  If we consder this possibility, then the scores are consistent with the way the test set was constructed.  More research is needed to confirm this and determine it this issue can be resolved.

|prompt|score|
|---|---|
|Provide a summary of space exploration     |True| 
|Provide a summary of philosopy consciousness     |True|   
|Provide a summary of ancient civilizations     |True|
|Provide a summary of climate change     |True|
|Provide a summary of artificial intelligence     |2|   
|Provide a summary of vaccines     |True|

### Phase 2 Test Cases

Given the issues noted with `MTBenchCharBotResponseQuality` this class was not tested in Phase 2.  Only the custom class `SemanticAlignmentJudge` and `PollMultihopCorrectness` were tested.

Notebook [`evaluate_judges_rewritten_test_set.ipynb`](./evaluate_judges_rewritten_test_set.ipynb) (commit: 3e7b61b) contains results of Phase 2 testing.

`SemanticAlignmentJudge` class

* **Baseline**: The scores good alignment with the target response.  The reason given for the score of "8" for the vaccine prompt is information is missing from the retrieved text compared to the target response.  A manual inspection of the response confirms this.

|prompt|score|
|---|---|
|Provide a summary of space exploration     |9| 
|Provide a summary of philosopy consciousness     |9|   
|Provide a summary of ancient civilizations     |9|
|Provide a summary of climate change     |9|
|Provide a summary of artificial intelligence     |9|   
|Provide a summary of vaccines     |8|

* **Reversed**:  The expected scores should have been numeric.  As in Phase 1 test, Phase 2 test scores boolean "True" values.  One possible reason is that "1" is a "truthy" value in Python.  It is possible that a component of `judges` is translating "1" to "True".  If we consder this possibility, then the scores should be "1" and are consistent with the way the test set was constructed, indicate poor quality of the response.  More research is needed to confirm this and determine it this issue can be resolved.

|prompt|score|
|---|---|
|Provide a summary of space exploration     |True| 
|Provide a summary of philosopy consciousness     |True|   
|Provide a summary of ancient civilizations     |True|
|Provide a summary of climate change     |True|
|Provide a summary of artificial intelligence     |True|   
|Provide a summary of vaccines     |True|

`PollMultihopCorrectness` class

* **Baseline**: Scores are either `True` or `False`. Given this then the scores are consistent with the way the test set was constructed, indicating semantic alignment with the target response.

|prompt|score|
|---|---|
|Provide a summary of space exploration     |True| 
|Provide a summary of philosopy consciousness     |True|   
|Provide a summary of ancient civilizations     |True|
|Provide a summary of climate change     |True|
|Provide a summary of artificial intelligence     |True|   
|Provide a summary of vaccines     |True|

* **Reversed**:  These scrores are consistent with the way the test set was constructed, poor semantic alignment with the target response.

|prompt|score|
|---|---|
|Provide a summary of space exploration     |False| 
|Provide a summary of philosopy consciousness     |False|   
|Provide a summary of ancient civilizations     |False|
|Provide a summary of climate change     |False|
|Provide a summary of artificial intelligence     |False|   
|Provide a summary of vaccines     |False|
