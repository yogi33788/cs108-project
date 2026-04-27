import csv
import matplotlib.pyplot as plt
from collections import Counter

#creates empty list 
winner = []
wins = []
game = []
Game = []
freq = []
player = []

#Reads history.csv 
with open("history.csv",mode="r",newline='') as file:
    csvfile = csv.reader(file)
    for line in csvfile:
        if line:
            winner.append(line[0])
            game.append(line[3])

#counts top5 total wins
count_win = Counter(winner) #creates dictionary
top5_wins = count_win.most_common(5) 

for key, value in top5_wins:
    player.append(key)
    wins.append(value)

#games list by frequency
count_game = Counter(game)

for key, value in count_game.items():
    Game.append(key)
    freq.append(value)

#Bar graph for top5 total wins
plt.bar(player,wins,color ='r',width=0.5)
plt.title("Top 5 Players by total Wins")
plt.xlabel("PLAYER")
plt.ylabel("No of Wins")
plt.show()

#Pie chart of most played games by freaquency
plt.pie(freq,labels=Game)
plt.show()
