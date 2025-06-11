import random
import os
import csv
import data_layer.jailbreak_prompts_datasets.jailbreak_prompts_datasets_handler as jbph

def to_upper(text):
    indices = random.sample(range(len(text)), k=len(text)//3)
    text = list(text)
    for i in indices:
        text[i] = text[i].upper()
    result = ''.join(text)
    # print("[After to_upper]:", result)
    return result

def introduce_typos(text):
    keyboard_neighbors = {
        'a': ['q', 'w', 's', 'z'],
        'b': ['v', 'g', 'h', 'n'],
        'c': ['x', 'd', 'f', 'v'],
        'd': ['s', 'e', 'r', 'f', 'c', 'x'],
        'e': ['w', 's', 'd', 'r'],
        'f': ['d', 'r', 't', 'g', 'v', 'c'],
        'g': ['f', 't', 'y', 'h', 'b', 'v'],
        'h': ['g', 'y', 'u', 'j', 'n', 'b'],
        'i': ['u', 'j', 'k', 'o'],
        'j': ['h', 'u', 'i', 'k', 'n', 'm'],
        'k': ['j', 'i', 'o', 'l', 'm'],
        'l': ['k', 'o', 'p'],
        'm': ['n', 'j', 'k'],
        'n': ['b', 'h', 'j', 'm'],
        'o': ['i', 'k', 'l', 'p'],
        'p': ['o', 'l'],
        'q': ['a', 'w'],
        'r': ['e', 'd', 'f', 't'],
        's': ['a', 'w', 'e', 'd', 'x', 'z'],
        't': ['r', 'f', 'g', 'y'],
        'u': ['y', 'h', 'j', 'i'],
        'v': ['c', 'f', 'g', 'b'],
        'w': ['q', 'a', 's', 'e'],
        'x': ['z', 's', 'd', 'c'],
        'y': ['t', 'g', 'h', 'u'],
        'z': ['a', 's', 'x'],
    }

    text = list(text)
    for _ in range(len(text) // 3):
        idx = random.randint(0, len(text) - 1)
        char = text[idx].lower()
        if char in keyboard_neighbors:
            replacement = random.choice(keyboard_neighbors[char])
            if text[idx].isupper():
                replacement = replacement.upper()
            text[idx] = replacement
    result = ''.join(text)
    # print("[After introduce_typos]:", result)
    return result


def replace_with_numbers(text):
    replacements = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
    text = list(text)
    for _ in range(len(text) // 2):
        idx = random.randint(0, len(text) - 1)
        char = text[idx].lower()
        if char in replacements:
            text[idx] = replacements[char]
    result = ''.join(text)
    # print("[After replace_with_numbers]:", result)
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
    # print("[After shuffle_letters]:", result)
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
    # print("[After add_remove_spaces]:", result)
    return result

def shuffle_words(text):
    words = text.split()
    for _ in range(len(words) // 5):
        idx1, idx2 = random.sample(range(len(words)), 2)
        words[idx1], words[idx2] = words[idx2], words[idx1]
    result = ' '.join(words)
    # print("[After shuffle_words]:", result)
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
    # original_tex = text
    for step in steps:
        text = step(text)
    return text

# # דוגמה לשימוש
# original_text = "Hi my name is Adi"
# distorted = distort_text(original_text)
# print("[Final distorted]:", distorted)

names_and_prompts = jbph.create_list_of_pairs_names_and_prompts_from_csv(
    '../../data_layer/jailbreak_prompts_datasets/first_dataset.csv')

def _create_all_augmentations_for_all_prompts():
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
    csv_file_path = f"../../data_layer/jailbreak_prompts_datasets/augmentations_prompts.csv"
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