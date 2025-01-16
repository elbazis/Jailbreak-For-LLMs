from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
import os
import data_layer.jailbreak_prompts_datasets.jailbreak_prompts_datasets_handler as jbph

load_dotenv()


def run_llama3() -> list:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    names_and_prompts = jbph.create_list_of_pairs_names_and_prompts_from_csv('../data_layer/jailbreak_prompts_datasets/first_dataset.csv')

    records = []
    # i = 0
    for name, prompt in names_and_prompts:
        # if i >= 4:
        #     break
        # i += 1
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        responses = []
        for chunk in completion:
            # print(chunk.choices[0].delta.content or "", end="")
            responses.append(chunk.choices[0].delta.content or "")
        # print(i)
        print("".join(responses))
        current_timestamp = datetime.now().isoformat()
        records.append((name, prompt, "".join(responses), current_timestamp))
    return records
