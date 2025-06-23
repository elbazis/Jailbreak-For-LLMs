import asyncio
import os
from datetime import datetime

from attack_controller import _save_records_to_csv, run_all
import data_layer.jailbreak_prompts_datasets.jailbreak_prompts_datasets_handler as jbph
from attack_record import JailbreakAttackRecord
from evaluate_score import JailbreakScorer
from logic_layer.consts import MODELS, BASE_PATH


def run_prompts(names_and_prompts, model, output_file):
    scorer = JailbreakScorer(device="cpu", verbose=False)
    for name, prompt in names_and_prompts:
        responses = asyncio.run(run_all([prompt], model))
        records = []
        for response in responses:
            timestamp = datetime.now()
            grade = scorer(prompt, response)
            new_attack_record = JailbreakAttackRecord(name, prompt, model, response, timestamp, grade)
            records.append(new_attack_record)
        _save_records_to_csv(records, output_file)



def create_list_of_pairs_names_and_images_prompts(prompts_path):
    names_and_prompts_images = []

    for filename in os.listdir(prompts_path):
        if filename.endswith('_prompt.png'):
            prompt_name = filename[:-11]
            full_path = os.path.join(prompts_path, filename)
            names_and_prompts_images.append((prompt_name, full_path))
    return names_and_prompts_images


def main(prompts_path):
    names_and_prompts = jbph.create_list_of_pairs_names_and_prompts_from_csv(prompts_path)
    for model in MODELS:
        model = model.replace("/", "_")
        output_file = f"../data_layer/jailbreak_attacks_log/{model}_attacks_log.csv"
        run_prompts(names_and_prompts, model, output_file)


if __name__ == '__main__':
    for fname in os.listdir(f"../{BASE_PATH}"):
        if fname.endswith('.csv'):
            main(f"../{BASE_PATH}/{fname}")
