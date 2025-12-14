import pandas as pd
import matplotlib.pyplot as plt

# Set Japanese font for Mac
plt.rcParams['font.family'] = 'Hiragino Sans'

# Load data, skipping the first 2 rows of metadata
file_path = '/Users/aoyamahiroki/Desktop/field_analysis/question.csv'
df = pd.read_csv(file_path, encoding='cp932', header=2)

# Rename columns for easier access
df.columns = ['Category', 'QuestionNo', 'NationalRate', 'SchoolRate']

# Data Cleaning
# Ensure rates are numeric (remove '%' if present, though sample data looked numeric but as strings maybe? or just verify)
# The sample output showed 61.4, so they might be floats already or strings.
# forcing conversion just in case.
# Data Cleaning
# Force conversion to numeric, coercing errors to NaN
df['NationalRate'] = pd.to_numeric(df['NationalRate'].astype(str).str.replace('%', ''), errors='coerce')
df['SchoolRate'] = pd.to_numeric(df['SchoolRate'].astype(str).str.replace('%', ''), errors='coerce')

# Drop rows where data could not be converted (likely headers or empty lines)
initial_count = len(df)
df = df.dropna(subset=['NationalRate', 'SchoolRate'])
dropped_count = initial_count - len(df)
if dropped_count > 0:
    print(f"Warning: Dropped {dropped_count} rows due to invalid numeric data.")

# Calculate difference
df['Difference'] = df['SchoolRate'] - df['NationalRate']

# --- Analysis 1: Field-level Performance ---
# Group by Category and calculate means
field_stats = df.groupby('Category').agg({
    'NationalRate': 'mean',
    'SchoolRate': 'mean',
    'Difference': 'mean',
    'QuestionNo': 'count' # Count of questions in that field
}).reset_index()

# Rename for clarity
field_stats.rename(columns={'QuestionNo': 'NumQuestions'}, inplace=True)

# Sort by Difference (ascending) to find weakest fields
weak_fields = field_stats[field_stats['Difference'] < 0].sort_values('Difference')

# --- Analysis 2: Question-level Weaknesses ---
# Identify individual questions where school is significantly lower (e.g., > 10% difference)
significant_weak_questions = df[df['Difference'] <= -10].sort_values('Difference')

# Output Results
print("# 分析結果: 全国平均を下回る分野\n")

print("## 1. 分野別比較 (差の小さい順)")
print("| 分野 | 問題数 | 貴校平均(%) | 全国平均(%) | 差(ポイント) |")
print("| :--- | :---: | :---: | :---: | :---: |")
for _, row in weak_fields.iterrows():
    print(f"| {row['Category']} | {row['NumQuestions']} | {row['SchoolRate']:.1f} | {row['NationalRate']:.1f} | {row['Difference']:.1f} |")

print("\n\n## 2. 特に正答率が低い個別問題 (差が-10ポイント以下)")
print("| 分野 | 問題番号 | 貴校(%) | 全国(%) | 差 |")
print("| :--- | :---: | :---: | :---: | :---: |")
for _, row in significant_weak_questions.iterrows():
    print(f"| {row['Category']} | {row['QuestionNo']} | {row['SchoolRate']} | {row['NationalRate']} | {row['Difference']:.1f} |")

# Visualize
plt.figure(figsize=(10, 6))
# Filter for fields with negative difference only for the chart, or all fields? 
# Let's show all fields sorted by difference to give context.
sorted_stats = field_stats.sort_values('Difference')

plt.barh(sorted_stats['Category'], sorted_stats['Difference'], color=['red' if x < 0 else 'blue' for x in sorted_stats['Difference']])
plt.axvline(0, color='black', linewidth=0.8)
plt.title('分野別: 貴校正答率 - 全国正答率')
plt.xlabel('差 (ポイント)')
plt.ylabel('分野')
plt.tight_layout()
plt.savefig('/Users/aoyamahiroki/Desktop/field_analysis/performance_gap_chart.png')
print("\nChar image saved to: /Users/aoyamahiroki/Desktop/field_analysis/performance_gap_chart.png")
