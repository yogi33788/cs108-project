#!/bin/bash
> tictactoe.ssv
> othello.ssv
> connect4.ssv
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
}' history.csv > winloss.ssv
cut -f1 users.tsv | sort -u > usersfile

declare -A tictactoewins othellowins connect4wins
declare -A tictactoelosses othellolosses connect4losses
declare -A tictactoe_wbyl othello_wbyl connect4_wbyl

while read -r line; do

    user=$(echo "$line" | cut -d " " -f 2)
    w_l=$(echo "$line" | cut -d " " -f 1)
    game=$(echo "$line" | cut -d " " -f 3)
    no_of_w_l=$(echo "$line" | cut -d " " -f 4)

    if [[ $game == "tictactoe" ]]; then
        if [[ $w_l == "wins" ]]; then
            tictactoewins["$user"]=$no_of_w_l
        else
            tictactoelosses["$user"]=$no_of_w_l
        fi
    elif [[ $game == "othello" ]]; then
        if [[ $w_l == "wins" ]]; then
            othellowins["$user"]=$no_of_w_l
        else
            othellolosses["$user"]=$no_of_w_l
        fi
    elif [[ $game == "connect4" ]]; then
        if [[ $w_l == "wins" ]]; then
            connect4wins["$user"]=$no_of_w_l
        else
            connect4losses["$user"]=$no_of_w_l
        fi
    fi
done < winloss.ssv

while read -r line; do

    if (( ${tictactoelosses[$line]:-0} != 0 )); then
        w=${tictactoewins[$line]:-0}
        l=${tictactoelosses[$line]:-0}
        tictactoe_wbyl["$line"]=$(echo "scale=2; $w / $l" | bc)
    else
        if (( ${tictactoewins[$line]:-0} != 0 )); then
            tictactoe_wbyl["$line"]=inf
        else
            tictactoe_wbyl["$line"]=NaN
        fi
    fi
    echo "$line ${tictactoewins[$line]:-0} ${tictactoelosses[$line]:-0} ${tictactoe_wbyl[$line]}" >> tictactoe.ssv

    if (( ${othellolosses[$line]:-0} != 0 )); then
        w=${othellowins[$line]:-0}
        l=${othellolosses[$line]:-0}
        othello_wbyl["$line"]=$(echo "scale=2; $w / $l" | bc)
    else
        if (( ${othellowins[$line]:-0} != 0 )); then
            othello_wbyl["$line"]=inf
        else
            othello_wbyl["$line"]=NaN
        fi
    fi
    echo "$line ${othellowins[$line]:-0} ${othellolosses[$line]:-0} ${othello_wbyl[$line]}" >> othello.ssv

    if (( ${connect4losses[$line]:-0} != 0 )); then
        w=${connect4wins[$line]:-0}
        l=${connect4losses[$line]:-0}
        connect4_wbyl["$line"]=$(echo "scale=2; $w / $l" | bc)
    else
        if (( ${connect4wins[$line]:-0} != 0 )); then
            connect4_wbyl["$line"]=inf
        else
            connect4_wbyl["$line"]=NaN
        fi
    fi
    echo "$line ${connect4wins[$line]:-0} ${connect4losses[$line]:-0} ${connect4_wbyl[$line]}" >> connect4.ssv

done < usersfile

if [[ $1 == "wins" ]]; then
    for f in tictactoe.ssv othello.ssv connect4.ssv; do
        sort -t " " -k1,1 -k3,3n -k2,2nr "$f" > temp.ssv
        mv temp.ssv "$f"
    done
elif [[ $1 == "losses" ]]; then
    for f in tictactoe.ssv othello.ssv connect4.ssv; do
        sort -t " " -k1,1 -k2,2n -k3,3nr "$f" > temp.ssv
        mv temp.ssv "$f"
    done
elif [[ $1 == "wbyl" ]]; then
    for f in tictactoe.ssv othello.ssv connect4.ssv; do
        sort -t " " -k1,1 -grk4,4 "$f" > temp.ssv
        mv temp.ssv "$f"
    done
fi

echo "=== TicTacToe ==="
echo "User Wins Losses W/L" | cat - tictactoe.ssv | column -t

echo "=== Othello ==="
echo "User Wins Losses W/L" | cat - othello.ssv | column -t

echo "=== Connect4 ==="
echo "User Wins Losses W/L" | cat - connect4.ssv | column -t

rm usersfile

