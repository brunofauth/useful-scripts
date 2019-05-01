#! /bin/bash


if [ -t 1 ]; then
    in_terminal=true
fi


choose() {
    choices=$(xargs -r -I "{}" echo "{}")
    if [ "$in_terminal" = true ]; then
        echo "$choices" | fzf -e -i --prompt="$1 "
    else
        echo "$choices" | rofi -dmenu -i -p "$1"
    fi
}


scripts=$(find "$HOME/useful-scripts" -type f | grep -ve .git)
file=$(echo "$scripts" | choose "What to edit?")


if [[ -n "$file" ]]; then
    $EDITOR "$file"
fi
