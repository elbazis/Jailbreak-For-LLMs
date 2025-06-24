import pandas as pd
import matplotlib.pyplot as plt

def load_average_grades(path):
    return pd.read_excel(path, sheet_name='Average Grade')

def load_combined_augmented_data(path):
    xls = pd.ExcelFile(path)
    all_aug_dfs = [pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names]
    return pd.concat(all_aug_dfs)

def compute_mean_per_prompt_and_augmentation(combined_df):
    return (
        combined_df.groupby(['Attack Name', 'Augmentation Type'])['New Grading']
        .mean()
        .reset_index()
    )

def plot_comparison_per_augmentation(average_df, mean_by_prompt_aug):
    augmentation_types = mean_by_prompt_aug['Augmentation Type'].unique()

    for aug_type in augmentation_types:
        plt.figure(figsize=(14, 8))

        plt.plot(
            average_df['Attack Name'],
            average_df['Grade Augmentations'],
            label='Original Average Grade',
            linewidth=2,
            marker='o',
            color='blue'
        )

        sub_df = mean_by_prompt_aug[mean_by_prompt_aug['Augmentation Type'] == aug_type]
        sub_df = sub_df.set_index('Attack Name').reindex(average_df['Attack Name']).reset_index()

        plt.plot(
            sub_df['Attack Name'],
            sub_df['New Grading'],
            label=f'Augmentation: {aug_type}',
            linestyle='--',
            marker='x',
            color='orange'
        )

        plt.title(f'Average Grade vs {aug_type}')
        plt.xlabel('Prompt')
        plt.ylabel('Grade')
        plt.legend()
        plt.xticks(rotation=90, fontsize=8)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def plot_bar_chart_avg_per_augmentation(combined_aug_df, baseline_avg):
    avg_per_augmentation = (
        combined_aug_df.groupby('Augmentation Type')['New Grading']
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))
    avg_per_augmentation.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.axhline(y=baseline_avg, color='red', linestyle='--', label='Baseline')

    plt.title('Average Grade per Augmentation Type (with Baseline)')
    plt.ylabel('Average Grade')
    plt.xlabel('Augmentation Type')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()
