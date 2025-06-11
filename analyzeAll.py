import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

task_n = 1 if len(sys.argv) < 2 else int(sys.argv[1])
task1_allFP = f'./in/Task{task_n}FemmesProches.txt'
task1_allFE = f'./in/Task{task_n}FemmesEloignes.txt'
task1_allHP = f'./in/Task{task_n}HommesProches.txt'
task1_allHE = f'./in/Task{task_n}HommesEloignes.txt'
title = f"Task{task_n}" if task_n < 3 else "Tasks"

with open(task1_allFP, 'r') as f:
    data = [line.strip().split('\t') for line in f.readlines()[1:]]
    for row in data:
        row.append("Female - Close")
    df_fp = pd.DataFrame(data, columns=["speaker", "label", "legend"])
    
with open(task1_allFE, 'r') as f:
    data = [line.strip().split('\t') for line in f.readlines()[1:]]
    for row in data:
        row.append("Female - Far")
    df_fe = pd.DataFrame(data, columns=["speaker", "label", "legend"])
    
with open(task1_allHP, 'r') as f:
    data = [line.strip().split('\t') for line in f.readlines()[1:]]
    for row in data:
        row.append("Male - Close")
    df_hp = pd.DataFrame(data, columns=["speaker", "label", "legend"])
    
with open(task1_allHE, 'r') as f:
    data = [line.strip().split('\t') for line in f.readlines()[1:]]
    for row in data:
        row.append("Male - Far")
    df_he = pd.DataFrame(data, columns=["speaker", "label", "legend"])

df = pd.concat([df_fp, df_fe, df_hp, df_he], ignore_index=True)

def generate(full_df, plot_type):
    df_filtered = df[df['label'] == ('?' if plot_type=='other' else plot_type)]

    df_percent = df_filtered.groupby(['speaker', 'legend']).size() / df.groupby(['speaker', 'legend']).size() * 100
    df_percent = df_percent.reset_index(name=f'%{plot_type}')
    # In case there are no FR, OCC or ? for a speaker
    df_percent = df_percent.fillna(0.0)

    quartiles = df_percent.groupby('legend')[f'%{plot_type}'].quantile([0.25, 0.5, 0.75]).unstack()
    quartiles.columns = ['Q1', 'Q2 (Median)', 'Q3']
    quartiles['Type'] = plot_type
    quartiles['Condition'] = quartiles.index
    quartiles = quartiles[['Type', 'Condition', 'Q1', 'Q2 (Median)', 'Q3']]

    desired_order = ["Female - Far", "Female - Close", "Male - Far", "Male - Close"]
    sns.boxplot(data=df_percent, x='legend', y=f'%{plot_type}', hue='legend', palette=["#f8766d", "#00bfc4", "#c77cff", "#7cae00"], legend=False, order=desired_order)

    plt.title(f"{title} %{plot_type} According to Gender and Cultural affiliation")
    plt.xlabel("Condition")
    plt.ylabel(f"% {plot_type}")

    plt.savefig(f"./out/{title}/{title}_{plot_type}_all.png", dpi=300)
    plt.close()
    
    return quartiles
    
stats_occ = generate(df, 'OCC')
stats_fr = generate(df, 'FR')
stats_other = generate(df, 'other')
stats_df = pd.concat([stats_occ, stats_fr, stats_other], ignore_index=True)
stats_df.to_csv(f"./out/{title}/{title}_All_stats.csv", index=False)
