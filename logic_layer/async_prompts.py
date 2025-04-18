import aiohttp
import html
import asyncio
from attack_controller import _save_records_to_csv, run_all
import data_layer.jailbreak_prompts_datasets.jailbreak_prompts_datasets_handler as jbph
from attack_record import JailbreakAttackRecord
from datetime import datetime


if __name__ == '__main__':
    names_and_prompts = jbph.create_list_of_pairs_names_and_prompts_from_csv(
        'data_layer/jailbreak_prompts_datasets/first_dataset.csv')
    prompts_only = [prompt for _, prompt in names_and_prompts]
    responses = asyncio.run(run_all(prompts_only))
    records = []
    for (name, prompt), response in zip(names_and_prompts, responses):
        timestamp = datetime.now().isoformat()
        # grade = compute_attack_grade(prompt, response)
        grade = 0 #TODO: change
        new_attack_record = JailbreakAttackRecord(name, prompt, "gemma3", response, timestamp, grade)
        records.append(new_attack_record)

    _save_records_to_csv(records, "data_layer/jailbreak_attacks_log/attacks_log_new.csv")

