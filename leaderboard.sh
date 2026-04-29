#!/bin/bash
> tictactoe.ssv
> othello.ssv
> connect4.ssv

#creates winloss.ssv from history.ssv 
awk '
BEGIN{
FS=",";
}
{
    wins[$1" "$4]++;
    losses[$2" "$4]++;
}
END{
    for(i in wins)
        print("wins",i,wins[i])
    for(i in losses)
        print("losses",i,losses[i])
}' history.csv > winloss.ssv #winloss.ssv is in the form "win or loss" "username" "Game" "Number of wins/losses" 

#creates usersfile which contains only usernames 
cut -f1 users.tsv | sort -u > usersfile

#Declares associative arrays for win
declare -A tictactoewins othellowins connect4wins
#Declares associative arrays for loss
declare -A tictactoelosses othellolosses connect4losses
#Declares associative array for win by loss ratio
declare -A tictactoe_wbyl othello_wbyl connect4_wbyl

#Reads winloss.ssv file
while read line; do

#win or loss
    w_l=$(echo "$line" | cut -d " " -f 1)
#username
    user=$(echo "$line" | cut -d " " -f 2)
#Game
    game=$(echo "$line" | cut -d " " -f 3)
#Total no of win or loss in that Game
    no_of_w_l=$(echo "$line" | cut -d " " -f 4)

#Mapping no of wins or losses for paticular user in that Game 
    if [[ $game == "TicTacToe" ]]; then
        if [[ $w_l == "wins" ]]; then
            tictactoewins["$user"]=$no_of_w_l
        else
            tictactoelosses["$user"]=$no_of_w_l
        fi
    elif [[ $game == "Othello" ]]; then
        if [[ $w_l == "wins" ]]; then
            othellowins["$user"]=$no_of_w_l
        else
            othellolosses["$user"]=$no_of_w_l
        fi
    elif [[ $game == "Connect4" ]]; then
        if [[ $w_l == "wins" ]]; then
            connect4wins["$user"]=$no_of_w_l
        else
            connect4losses["$user"]=$no_of_w_l
        fi
    fi
done < winloss.ssv

#Reads userfile which contains usernames
while read line; do

#If losses not equal to 0 then it do wins/losses directly by division for tictactoe
    if (( ${tictactoelosses[$line]:-0} != 0 )); then
        w=${tictactoewins[$line]:-0}
        l=${tictactoelosses[$line]:-0}
	tictactoe_wbyl["$line"]=$(awk -v w="$w" -v l="$l" 'BEGIN { printf "%.2f", w / l }')
    else
    #If win not equal to 0 and loss is 0 then win/loss is inf for tictactoe
        if (( ${tictactoewins[$line]:-0} != 0 )); then
            tictactoe_wbyl["$line"]=inf
        else
        #If both wins and losses equal to 0 then win/loss is NaN for tictactoe
            tictactoe_wbyl["$line"]=NaN
        fi
    fi
    echo "$line ${tictactoewins[$line]:-0} ${tictactoelosses[$line]:-0} ${tictactoe_wbyl[$line]}" >> tictactoe.ssv

#If losses not equal to 0 then it do wins/losses directly by division for othello
    if (( ${othellolosses[$line]:-0} != 0 )); then
        w=${othellowins[$line]:-0}
        l=${othellolosses[$line]:-0}
	othello_wbyl["$line"]=$(awk -v w="$w" -v l="$l" 'BEGIN { printf "%.2f", w / l }')
    else
    #If win not equal to 0 and loss is 0 then win/loss is inf for othello
        if (( ${othellowins[$line]:-0} != 0 )); then
            othello_wbyl["$line"]=inf
        else
        #If both wins and losses equal to 0 then win/loss is NaN for othello
            othello_wbyl["$line"]=NaN
        fi
    fi
    echo "$line ${othellowins[$line]:-0} ${othellolosses[$line]:-0} ${othello_wbyl[$line]}" >> othello.ssv

#If losses not equal to 0 then it do wins/losses directly by division for connect4
    if (( ${connect4losses[$line]:-0} != 0 )); then
        w=${connect4wins[$line]:-0}
        l=${connect4losses[$line]:-0}
	connect4_wbyl["$line"]=$(awk -v w="$w" -v l="$l" 'BEGIN { printf "%.2f", w / l }')
    else
    #If win not equal to 0 and loss is 0 then win/loss is inf for connect4
        if (( ${connect4wins[$line]:-0} != 0 )); then
            connect4_wbyl["$line"]=inf
        else
        #If both wins and losses equal to 0 then win/loss is NaN for connect4
            connect4_wbyl["$line"]=NaN
        fi
    fi
    echo "$line ${connect4wins[$line]:-0} ${connect4losses[$line]:-0} ${connect4_wbyl[$line]}" >> connect4.ssv

done < usersfile

#sorts by wins
if [[ $1 == "wins" ]]; then
    for f in tictactoe.ssv othello.ssv connect4.ssv; do
        sort -t " " -k2,2nr -k3,3n -k1,1 "$f" > temp.ssv
        mv temp.ssv "$f"
    done
#sorts by losses
elif [[ $1 == "losses" ]]; then
    for f in tictactoe.ssv othello.ssv connect4.ssv; do
        sort -t " " -k3,3nr -k2,2n -k1,1 "$f" > temp.ssv
        mv temp.ssv "$f"
    done
#sorts by win by loss ratio
elif [[ $1 == "wbyl" ]]; then
    for f in tictactoe.ssv othello.ssv connect4.ssv; do
        sort -t " " -grk4,4 -k1,1 "$f" > temp.ssv
        mv temp.ssv "$f"
    done
fi

#Prints Tictactoe table 
echo "========= TicTacToe ========="
echo "User Wins Losses W/L" | cat - tictactoe.ssv | column -t

#Prints Othello table
echo "========= Othello ========="
echo "User Wins Losses W/L" | cat - othello.ssv | column -t

#Prints Connect4 table
echo "========= Connect4 ========="
echo "User Wins Losses W/L" | cat - connect4.ssv | column -t

#Removes extra created files
rm -f usersfile winloss.ssv tictactoe.ssv othello.ssv connect4.ssv
