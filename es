#! /usr/bin/env sh


for script in "$@"; do
    if [ -e "$SCRIPTS/$script" ]; then
        "$EDITOR" "$SCRIPTS/$script" 
    fi
done


if [ "$#" -eq 0 ]; then
    find "$SCRIPTS" -type f -print0 \
        | grep -zve .git \
        | sort -z \
        | fzf -e -i -m --read0 --print0 \
        | xargs -r0L 1 -I {} sh -c "</dev/tty '$EDITOR' '{}'"
fi

