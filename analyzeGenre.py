import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

task_n = 1 if len(sys.argv) < 2 else int(sys.argv[1])
task1_genreF = f'./in/Task{task_n}Femmes.txt'
task1_genreH = f'./in/Task{task_n}Hommes.txt'
title = f"Task{task_n}" if task_n < 3 else "Tasks"

with open(task1_genreF, 'r') as f:
    data = [line.strip().split('\t') for line in f.readlines()[1:]]
    for row in data:
        row.append("F")
    df_f = pd.DataFrame(data, columns=["speaker", "label", "genre"])
    
with open(task1_genreH, 'r') as f:
    data = [line.strip().split('\t') for line in f.readlines()[1:]]
    for row in data:
        row.append("M")
    df_h = pd.DataFrame(data, columns=["speaker", "label", "genre"])

df = pd.concat([df_f, df_h], ignore_index=True)

def generate_for_gender(full_df, plot_type):
    df_filtered = df[df['label'] == ('?' if plot_type=='other' else plot_type)]

    df_percent = df_filtered.groupby(['speaker', 'genre']).size() / df.groupby(['speaker', 'genre']).size() * 100
    df_percent = df_percent.reset_index(name=f'%{plot_type}')
    # In case there are no FR, OCC or ? for a speaker
    df_percent = df_percent.fillna(0.0)

    quartiles = df_percent.groupby('genre')[f'%{plot_type}'].quantile([0.25, 0.5, 0.75]).unstack()
    quartiles.columns = ['Q1', 'Q2 (Median)', 'Q3']
    quartiles['Type'] = plot_type
    quartiles['Genre'] = quartiles.index
    quartiles = quartiles[['Type', 'Genre', 'Q1', 'Q2 (Median)', 'Q3']]

    sns.boxplot(data=df_percent, x='genre', y=f'%{plot_type}', hue='genre', palette=["#F8766D", "#00BFC4"], legend=False)

    plt.title(f"{title} %{plot_type} According to Gender")
    plt.xlabel("Gender")
    plt.ylabel(f"% {plot_type}")

    plt.savefig(f"./out/{title}/{title}_{plot_type}_genre.png", dpi=300)
    plt.close()
    
    return quartiles
    
stats_occ = generate_for_gender(df, 'OCC')
stats_fr = generate_for_gender(df, 'FR')
stats_other = generate_for_gender(df, 'other')
stats_df = pd.concat([stats_occ, stats_fr, stats_other], ignore_index=True)
stats_df.to_csv(f"./out/{title}/{title}_Genre_stats.csv", index=False)
