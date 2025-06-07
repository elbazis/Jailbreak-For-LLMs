import asyncio
from attack_controller import _save_records_to_csv, run_all
import data_layer.jailbreak_prompts_datasets.jailbreak_prompts_datasets_handler as jbph
from attack_record import JailbreakAttackRecord
from datetime import datetime


def run_prompts(names_and_prompts, model, output_file):
    prompts_only = [prompt for _, prompt in names_and_prompts]
    responses = asyncio.run(run_all(prompts_only, model))
    records = []
    for (name, prompt), response in zip(names_and_prompts, responses):
        timestamp = datetime.now()
        grade = 0  # TODO: change
        new_attack_record = JailbreakAttackRecord(name, prompt, model, response, timestamp, grade)
        records.append(new_attack_record)

    _save_records_to_csv(records, output_file)

def main(prompts_path, prompts_lang):
    names_and_prompts = jbph.create_list_of_pairs_names_and_prompts_from_csv(prompts_path)
    models = ["google/gemma-3-12b", "llava-llama-3-8b-v1_1"]
    for model in models:
        model = model.replace("/", "_")
        output_file = f"../data_layer/jailbreak_attacks_log/{model}_attacks_log_{prompts_lang}.csv"
        run_prompts(names_and_prompts, model, output_file)


if __name__ == '__main__':
    #original
    main('../data_layer/jailbreak_prompts_datasets/first_dataset.csv', 'en')

    #באסקית
    main("../data_layer/translated_jailbreak_prompts/eu_prompts.csv",'eu')

    #וולשית
    main("../data_layer/translated_jailbreak_prompts/cy_prompts.csv",'cy')

    #אסטונית
    main("../data_layer/translated_jailbreak_prompts/et_prompts.csv",'et')
