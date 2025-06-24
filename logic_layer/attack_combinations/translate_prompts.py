from googletrans import Translator
from tqdm import tqdm
import pandas as pd
import os
import csv
import data_layer.jailbreak_prompts_datasets.jailbreak_prompts_datasets_handler as jbph
from logic_layer.consts import BASE_PATH


def _translate_prompts(lang):
    names_and_prompts = jbph.create_list_of_pairs_names_and_prompts_from_csv(f"../../{BASE_PATH}/first_dataset.csv")
    names_and_translated_prompts = []
    translator = Translator()
    for name, prompt in names_and_prompts:
        try:
            result = translator.translate(prompt, dest=lang)
            translated_prompt = result.text
        except Exception as e:
            print(prompt)
            print(f"Error translating")
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


def translate_responses_in_excel(
        path: str,
        sheet_name: str = 0,
        response_col: str = "Response",
        lang: str = "en",
        output_path: str = None
    ):

    translator = Translator()
    df = pd.read_excel(path, sheet_name=sheet_name)
    if response_col not in df.columns:
        raise KeyError(f"Column '{response_col}' not found in sheet.")

    translated_responses = []
    for response in tqdm(df[response_col].astype(str)):
        try:
            result = translator.translate(response, dest=lang)
            translated_responses.append(result.text)
        except Exception as e:
            print(f"Error translating: {response[:60]}...")
            translated_responses.append("")

    df["Translated Response"] = translated_responses
    if not output_path:
        output_path = path.replace(".xlsx", f"_translated_{lang}.xlsx")

    df.to_excel(output_path, index=False)