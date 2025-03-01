import json
import os


RAW_DATA_DIR = "raw_documents"
BASELINE_TEST_SET = "test_sets/baseline_test_set.json"


# for each file in the raw data directory
# read the file and extract the text
# and apppned to the test set list
test_set = []
for file in os.listdir(RAW_DATA_DIR):
    with open(os.path.join(RAW_DATA_DIR, file), "r") as f:
        # extract the file name without the extension
        # as the prompt
        prompt = "Provide a summary of " + os.path.splitext(file)[0].replace("_", " ") 
        text = f.read()
        test_set.append({"prompt": prompt, "golden_response": text})

# save the test set list as a json file
with open(BASELINE_TEST_SET, "w") as f:
    json.dump(test_set, f, indent=4)