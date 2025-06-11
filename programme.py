import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Modify these lines to change the graphs
task = 1
def main():
    display("%?")  # Change to "%FR" or "%OCC" to display those graphs


task1WomenLowDeg = pd.read_csv("T/Task1/Task1WomenLow.txt", delimiter=";", skiprows=1, header=None)
task1MenLow = pd.read_csv("T/Task1/Task1MenLow.txt", delimiter=";", skiprows=1, header=None)
task1WomenHighDeg = pd.read_csv("T/Task1/Task1WomenHigh.txt", delimiter=";", skiprows=1, header=None)
task1ManHighDeg = pd.read_csv("T/Task1/Task1MenHigh.txt", delimiter=";", skiprows=1, header=None)
task2WomenLowDeg = pd.read_csv("T/Task2/Task2WomenLow.txt", delimiter=";", skiprows=1, header=None)
task2MenLow = pd.read_csv("T/Task2/Task2MenLow.txt", delimiter=";", skiprows=1, header=None)
task2WomenHighDeg = pd.read_csv("T/Task2/Task2WomenHigh.txt", delimiter=";", skiprows=1, header=None)
task2ManHighDeg = pd.read_csv("T/Task2/Task2MenHigh.txt", delimiter=";", skiprows=1, header=None)


if task == 1:
    taskWomenLowDeg = task1WomenLowDeg
    taskMenLow = task1MenLow
    taskWomenHighDeg = task1WomenHighDeg
    taskManHighDeg = task1ManHighDeg
elif task == 2:
    taskWomenLowDeg = task2WomenLowDeg
    taskMenLow = task2MenLow
    taskWomenHighDeg = task2WomenHighDeg
    taskManHighDeg = task2ManHighDeg
else:
    raise ValueError("Invalid task number. Please choose 1 or 2.")


GroupBy1 = taskWomenLowDeg.groupby([0,1]).size().reset_index(name='count')
result1 = GroupBy1.pivot(index=0, columns=1, values='count').fillna(0)
result1["Culture"] = ["LowDeg"] * len(result1)
result1["Gender"] = ["Woman"] * len(result1)


GroupBy2 = taskWomenHighDeg.groupby([0,1]).size().reset_index(name='count')
result2 = GroupBy2.pivot(index=0, columns=1, values='count').fillna(0)
result2["Culture"] = ["HighDeg"] * len(result2)
result2["Gender"] = ["Woman"] * len(result2)


GroupBy3 = taskMenLow.groupby([0,1]).size().reset_index(name='count')
result3 = GroupBy3.pivot(index=0, columns=1, values='count').fillna(0)
result3["Culture"] = ["LowDeg"] * len(result3)
result3["Gender"] = ["Man"] * len(result3)


GroupBy4 = taskManHighDeg.groupby([0,1]).size().reset_index(name='count')
result4 = GroupBy4.pivot(index=0, columns=1, values='count').fillna(0)
result4["Culture"] = ["HighDeg"] * len(result4)
result4["Gender"] = ["Man"] * len(result4)
# print(result4) # ça marche bien

result = pd.concat([result1, result2, result3, result4], axis=0, ignore_index=False)
print(result)

data = [
    [float(100*line[0]/(line[0]+line[1]+line[2])), float(100*line[1]/(line[0]+line[1]+line[2])), float(100*line[2]/(line[0]+line[1]+line[2])), str(line[3]), str(line[4])] for line in result.itertuples(index=False, name=None)
]
# data = np.array(data)

print(data) #     %? then %FR then %OCC then Culture then Gender

WomenLow = []
WomenHigh = []
MenLow = []
MenHigh = []
for d in data:
    if d[3] == "LowDeg" and d[4] == "Woman":
        WomenLow.append(d[:3])
    elif d[3] == "HighDeg" and d[4] == "Woman":
        WomenHigh.append(d[:3])
    elif d[3] == "LowDeg" and d[4] == "Man":
        MenLow.append(d[:3])
    elif d[3] == "HighDeg" and d[4] == "Man":
        MenHigh.append(d[:3])

def display(y):
    # y shall be %? or %FR or %OCC
    if y == "%?":
        yy = 0
    elif y == "%FR":
        yy = 1
    elif y == "%OCC":
        yy = 2
    else:
        raise ValueError("Invalid y-axis label. Choose '%?', '%FR', or '%OCC'.")
    plt.boxplot(WomenLow[:][yy], positions=[1], widths=0.5)
    plt.boxplot(WomenHigh[:][yy], positions=[2], widths=0.5)
    plt.boxplot(MenLow[:][yy], positions=[3], widths=0.5)
    plt.boxplot(MenHigh[:][yy], positions=[4], widths=0.5)
    plt.gca().xaxis.set_ticklabels(['Women Low Degree of Culture', 'Women High Degree of Culture ', 'Men Low Degree of Culture', 'Men High Degree of Culture']) 
    plt.ylabel(y)
    plt.show()

if __name__ == "__main__":
    main()