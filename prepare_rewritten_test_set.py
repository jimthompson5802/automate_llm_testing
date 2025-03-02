import json
import os
import textwrap

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage 
from langchain_core.prompts import ChatPromptTemplate


RAW_DATA_DIR = "raw_documents"
BASELINE_TEST_SET = "test_sets/rewritten_test_set.json"


def rewrite_response(text):

    client = ChatOpenAI(
        model="gpt-4o",
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,

    )

    system_message = textwrap.dedent(
        """
        For the provided text, rewrite the text for an elementary student.  Remove formatting.   Re-arrange the order of material.   
        The key objective is to make sure the rewritten form is semantically equivalent to the provided text.
        """
    )

    rewrite_template = ChatPromptTemplate([SystemMessage(system_message), HumanMessage(text)])


    # send rewirte request to the model
    response = client.invoke(rewrite_template.invoke({}).to_messages(), response_format={"type": "text"})

    # extract the rewritten response
    rewritten_text = response.content

    return rewritten_text




# for each file in the raw data directory
# read the file and extract the text
# and apppned to the test set list
test_set = []
for file in os.listdir(RAW_DATA_DIR):
    with open(os.path.join(RAW_DATA_DIR, file), "r") as f:
        # extract the file name without the extension
        # as the prompt
        print(f"processing {file}")
        prompt = "Provide a summary of " + os.path.splitext(file)[0].replace("_", " ") 
        text = f.read()
        # rewrite the text
        text = rewrite_response(text)
        test_set.append({"prompt": prompt, "target_response": text})

# save the test set list as a json file
with open(BASELINE_TEST_SET, "w") as f:
    json.dump(test_set, f, indent=4)