# Jailbreak-For-LLMs

A framework for evaluating the robustness of Large Language Models (LLMs) against jailbreak attacks, including prompt augmentation, translation, image-based prompts, and automated scoring.

---

## Table of Contents

- [Setup](#setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create and Activate a Virtual Environment](#2-create-and-activate-a-virtual-environment)
  - [3. Install Python Dependencies](#3-install-python-dependencies)
  - [4. Install and Set Up LM Studio](#4-install-and-set-up-lm-studio)
  - [5. Download and Load Models in LM Studio](#5-download-and-load-models-in-lm-studio)
- [Running Prompts](#running-prompts)
- [Generating Graphs](#generating-graphs)
- [Translating Prompts](#translating-prompts)
- [Adding New Prompts](#adding-new-prompts)
- [Evaluating Scores](#evaluating-scores)
- [Prompt Augmentation](#prompt-augmentation)
- [Image-Based Prompts](#image-based-prompts)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/elbazis/Jailbreak-For-LLMs
cd Jailbreak-For-LLMs
```

### 2. Create and Activate a Virtual Environment

```sh
python3 -m venv project_venv
source project_venv/bin/activate
```

### 3. Install Python Dependencies

```sh
pip install -r requirements.txt
```

### 4. Install and Set Up LM Studio

- Download LM Studio from [https://lmstudio.ai/](https://lmstudio.ai/)
- Install and launch LM Studio on your machine.

### 5. Download and Load Models in LM Studio

- In LM Studio, search for and download the models listed in [`logic_layer/consts.py`](logic_layer/consts.py) under `MODELS`.
- Start the local server in LM Studio (usually via the UI: "Start Server" or similar).
- By default, the server runs at `http://localhost:1234`.

---

## Running Prompts

To run prompts against all models and log results:

```sh
cd logic_layer
python run_prompts.py
```
- This will process all CSVs in `data_layer/jailbreak_prompts_datasets/` and save results in `data_layer/jailbreak_attacks_log/`.

---

## Generating Graphs

To visualize and compare results:

```sh
cd presentation_layer
python compare_original_translated.py
```
- This will generate graphs comparing baseline and translated prompt results.

---

## Translating Prompts

To translate prompts to another language (e.g., Basque):

```sh
cd logic_layer/attack_combinations
python translate_prompts.py
```
- Edit `translate_prompts.py` to set the target language code (e.g., `"eu"` for Basque).
- Translated prompts will be saved in `data_layer/translated_jailbreak_prompts/`.

---

## Adding New Prompts

1. Add your new prompts to a CSV file in `data_layer/jailbreak_prompts_datasets/` (e.g., `first_dataset.csv`).
   - Format: columns `Name`, `Prompt`.
2. If needed, use [`format_csv_to_two_columns`](data_layer/jailbreak_prompts_datasets/jailbreak_prompts_datasets_handler.py) to reformat your CSV.

---

## Evaluating Scores

Scoring is handled automatically during prompt runs using [`JailbreakScorer`](logic_layer/evaluate_score.py).  
You can also use it directly:

```python
from evaluate_score import JailbreakScorer
scorer = JailbreakScorer()
score = scorer(prompt, answer)
```

---

## Prompt Augmentation

To generate augmented prompts (typos, shuffling, etc.):

```sh
cd logic_layer/attack_combinations
python text_augmentation_prompts.py
```
- Augmented prompts will be saved in `data_layer/jailbreak_prompts_datasets/augmentations_prompts.csv`.

---

## Image-Based Prompts

To convert prompts to images:

```sh
cd logic_layer/attack_combinations
python image_prompts.py
```
- Images will be saved in `data_layer/images_prompts/`.

To run attacks using image prompts, use the relevant functions in [`attack_controller.py`](logic_layer/attack_controller.py).

---

## Project Structure

- `logic_layer/`: Core logic (prompt running, scoring, augmentation, translation, etc.)
- `data_layer/`: Datasets, logs, and images.
- `presentation_layer/`: Visualization and graphing scripts.
- `data_access_layer/`: Database access utilities.

---

## Troubleshooting

- **LM Studio not responding:** Ensure the server is running and the correct model is loaded.
- **Model not found:** Download the required model in LM Studio.
- **Missing dependencies:** Reinstall with `pip install -r requirements.txt`.
- **Encoding issues:** Ensure all CSVs are UTF-8 encoded.

---

For further details, see the source code and comments in each script.