import csv
from datetime import datetime
# from llama3 import run_llama3
from attack_grade import compute_attack_grade
from attack_record import JailbreakAttackRecord
from phi4 import run_phi4
import os

def _save_records_to_csv(records: list, csv_file_path: str) -> None:
    """
    Saves a list of JailbreakAttackRecord objects to a CSV file.

    :param records: List of JailbreakAttackRecord instances.
    :param csv_file_path: Path to the CSV file where the records will be saved.
    """
    # Define the header based on the attributes of JailbreakAttackRecord
    header = ["Attack Name", "Prompt", "Target Model", "Response", "Timestamp", "Grade"]
    file_exists = os.path.isfile(csv_file_path)

    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(header)

        # Iterate through each record and write it to the CSV
        for jailbreak_record in records:
            writer.writerow([
                jailbreak_record.attack_name,
                jailbreak_record.prompt,
                jailbreak_record.target_model,
                jailbreak_record.model_response,
                jailbreak_record.timestamp if isinstance(jailbreak_record.timestamp, str)
                else jailbreak_record.timestamp.isoformat(),
                jailbreak_record.grade
            ])


def work_with_llama3():
    list_of_records = run_llama3()
    list_of_records_instances = []
    for record in list_of_records:
        name = record[0]
        prompt = record[1]
        response = record[2]
        timestamp = record[3]
        grade = compute_attack_grade(prompt, response)
        new_attack_record = JailbreakAttackRecord(name, prompt, "LLAMA3", response, timestamp, grade)
        list_of_records_instances.append(new_attack_record)

    _save_records_to_csv(list_of_records_instances, "../data_layer/jailbreak_attacks_log/attacks_log.csv")


def work_with_phi4():
    list_of_records = run_phi4()
    list_of_records_instances = []
    for record in list_of_records:
        name = record[0]
        prompt = record[1]
        response = record[2]
        timestamp = record[3]
        grade = compute_attack_grade(prompt, response)
        new_attack_record = JailbreakAttackRecord(name, prompt, "phi4", response, timestamp, grade)
        list_of_records_instances.append(new_attack_record)

    _save_records_to_csv(list_of_records_instances, "../data_layer/jailbreak_attacks_log/attacks_log.csv")

work_with_phi4()