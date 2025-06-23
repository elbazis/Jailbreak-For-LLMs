# import pandas as pd
# import matplotlib.pyplot as plt
#
# # === קובץ הבייסליין ===
# baseline_xlsx = '../data_layer/jailbreak_attacks_log/original_prompts_results.xlsx'
# baseline_df = pd.read_excel(baseline_xlsx, sheet_name='Average Grade')
#
# # === קבצי תרגום ===
# translated_xlsx_files = [
#     'translate_cy_prompts_results.xlsx',
#     'translate_et_prompts_results.xlsx',
#     'translate_eu_prompts_results.xlsx'
# ]
#
# translated_labels = ['Translated (cy)', 'Translated (et)', 'Translated (eu)']
# colors = ['blue', 'green', 'purple']
#
# # === עבור כל קובץ תרגום – צור גרף נפרד ===
# for file, label, color in zip(translated_xlsx_files, translated_labels, colors):
#     df = pd.read_excel(f'../data_layer/jailbreak_attacks_log/{file}', sheet_name='Average Grade')
#
#     # יישור לפי הבייסליין
#     df = df.set_index('Attack Name').reindex(baseline_df['Attack Name']).reset_index()
#
#     # גרף
#     plt.figure(figsize=(14, 8))
#
#     # baseline
#     plt.plot(
#         baseline_df['Attack Name'],
#         baseline_df['Grade'],
#         label='Original Average Grade',
#         linewidth=2,
#         marker='o',
#         color='black'
#     )
#
#     # עקומת תרגום
#     plt.plot(
#         df['Attack Name'],
#         df['Grade'],
#         label=label,
#         linestyle='--',
#         marker='x',
#         color=color
#     )
#
#     # עיצוב
#     plt.title(f'Original vs {label}')
#     plt.xlabel('Prompt')
#     plt.ylabel('Grade')
#     plt.legend()
#     plt.xticks(rotation=90, fontsize=8)
#     plt.grid(True)
#     plt.tight_layout()
#
#     # הצגה (אפשר גם לשמור לקובץ אם רוצים)
#     # plt.savefig(f'comparison_{label}.png', dpi=300)
#     plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# === קובצי תרגום בלבד ===
translated_xlsx_files = [
    'translate_cy_prompts_results.xlsx',
    'translate_et_prompts_results.xlsx',
    'translate_eu_prompts_results.xlsx'
]

translated_labels = ['Translated (cy)', 'Translated (et)', 'Translated (eu)']
colors = ['blue', 'green', 'purple']

# === טען את כל קבצי התרגום ===
translated_dfs = [
    pd.read_excel(f'../data_layer/jailbreak_attacks_log/{file}', sheet_name='Average Grade')
    for file in translated_xlsx_files
]

# === גרף אחד עם 3 עקומות ===
plt.figure(figsize=(14, 8))

# נשתמש בקובץ הראשון כבסיס לסדר ההופעה בציר X
x_axis = translated_dfs[0]['Attack Name']

# ציור כל עקומת תרגום
for df, label, color in zip(translated_dfs, translated_labels, colors):
    # נוודא סדר אחיד לפי x_axis
    df = df.set_index('Attack Name').reindex(x_axis).reset_index()
    plt.plot(
        df['Attack Name'],
        df['Grade'],
        label=label,
        linestyle='--',
        marker='x',
        color=color
    )

# === עיצוב גרף ===
plt.title('Comparison of Translated Prompts (No Baseline)')
plt.xlabel('Prompt')
plt.ylabel('Grade')
plt.legend()
plt.xticks(rotation=90, fontsize=8)
plt.grid(True)
plt.tight_layout()

# הצגה
plt.show()

