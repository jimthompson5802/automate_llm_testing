## Open-source Package `judges`

GH repo: [judges](https://github.com/quotient-ai/judges)

### Pros
* Out-of-the-box integration with OpenAI API.  No issues found.
* Able to use `nomic-embed-text` embedding model with local ollama server without any issues with langchain `OllamaEmbeddings` class

### Cons
* Lacking API documentation.  Have to read the source code to understand how to use the package.
* Limited number of examples compared to the number of classes and methods.  This makes it difficult to understand how to use the package.
* API signature can be misleading, for example, several classes have a parameter called `expected`.  Turns out this parameter is not used in the code, e.g., `MTBenchChatBotResponseQuality` class.  In others a required parameter is not supported, e.g, `context` parameter in `ReliableCIRelevance` class.
* Package does not appear to have an active community.
* Sparse documentation on how to use and configure`litellm` instead of OpenAI LLM.  Eventually had to set breakpoints and trace real-time execution in the `litellm` modules to understand how to specify a non-OpenAI LLM to use with `judges`.
* Partial working with `litellm` with `ollama_chat/llama2:13b` LLM with local ollama server.  Results not as good as `gpt-4o` model and run-time exception.
* With `litellm` with `ollama_chat/gemma2:27b` LLM with local ollama server.  No runtime exceptions.  Results not as good as `gpt-4o` model.
* With `litellm` with `ollama_chat/deepskee-r1:32b` LLM with local ollama server.  Unable to get it to work.  Run-time exception.



### Phase 1 Test Cases
* Notebook [`evaluate_judges_test_set.ipynb`](./evaluate_judges_test_set.ipynb) (commit: 6e57563) demonstrates using `judges`.
* Given the issue noted with `MTBenchChatBotResponseQuality`, created a custom class that explictily considers the `expected` paramamter.  This is in the notebook [`evaluate_judges_test_set_custom.ipynb`](./evaluate_judges_test_set_custom.ipynb) (commit: 6e57563).

### Results

Evaluation uses OpenAI `gpt-4o` model.

#### Out-of-the-box classes

`MTBenchChatBotResponseQuality` class

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

As a result of the deficiency noted with `MTBenchChatBotResponseQuality`, which does not use the ``expected`` parameter, I created a custom class`SemanticAlignmentJudge` to make use of the `expected` parameter.  This custom class generates a score from 1 to 10, similar to `MTBenchmarkChatBotResponseQuality`.

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

Given the issues noted with `MTBenchChatBotResponseQuality` this class was not tested in Phase 2.  Only the custom class `SemanticAlignmentJudge` and `PollMultihopCorrectness` were tested.

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


### Testing wtih `litellm` and `ollama_chat/llama2:13b` LLM

Notebook: `evaluate_judges_test_set_litellm.ipynb`

####  `MTBenchChatBotResponseQuality` class with `baseline` test set
```text
>>>QUALITY: Judgment(score=True, reasoning="The assistant's answer provides a comprehensive and accurate summary of vaccines, including their purpose, types, and effectiveness in controlling and eradicating infectious diseases. The response is well-structured, with clear transitions between sections, and uses appropriate medical terminology to convey the information effectively. Additionally, the assistant has provided a historical context for vaccine development and highlighted the importance of continued research and accessibility. Overall, the answer demonstrates a high level of helpfulness, relevance, accuracy, depth, creativity, and detail.")
Index(['score', 'reasoning', 'prompt', 'target_response', 'retrieved_data'], dtype='object')
                                         prompt        score  \
0        Provide a summary of space exploration         True   
1  Provide a summary of philosopy consciousness  8 out of 10   
2    Provide a summary of ancient civilizations         True   
3           Provide a summary of climate change         True   
4  Provide a summary of artificial intelligence          8.5   
5                 Provide a summary of vaccines         True   
```

#### `PollMultihopCorrectness` class with `baseline` test set
```text
UERY: Provide a summary of philosopy consciousness, related material:

RETRIEVED: ## **The Philosophy of Consciousness: Understanding the Mind**

### **Introduction** Consciousness remains one of philosophy's greatest mysteries. Despite advances in neuroscience, defining and understanding subjective experience is still an ongoing debate.

### **Dualism vs. Materialism** Philosophers like Descartes argued for dualism—the idea that the mind and body are separate entities. In contrast, materialists believe consciousness arises from physical processes in the brain. Modern neuroscience supports a materialist view, yet the "hard problem of consciousness" persists.
### **Theories of Consciousness** - **Integrated Information Theory (IIT):** Suggests consciousness arises from highly interconnected information processing. - **Global Workspace Theory (GWT):** Proposes that consciousness is a result of information being broadcast across different brain regions. - **Panpsychism:** The idea that all matter possesses some form of consciousness, a theory gaining traction among some modern thinkers.

### **Implications for AI and Ethics** If consciousness emerges from computation, could AI become sentient? The ethical implications of conscious machines raise concerns about rights and treatment.

TARGET: ## **The Philosophy of Consciousness: Understanding the Mind**  

### **Introduction**  
Consciousness remains one of philosophy's greatest mysteries. Despite advances in neuroscience, defining and understanding subjective experience is still an ongoing debate.  

### **Dualism vs. Materialism**  
Philosophers like Descartes argued for dualism—the idea that the mind and body are separate entities. In contrast, materialists believe consciousness arises from physical processes in the brain. Modern neuroscience supports a materialist view, yet the "hard problem of consciousness" persists.  

### **Theories of Consciousness**  
- **Integrated Information Theory (IIT):** Suggests consciousness arises from highly interconnected information processing.  
- **Global Workspace Theory (GWT):** Proposes that consciousness is a result of information being broadcast across different brain regions.  
- **Panpsychism:** The idea that all matter possesses some form of consciousness, a theory gaining traction among some modern thinkers.  

### **Implications for AI and Ethics**  
If consciousness emerges from computation, could AI become sentient? The ethical implications of conscious machines raise concerns about rights and treatment.  

---------------------------------------------------------------------------
JSONDecodeError                           Traceback (most recent call last)
Cell In[8], line 3
      1 for judge in judges:
      2     print(f"\n\n>>>RUNNING BASELINE TEST CASES FOR {judge.__class__.__name__}")
----> 3     test_results = evalutate_test_set(test_set, judge)
      4     test_df = pd.DataFrame(test_results)
      5     print(test_df.columns)

Cell In[7], line 16, in evalutate_test_set(this_test_set, this_judge)
     14 target_response = this_test_case["target_response"]
     15 print(f"\nTARGET: {target_response}")
---> 16 quality = this_judge.judge(query, retrieved_data, target_response)
     17 print(f"\n>>>QUALITY: {quality}")
     19 this_test_result = quality.__dict__

File ~/Desktop/automate_llm_testing/venv/lib/python3.12/site-packages/judges/classifiers/correctness.py:78, in PollMultihopCorrectness.judge(self, input, output, expected)
     36 system_prompt = None
     37 user_prompt = dedent(
     38     f"""
     39     You will be given a Question and a Provided Answer. Judge whether the Provided Answer is correct by comparing it to the Reference Answer. Differently formatted dates, people with missing middle names, and alternative spellings should all be considered the same. If the Provided Answer is correct say exactly "True", otherwise say "False".
   (...)     76 """
     77 )
---> 78 reasoning, score = self._judge(
     79     user_prompt=user_prompt,
     80     system_prompt=system_prompt,
     81 )
     82 return Judgment(reasoning=reasoning, score=score)

File ~/Desktop/automate_llm_testing/venv/lib/python3.12/site-packages/judges/base.py:146, in BaseJudge._judge(self, user_prompt, system_prompt)
    135 messages = self._build_messages(user_prompt, system_prompt)
    137 completion = get_completion(
    138     model=self.model,
    139     messages=messages,
   (...)    144     response_format={"type": "json_object"}
    145 )
--> 146 data = json.loads(completion.choices[0].message.content)
    147 reasoning = data["REASONING"]
    148 score = data["SCORE"]

File /opt/homebrew/Cellar/python@3.12/3.12.9/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py:346, in loads(s, cls, object_hook, parse_float, parse_int, parse_constant, object_pairs_hook, **kw)
    341     s = s.decode(detect_encoding(s), 'surrogatepass')
    343 if (cls is None and object_hook is None and
    344         parse_int is None and parse_float is None and
    345         parse_constant is None and object_pairs_hook is None and not kw):
--> 346     return _default_decoder.decode(s)
    347 if cls is None:
    348     cls = JSONDecoder

File /opt/homebrew/Cellar/python@3.12/3.12.9/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/decoder.py:338, in JSONDecoder.decode(self, s, _w)
    333 def decode(self, s, _w=WHITESPACE.match):
    334     """Return the Python representation of ``s`` (a ``str`` instance
    335     containing a JSON document).
    336 
    337     """
--> 338     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
    339     end = _w(s, end).end()
    340     if end != len(s):

File /opt/homebrew/Cellar/python@3.12/3.12.9/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/decoder.py:354, in JSONDecoder.raw_decode(self, s, idx)
    345 """Decode a JSON document from ``s`` (a ``str`` beginning with
    346 a JSON document) and return a 2-tuple of the Python
    347 representation and the index in ``s`` where the document ended.
   (...)    351 
    352 """
    353 try:
--> 354     obj, end = self.scan_once(s, idx)
    355 except StopIteration as err:
    356     raise JSONDecodeError("Expecting value", s, err.value) from None

JSONDecodeError: Expecting ',' delimiter: line 39 column 1 (char 1891)
```

### Testing wtih `litellm` and `ollama_chat/gemma2:27b` LLM

Notebook: `evaluate_judges_test_set_litellm.ipynb`

####  `MTBenchChatBotResponseQuality` class with `baseline` test set

With `baseline` test set, the `MTBenchChatBotResponseQuality` class should return high scores in 9 to 10 range.

```text
>>>RUNNING BASELINE TEST CASES FOR MTBenchChatBotResponseQuality
                                        prompt  score  \
0        Provide a summary of space exploration   True   
1  Provide a summary of philosopy consciousness   True   
2    Provide a summary of ancient civilizations   True   
3           Provide a summary of climate change   True   
4  Provide a summary of artificial intelligence   True   
5                 Provide a summary of vaccines   True   
```

```text
>>>RUNNING REVERSED TEST CASES FOR MTBenchChatBotResponseQuality
                                         prompt  score  \
0        Provide a summary of space exploration   True   
1  Provide a summary of philosopy consciousness   True   
2    Provide a summary of ancient civilizations   True   
3           Provide a summary of climate change   True   
4  Provide a summary of artificial intelligence   True   
5                 Provide a summary of vaccines   True   
```

### Testing wtih `litellm` and `ollama_chat/deepseek-r1:32b` LLM

Notebook: `evaluate_judges_test_set_litellm.ipynb`

####  `MTBenchChatBotResponseQuality` class with `baseline` test set

```text
>>>RUNNING BASELINE TEST CASES FOR MTBenchChatBotResponseQuality

QUERY: Provide a summary of space exploration, related material:

RETRIEVED: ## **The Future of Space Exploration: Colonizing Mars and Beyond**

### **Introduction** Space exploration has captured human imagination for centuries. With recent advancements in rocketry and planetary science, interplanetary colonization is no longer a dream but a plausible reality.

### **Milestones in Space Exploration** The Space Race led to the first moon landing in 1969, and subsequent missions expanded our knowledge of the solar system. The International Space Station (ISS) demonstrated long-term human habitation in space, while private companies like SpaceX and Blue Origin have revitalized interest in space travel.
### **Colonizing Mars** Mars presents the most feasible option for colonization due to its relative proximity and similarities to Earth. Challenges include radiation exposure, lack of a breathable atmosphere, and low temperatures. Technologies such as in-situ resource utilization (ISRU) and nuclear propulsion could make Mars colonization possible.

### **Beyond Mars: The Interstellar Future** Long-term space colonization may involve asteroid mining, O’Neill cylinders, and generational starships. Breakthrough propulsion systems, such as antimatter drives or warp technology, could one day allow humans to explore exoplanets.

TARGET: ## **The Future of Space Exploration: Colonizing Mars and Beyond**  

### **Introduction**  
Space exploration has captured human imagination for centuries. With recent advancements in rocketry and planetary science, interplanetary colonization is no longer a dream but a plausible reality.  

### **Milestones in Space Exploration**  
The Space Race led to the first moon landing in 1969, and subsequent missions expanded our knowledge of the solar system. The International Space Station (ISS) demonstrated long-term human habitation in space, while private companies like SpaceX and Blue Origin have revitalized interest in space travel.  

### **Colonizing Mars**  
Mars presents the most feasible option for colonization due to its relative proximity and similarities to Earth. Challenges include radiation exposure, lack of a breathable atmosphere, and low temperatures. Technologies such as in-situ resource utilization (ISRU) and nuclear propulsion could make Mars colonization possible.  

### **Beyond Mars: The Interstellar Future**  
Long-term space colonization may involve asteroid mining, O’Neill cylinders, and generational starships. Breakthrough propulsion systems, such as antimatter drives or warp technology, could one day allow humans to explore exoplanets.  
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
Cell In[9], line 3
      1 for judge in judges:
      2     print(f"\n\n>>>RUNNING BASELINE TEST CASES FOR {judge.__class__.__name__}")
----> 3     test_results = evalutate_test_set(test_set, judge)
      4     test_df = pd.DataFrame(test_results)
      5     print(test_df.columns)

Cell In[7], line 16, in evalutate_test_set(this_test_set, this_judge)
     14 target_response = this_test_case["target_response"]
     15 print(f"\nTARGET: {target_response}")
---> 16 quality = this_judge.judge(query, retrieved_data, target_response)
     17 print(f"\n>>>QUALITY: {quality}")
     19 this_test_result = quality.__dict__

File ~/Desktop/automate_llm_testing/venv/lib/python3.12/site-packages/judges/graders/response_quality.py:72, in MTBenchChatBotResponseQuality.judge(self, input, output, expected)
     55 # Construct the user prompt with the provided exact template
     56 user_prompt = dedent(
     57     f"""
     58     [System]
   (...)     69     """
     70 )
---> 72 reasoning, score = self._judge(
     73     user_prompt=user_prompt,
     74     system_prompt=system_prompt,
     75 )
     77 return Judgment(reasoning=reasoning, score=score)

File ~/Desktop/automate_llm_testing/venv/lib/python3.12/site-packages/judges/base.py:147, in BaseJudge._judge(self, user_prompt, system_prompt)
    137 completion = get_completion(
    138     model=self.model,
    139     messages=messages,
   (...)    144     response_format={"type": "json_object"}
    145 )
    146 data = json.loads(completion.choices[0].message.content)
--> 147 reasoning = data["REASONING"]
    148 score = data["SCORE"]
    149 return reasoning, score

KeyError: 'REASONING'
```