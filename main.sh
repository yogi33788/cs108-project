#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Welcome to the Mini Game Hub${NC}"

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
    read -p "$(echo -e "${YELLOW}Enter player$player_no username: ${NC}")" user

if check_user "$user"; then #user already registered
        #echo -e "${GREEN}Player already registered.${NC}" 

#Enter player password it will not be shown in terminal
read -s -p "$(echo -e "${YELLOW}Enter player$player_no password: ${NC}")" pass 
echo "" >&2

#Converts our password into hashed password by using sha256 
hashedpass=$(echo -n "${pass}" | sha256sum | cut -d ' ' -f1 )

#stored password is the sha256 password stored for the user in users.tsv
storedpass=$(grep "^$user"$'\t' users.tsv | cut -d $'\t' -f2 )

    if [[ ${hashedpass} == ${storedpass} ]]; then #If passwords match then login succesful
            echo "" >&2
            echo -e "${GREEN}${user} logged in succesfully${NC}" >&2
            echo "$user" 
            return 0        
        else
            echo -e "${RED}Invalid password!!${NC}" >&2 #If passwords doesn't match then try again
            echo -e "${RED}< Please try again >${NC}" >&2
        fi
else  #If user not registered

    #Type Y if you want to register
    #if you select otherthan Y it doesn't register
        read -p "$(echo -e "${YELLOW}Do you want to register ? (Y/N): ${NC}")" select
        if [[ "${select}" == "Y" ]]; then 

        #Creates password for the user
                read -s -p "$(echo -e "${YELLOW}Create a password for $user ${NC}")" pass
                echo "" >&2
                echo -e "${user}\t$(echo -n "${pass}" | sha256sum | cut -d ' ' -f1 )" >> users.tsv #stores hashed password in users.tsv
                echo -e "${GREEN}Your registration is succesfull${NC}" >&2
                echo "$user"
                return 0    
            else
              echo -e "${RED}Player not registered${NC}" >&2
        fi
fi
done
}

player1_user=$(player_login "1" | tail -n 1 ) #If player1 logins then player1_user stores player1 username
while true; do 
    player2_user=$(player_login "2" | tail -n 1 ) #If player2 logins then player2_user stores player2 username 
    
#Ensures both players are different
    if [[ $player1_user != $player2_user ]]; then
        echo -e "${GREEN}You both can start the game${NC}" >&2
        break   #If player1 and player2 are different then breaks this loop and call the game.py 
        else #If player1 and player2 are same then player2 need to login again
        echo -e "${RED}Player1 is same as player2${NC}" >&2
        echo -e "${RED}Player2 need to login again${NC}" >&2
    fi
done

python3 game.py "$player1_user" "$player2_user"
