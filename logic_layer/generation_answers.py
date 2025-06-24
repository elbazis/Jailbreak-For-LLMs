import asyncio
import pandas as pd
from tqdm.asyncio import tqdm as tqdm_asyncio
from attack_controller import ask_lmstudio
from logic_layer.consts import MODELS, BASE_PATH

input_csv = f"{BASE_PATH}/first_dataset.csv"
df = pd.read_csv(input_csv)
prompts = df['Prompt'].tolist()

# Function to generate three variations for each prompt
async def generate_jailbreak_variations(prompt):
    variations = []
    instruction_styles = [
        "Provide detailed explicit instructions:",
        "Provide a concise but clear guide:",
        "Briefly outline explicit steps clearly:"
    ]
    for style in instruction_styles:
        for model in MODELS:
            full_prompt = f"{style}\n{prompt}"
            response = await ask_lmstudio(full_prompt, model)
            variations.append(response.strip())
    return variations

async def main():
    results = []
    for prompt in tqdm_asyncio(prompts, desc="Generating answers"):
        answers = await generate_jailbreak_variations(prompt)
        results.append({
            "prompt": prompt,
            "answer_1": answers[0],
            "answer_2": answers[1],
            "answer_3": answers[2]
        })

    df_results = pd.DataFrame(results)
    df_results.to_csv(BASE_PATH, index=False)

    print(f"Generated jailbreak reference answers saved to '{BASE_PATH}'")


if __name__ == "__main__":
    asyncio.run(main())