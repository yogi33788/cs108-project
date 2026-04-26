#!/bin/bash

echo "Welcome to Gaming World"
echo "Let go of stress,let the chill begin."

#check_user function checks whether user registerd or not registered
check_user() {
    temp=$(grep "^$1"$'\t' users.tsv)
    
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
	#Enter player username
	read -p "Enter player$player_no username: " user

if check_user "$user"; then #user already registered
        echo "Player already registered."

#Enter player password it will not be shown in terminal
read -s -p "Enter player$player_no password: " pass 
echo ""

#Converts our password into hashed password by using sha256 
hashedpass=$(echo -n "${pass}" | sha256sum | cut -d ' ' -f1 )

#stored password is the sha256 password stored for the user in users.tsv
storedpass=$(grep "^$user"$'\t' users.tsv | cut -d $'\t' -f2 )

	if [[ ${hashedpass} == ${storedpass} ]]; then #If passwords match then login succesful
            echo "${user} login succesful"
            echo "$user"
            return 0        
        else
            echo "Invalid password" #If passwords doesn't match then try again
            echo "Please try again"
        fi
else  #If user not registered

	#Type Y if you want to register
	#if you select otherthan Y it doesn't register
        read -p "You want to register(Y/N): " select
        if [[ "${select}" == "Y" ]]; then 

		#Creates password for the user
                read -s -p "Create password for $user " pass
                echo "" 
                echo -e "${user}\t$(echo -n "${pass}" | sha256sum | cut -d ' ' -f1 )" >> users.tsv #stores hashed password in users.tsv
                echo "Your registration succesfull" 
                echo "$user"
                return 0    
            else
                echo "Player not registered"
        fi
fi
done
}

player1_user=$(player_login "1" | tail -n 1 ) #If player1 logins then player1_user stores player1 username
while true; do 
    player2_user=$(player_login "2" | tail -n 1 ) #If player2 logins then player2_user stores player2 username 
    
#Ensures both players are different
    if [[ $player1_user != $player2_user ]]; then
        echo "You both can start the game"
        break	#If player1 and player2 are different then breaks this loop and call the game.py 
        else #If player1 and player2 are same then player2 need to login again
        echo "Player1 and Player2 are same"
        echo "Player2 need to login again"
    fi
done

python3 game.py "$player1_user" "$player2_user"
