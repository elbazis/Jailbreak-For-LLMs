from langchain_community.llms import Ollama
import data_layer.jailbreak_prompts_datasets.jailbreak_prompts_datasets_handler as jbph
from datetime import datetime
model = Ollama(model="phi4")
# result = model.invoke(input="who are you")
# print(result)


def run_phi4() -> list:
    names_and_prompts = jbph.create_list_of_pairs_names_and_prompts_from_csv('../data_layer/jailbreak_prompts_datasets/first_dataset.csv')
    # names_and_prompts = [("hello", "how are you")]
    records = []
    for name, prompt in names_and_prompts:
        result = model.invoke(input=prompt)
        print(result)
        current_timestamp = datetime.now().isoformat()
        records.append((name, prompt, result, current_timestamp))
    return records
