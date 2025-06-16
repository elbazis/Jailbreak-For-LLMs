import asyncio
from attack_controller import _save_records_to_csv, run_all
import data_layer.jailbreak_prompts_datasets.jailbreak_prompts_datasets_handler as jbph
import os
from attack_record import JailbreakAttackRecord
from datetime import datetime


def run_prompts(names_and_prompts, model, output_file):
    for name, prompt in names_and_prompts:
        responses = asyncio.run(run_all([prompt], model))
        records = []
        for response in responses:
            timestamp = datetime.now()
            grade = 0  # TODO: change
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


def main(prompts_path, prompts_lang):
    # names_and_prompts = jbph.create_list_of_pairs_names_and_prompts_from_csv(prompts_path)
    names_and_prompts = create_list_of_pairs_names_and_images_prompts(prompts_path)
    models = ["llava-llama-3-8b-v1_1"]
    for model in models:
        model = model.replace("/", "_")
        output_file = f"../data_layer/jailbreak_attacks_log/{model}_attacks_log_en_images.csv"
        run_prompts(names_and_prompts, model, output_file)


if __name__ == '__main__':
    #original
    main('../data_layer/images_prompts/original_prompts_images', 'en')

    #באסקית
    # main("../data_layer/translated_jailbreak_prompts/eu_prompts.csv",'eu')

    #וולשית
    # main("../data_layer/translated_jailbreak_prompts/cy_prompts.csv",'cy')

    #אסטונית
    # main("../data_layer/translated_jailbreak_prompts/et_prompts.csv",'et')
