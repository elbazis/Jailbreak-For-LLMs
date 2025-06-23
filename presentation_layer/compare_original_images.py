import pandas as pd
import matplotlib.pyplot as plt

# טען את קובץ הבייסליין
baseline_xlsx = '../data_layer/jailbreak_attacks_log/original_prompts_results.xlsx'
baseline_df = pd.read_excel(baseline_xlsx, sheet_name='Average Grade')

# טען את קובץ התמונות
photos_df = pd.read_excel('../data_layer/jailbreak_attacks_log/photos_results.xlsx', sheet_name='photos_results')

# הסר את הסיומת '_prompt.png' מהשמות
photos_df['Attack Name'] = photos_df['Attack Name'].str.replace('_prompt.png', '', regex=False)

# יישור לפי סדר הפרומפטים בבייסליין
photos_df = photos_df.set_index('Attack Name').reindex(baseline_df['Attack Name']).reset_index()

# === גרף ===
plt.figure(figsize=(14, 8))

# עקומת בייסליין
plt.plot(
    baseline_df['Attack Name'],
    baseline_df['Grade'],
    label='Original Average Grade',
    linewidth=2,
    marker='o',
    color='black'
)

# עקומת Photos
plt.plot(
    photos_df['Attack Name'],
    photos_df['Grade'],
    label='Photos Grade',
    linestyle='--',
    marker='x',
    color='orange'
)

# עיצוב
plt.title('Original vs Photos Prompt Grades')
plt.xlabel('Prompt')
plt.ylabel('Grade')
plt.legend()
plt.xticks(rotation=90, fontsize=8)
plt.grid(True)
plt.tight_layout()

plt.show()
