from googletrans import Translator
import data_layer.jailbreak_prompts_datasets.jailbreak_prompts_datasets_handler as jbph
import os
import csv

names_and_prompts = jbph.create_list_of_pairs_names_and_prompts_from_csv(
    '../../data_layer/jailbreak_prompts_datasets/first_dataset.csv')

def _translate_prompts(lang):
    names_and_translated_prompts = []
    translator = Translator()
    for name, prompt in names_and_prompts:
        # print(prompt)
        # print("****")
        try:
            result = translator.translate(prompt, dest='eu')
            translated_prompt = result.text
        except Exception as e:
            print(prompt)
            print(f"❌ Error translating")
            translated_prompt = ""
        finally:
            names_and_translated_prompts.append((name, translated_prompt))
    return names_and_translated_prompts

def save_translated_prompts(lang):
    names_and_translated_prompts =_translate_prompts(lang)
    csv_file_path = f"../../data_layer/translated_jailbreak_prompts/{lang}_prompts.csv"
    header = ["Name", "Prompt"]
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(header)

        for translated_prompt_record in names_and_translated_prompts:
            writer.writerow([
                translated_prompt_record[0],
                translated_prompt_record[1]
            ])

# save_translated_prompts('eu') #באסקית
# save_translated_prompts('cy') #וולשית
save_translated_prompts('et')  # אסטונית
