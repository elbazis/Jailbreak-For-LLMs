import random
import os
import csv
import data_layer.jailbreak_prompts_datasets.jailbreak_prompts_datasets_handler as jbph
from logic_layer.consts import BASE_PATH, KEYBOARD_NEIGHBORS, REPLACEMENTS

def to_upper(text):
    indices = random.sample(range(len(text)), k=len(text)//3)
    text = list(text)
    for i in indices:
        text[i] = text[i].upper()
    result = ''.join(text)
    return result

def introduce_typos(text):
    text = list(text)
    for _ in range(len(text) // 3):
        idx = random.randint(0, len(text) - 1)
        char = text[idx].lower()
        if char in KEYBOARD_NEIGHBORS:
            replacement = random.choice(KEYBOARD_NEIGHBORS[char])
            if text[idx].isupper():
                replacement = replacement.upper()
            text[idx] = replacement
    result = ''.join(text)
    return result


def replace_with_numbers(text):
    text = list(text)
    for _ in range(len(text) // 2):
        idx = random.randint(0, len(text) - 1)
        char = text[idx].lower()
        if char in REPLACEMENTS:
            text[idx] = REPLACEMENTS[char]
    result = ''.join(text)
    return result

def shuffle_letters(text):
    words = text.split()
    for i in range(len(words)):
        if len(words[i]) > 3:
            chars = list(words[i])
            idx1, idx2 = random.sample(range(len(chars)), 2)
            chars[idx1], chars[idx2] = chars[idx2], chars[idx1]
            words[i] = ''.join(chars)
    result = ' '.join(words)
    return result

def add_remove_spaces(text):
    text = list(text)
    for _ in range(len(text) // 3):
        action = random.choice(['add', 'remove'])
        idx = random.randint(0, len(text) - 1)
        if action == 'add':
            text.insert(idx, ' ')
        elif action == 'remove' and text[idx] == ' ':
            text.pop(idx)
    result = ''.join(text)
    return result

def shuffle_words(text):
    words = text.split()
    for _ in range(len(words) // 5):
        idx1, idx2 = random.sample(range(len(words)), 2)
        words[idx1], words[idx2] = words[idx2], words[idx1]
    result = ' '.join(words)
    return result

def distort_text(text):
    print("[Original]:", text)
    steps = [
        to_upper,
        introduce_typos,
        replace_with_numbers,
        shuffle_letters,
        add_remove_spaces,
        shuffle_words
    ]
    for step in steps:
        text = step(text)
    return text


def _create_all_augmentations_for_all_prompts():
    names_and_prompts = jbph.create_list_of_pairs_names_and_prompts_from_csv(f"../../{BASE_PATH}/first_dataset.csv")
    names_and_augmentations = []
    for name, original_prompt in names_and_prompts:
        steps = [
            to_upper,
            introduce_typos,
            replace_with_numbers,
            shuffle_letters,
            add_remove_spaces,
            shuffle_words
        ]
        all_augmentations_prompt = original_prompt
        for step in steps:
            all_augmentations_prompt = step(all_augmentations_prompt)
            only_one_augmentation_prompt = step(original_prompt)
            names_and_augmentations.append((name, only_one_augmentation_prompt, step.__name__))
        names_and_augmentations.append((name, all_augmentations_prompt, "all steps"))
    return names_and_augmentations

def save_augmentations_to_csv():
    names_and_augmentations = _create_all_augmentations_for_all_prompts()
    csv_file_path = f"../../{BASE_PATH}/augmentations_prompts.csv"
    header = ["Name", "Prompt", "Augmentation Type"]
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        if not file_exists:
            writer.writerow(header)

        for augmentation_record in names_and_augmentations:
            writer.writerow([
                augmentation_record[0],
                augmentation_record[1],
                augmentation_record[2]
            ])

save_augmentations_to_csv()