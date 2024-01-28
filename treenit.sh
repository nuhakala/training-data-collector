#!/bin/bash

# If the env variable is not null, use it. Otherwise use the given default value.
path="${TRAINING_FILE:=~/treenit.csv}" 

echo_last_training () {
    line=$(tail -1 ${TRAINING_FILE})
    echo "Edellinen treenikerta ${line::10}."

    type=${line:11:1}
    case ${type} in
        "y")
            echo "Edellinen treeni oli ylävartalo."
            ;;
        "j")
            echo "Edellinen treeni oli juoksu."
            ;;
        "h")
            echo "Edellinen treeni oli hiihto."
            ;;
        "a")
            echo "Edellinen treeni oli jalkatreeni."
            ;;
        *)
            echo "Tuntematon"
            ;;
    esac
}

# If 0 arguments
if [ $# -eq 0 ]; then
    echo_last_training
    python ~/OmatProjektit/training-diary/training.py
elif [[ "$1" = "last" ]]; then
    echo_last_training
fi
