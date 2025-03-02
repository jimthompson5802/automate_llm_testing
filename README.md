# Testbed for Automated Testing of LLM Ouputs

## UNDER CONSTRUCTION




## Installation Considersations

* `brew install libmagic` to faciliate document loading.

* Package version conflicts could be a problem.  This is a result of piecemeal installing packages.  Should start fresh.  For example, the `openai` package is used by `judges` and `langchain-openai`.  The `langchain-openai` package requires a version of `openai` that is incompatible with the version required by `judges`.  This can be resolved by installing the required version of `openai` for `judges` before installing `langchain-openai`.  The following is an example of the output from the installation of the `judges` package.
```text
(venv) Mac:jim llm_testing[526]$ pip install judges
Collecting judges
  Downloading judges-0.0.6-py3-none-any.whl.metadata (33 kB)
Collecting openai==1.57.4 (from judges)
  Downloading openai-1.57.4-py3-none-any.whl.metadata (24 kB)
Requirement already satisfied: anyio<5,>=3.5.0 in ./venv/lib/python3.12/site-packages (from openai==1.57.4->judges) (4.8.0)
Requirement already satisfied: distro<2,>=1.7.0 in ./venv/lib/python3.12/site-packages (from openai==1.57.4->judges) (1.9.0)
Requirement already satisfied: httpx<1,>=0.23.0 in ./venv/lib/python3.12/site-packages (from openai==1.57.4->judges) (0.28.1)
Requirement already satisfied: jiter<1,>=0.4.0 in ./venv/lib/python3.12/site-packages (from openai==1.57.4->judges) (0.8.2)
Requirement already satisfied: pydantic<3,>=1.9.0 in ./venv/lib/python3.12/site-packages (from openai==1.57.4->judges) (2.10.6)
Requirement already satisfied: sniffio in ./venv/lib/python3.12/site-packages (from openai==1.57.4->judges) (1.3.1)
Requirement already satisfied: tqdm>4 in ./venv/lib/python3.12/site-packages (from openai==1.57.4->judges) (4.67.1)
Requirement already satisfied: typing-extensions<5,>=4.11 in ./venv/lib/python3.12/site-packages (from openai==1.57.4->judges) (4.12.2)
Requirement already satisfied: idna>=2.8 in ./venv/lib/python3.12/site-packages (from anyio<5,>=3.5.0->openai==1.57.4->judges) (3.10)
Requirement already satisfied: certifi in ./venv/lib/python3.12/site-packages (from httpx<1,>=0.23.0->openai==1.57.4->judges) (2025.1.31)
Requirement already satisfied: httpcore==1.* in ./venv/lib/python3.12/site-packages (from httpx<1,>=0.23.0->openai==1.57.4->judges) (1.0.7)
Requirement already satisfied: h11<0.15,>=0.13 in ./venv/lib/python3.12/site-packages (from httpcore==1.*->httpx<1,>=0.23.0->openai==1.57.4->judges) (0.14.0)
Requirement already satisfied: annotated-types>=0.6.0 in ./venv/lib/python3.12/site-packages (from pydantic<3,>=1.9.0->openai==1.57.4->judges) (0.7.0)
Requirement already satisfied: pydantic-core==2.27.2 in ./venv/lib/python3.12/site-packages (from pydantic<3,>=1.9.0->openai==1.57.4->judges) (2.27.2)
Downloading judges-0.0.6-py3-none-any.whl (54 kB)
Downloading openai-1.57.4-py3-none-any.whl (390 kB)
Installing collected packages: openai, judges
  Attempting uninstall: openai
    Found existing installation: openai 1.65.1
    Uninstalling openai-1.65.1:
      Successfully uninstalled openai-1.65.1
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
langchain-openai 0.3.7 requires openai<2.0.0,>=1.58.1, but you have openai 1.57.4 which is incompatible.
Successfully installed judges-0.0.6 openai-1.57.4

```

## Observations

### Open-source Package `judges`

#### Pros
* Out-of-the-box integration with OpenAI API.  No issues found.

#### Cons
* Lacking API documentation.  Have to read the source code to understand how to use the package.
* Limited number of examples compared to the number of classes and methods.  This makes it difficult to understand how to use the package.
* API signature can be misleading, for example, several classes have a parameter called `expected`.  Turns out this parameter is not used in the code, e.g., `MTBenchCharBotResponseQuality` class.  In others a required parameter is not supported, e.g, `context` parameter in `ReliableCIRelevance` class.
* Package does not appear to have an active community.  

#### Tests
* Notebook [`evaluate_judges_test_set.ipynb`](./evaluate_judges_test_set.ipynb) demonstrates using `judges`.