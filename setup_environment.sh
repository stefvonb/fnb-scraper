#!/bin/bash

echo -n "Enter your FNB username: "
read username

echo -n "Enter your FNB password: "
read -s password

export FNB_USERNAME=$username
export FNB_PASSWORD=$password

