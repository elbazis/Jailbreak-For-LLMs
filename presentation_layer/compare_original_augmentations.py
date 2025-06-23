import pandas as pd
import matplotlib.pyplot as plt

# # List of xlsx files to compare
# compare_original_to_translated_xlsx_files = [
#     'original_prompts_results.xlsx',
#     'translate_cy_prompts_results.xlsx',
#     'translate_et_prompts_results.xlsx',
#     'translate_eu_prompts_results.xlsx'
# ]
# compare_original_to_photos_xlsx_files = [
#     'original_prompts_results.xlsx',
#     'photos_results.xlsx'
# ]
# compare_original_to_augmentations_xlsx_files = [
#     'original_prompts_results.xlsx',
#     'augmentations_prompts_results.xlsx'
# ]

# === שלב 1: טען את גיליון 'Average Grade' ===
average_grade_xlsx = '../data_layer/jailbreak_attacks_log/original_prompts_results.xlsx'
average_df = pd.read_excel(average_grade_xlsx, sheet_name='Average Grade')

# === שלב 2: טען את כל גיליונות קובץ האוגמנטציות ===
augmentations_xlsx = '../data_layer/jailbreak_attacks_log/augmentations_prompts_results.xlsx'
xls = pd.ExcelFile(augmentations_xlsx)

all_aug_dfs = [pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names]
combined_aug_df = pd.concat(all_aug_dfs)

# === שלב 3: חישוב ממוצעים לכל שילוב של Attack Name ו-Aggregation Type ===
mean_by_prompt_aug = (
    combined_aug_df.groupby(['Attack Name', 'Augmentation Type'])['Grade']
    .mean()
    .reset_index()
)

# === שלב 4: יצירת גרף נפרד לכל Augmentation Type ===
augmentation_types = mean_by_prompt_aug['Augmentation Type'].unique()

for aug_type in augmentation_types:
    plt.figure(figsize=(14, 8))

    # עקומת base line - ה-Original Average
    plt.plot(
        average_df['Attack Name'],
        average_df['Grade'],
        label='Original Average Grade',
        linewidth=2,
        marker='o',
        color='blue'
    )

    # עקומת האוגמנטציה הספציפית
    sub_df = mean_by_prompt_aug[mean_by_prompt_aug['Augmentation Type'] == aug_type]
    sub_df = sub_df.set_index('Attack Name').reindex(average_df['Attack Name']).reset_index()

    plt.plot(
        sub_df['Attack Name'],
        sub_df['Grade'],
        label=f'Augmentation: {aug_type}',
        linestyle='--',
        marker='x',
        color='orange'
    )

    # עיצוב גרף
    plt.title(f'Average Grade vs {aug_type}')
    plt.xlabel('Prompt')
    plt.ylabel('Grade')
    plt.legend()
    plt.xticks(rotation=90, fontsize=8)
    plt.grid(True)
    plt.tight_layout()

    # שמירה כקובץ (אופציונלי):
    # plt.savefig(f'comparison_{aug_type}.png', dpi=300)

    plt.show()