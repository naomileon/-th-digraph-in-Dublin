import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

task_n = 1 if len(sys.argv) < 2 else int(sys.argv[1])
task1_cultP = f'./in/Task{task_n}Proches.txt'
task1_cultE = f'./in/Task{task_n}Eloignes.txt'
title = f"Task{task_n}" if task_n < 3 else "Tasks"

with open(task1_cultP, 'r') as f:
    data = [line.strip().split('\t') for line in f.readlines()[1:]]
    for row in data:
        row.append("C")
    df_p = pd.DataFrame(data, columns=["speaker", "label", "culture"])
    
with open(task1_cultE, 'r') as f:
    data = [line.strip().split('\t') for line in f.readlines()[1:]]
    for row in data:
        row.append("F")
    df_e = pd.DataFrame(data, columns=["speaker", "label", "culture"])

df = pd.concat([df_p, df_e], ignore_index=True)

def generate_for_culture(full_df, plot_type):
    df_filtered = df[df['label'] == ('?' if plot_type=='other' else plot_type)]

    df_percent = df_filtered.groupby(['speaker', 'culture']).size() / df.groupby(['speaker', 'culture']).size() * 100
    df_percent = df_percent.reset_index(name=f'%{plot_type}')
    df_percent = df_percent.fillna(0.0)

    quartiles = df_percent.groupby('culture')[f'%{plot_type}'].quantile([0.25, 0.5, 0.75]).unstack()
    quartiles.columns = ['Q1', 'Q2 (Median)', 'Q3']
    quartiles['Type'] = plot_type
    quartiles['Culture'] = quartiles.index
    quartiles = quartiles[['Type', 'Culture', 'Q1', 'Q2 (Median)', 'Q3']]

    sns.boxplot(data=df_percent, x='culture', y=f'%{plot_type}', hue='culture', palette=["#F8766D", "#00BFC4"], legend=False)

    plt.title(f"{title} %{plot_type} According to Cultural affiliation")
    plt.xlabel("Cultural Affiliation")
    plt.ylabel(f"% {plot_type}")

    plt.savefig(f"./out/{title}/{title}_{plot_type}_cult.png", dpi=300)
    plt.close()
    
    return quartiles
    
stats_occ = generate_for_culture(df, 'OCC')
stats_fr = generate_for_culture(df, 'FR')
stats_other = generate_for_culture(df, 'other')
stats_df = pd.concat([stats_occ, stats_fr, stats_other], ignore_index=True)
stats_df.to_csv(f"./out/{title}/{title}_Cult_stats.csv", index=False)
