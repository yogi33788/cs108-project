#!/bin/bash
echo "Welcome to Gaming World"
echo "Let go of stress,let the chill begin."
check_user() {
    temp=$(grep "^$1\t" users.tsv)
    if [[ "${temp}" = "" ]]; then
        return 1
    else 
        return 0
    fi
}
player_login() {
    local player_no=$1
    local user=""
    local pass=""
while true; do
read -p "Enter player$player_no username: " user
if check_user "$user"; then
        echo "Player already registered."
read -s -p "Enter player$player_no password: " pass 
echo ""
hashedpass=$(echo -n "${pass}" | sha256sum | cut -d ' ' -f1 )
storedpass=$(grep "^$user\t" users.tsv | cut -d $'\t' -f2 )
if [[ ${hashedpass} == ${storedpass} ]]; then
        echo "${user} login succesful"
        echo "$user"
        return 0        
    else
        echo "Invalid password"
        echo "Please try again"
fi
    else
        read -p "You want to register(Y/N): " select
        if [[ "${select}" == "Y" ]]; then 
                read -s -p "Create password for $user " pass
                echo "" 
                echo -e "${user}\t$(echo -n "${pass}" | sha256sum | cut -d ' ' -f1 )" >> users.tsv
                echo "Your registration succesfull" 
                echo "$user"
                return 0    
            else
                echo "Player not registered"
        fi
done
}
player1_user=$(player_login "1" | tail -n 1 )
while true; do 
    player2_user=$(player_login "2" | tail -n 1 )
    if [[ $player1_user != $player2_user ]]; then
        echo "You both can start the game"
        break
        else
        echo "Player1 and Player2 are same"
        echo "Player2 need to login again"
    fi
done
game.py "$player1_user" "$player2_user"
