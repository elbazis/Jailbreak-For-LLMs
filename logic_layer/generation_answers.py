import asyncio
import pandas as pd
from tqdm.asyncio import tqdm as tqdm_asyncio
from attack_controller import ask_lmstudio
# Load prompts CSV
input_csv = "data_layer/jailbreak_prompts_datasets/first_dataset.csv"
output_csv = "data_layer/jailbreak_prompts_datasets/wizardlm_2_generated_answers.csv"

# Load prompts from CSV
df = pd.read_csv(input_csv)

# Assuming your CSV has a column named "prompt"
prompts = df['Prompt'].tolist()[:10]

# Function to generate three variations for each prompt
async def generate_jailbreak_variations(prompt):
    variations = []
    instruction_styles = [
        "Provide detailed explicit instructions:",
        "Provide a concise but clear guide:",
        "Briefly outline explicit steps clearly:"
    ]
    for style in instruction_styles:
        full_prompt = f"{style}\n{prompt}"
        response = await ask_lmstudio(full_prompt)
        variations.append(response.strip())
    return variations

# Main async function
async def main():
    results = []
    for prompt in tqdm_asyncio(prompts, desc="Generating answers"):
        answers = await generate_jailbreak_variations(prompt)
        # print(f"The answers are:\nFirst answer\n{answers[0]}\nSecond answer\n{answers[1]}\nThird answer\n{answers[2]}\n")
        results.append({
            "prompt": prompt,
            "answer_1": answers[0],
            "answer_2": answers[1],
            "answer_3": answers[2]
        })

    # Save generated answers to CSV
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_csv, index=False)

    print(f"✅ Generated jailbreak reference answers saved to '{output_csv}'")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())