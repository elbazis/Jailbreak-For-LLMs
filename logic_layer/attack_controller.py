import csv
from datetime import datetime
from attack_record import JailbreakAttackRecord
import os
import aiohttp
import html

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


async def ask_lmstudio(prompt):
    async with aiohttp.ClientSession() as session:
        payload = {
            "model": "gemma-3-4b-it",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "stream": False
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        async with session.post("http://localhost:1234/v1/chat/completions", json=payload, headers=headers, timeout=1800) as resp:
            res = await resp.json()
            raw_text = res["choices"][0]["message"]["content"]

            # Clean up encoding issues and decode HTML entities
            cleaned_text = (
                raw_text
                .encode('latin1', errors='ignore')  # Fix common mojibake
                .decode('utf-8', errors='ignore')   # Decode properly
            )
            cleaned_text = html.unescape(cleaned_text)  # Fix things like &amp; -> &

            print(cleaned_text)
            return cleaned_text

async def run_all(prompts):
    tasks = [ask_lmstudio(p) for p in prompts]
    return await asyncio.gather(*tasks)