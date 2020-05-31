#! /bin/sh


cd "$SCRIPTS" || exit 1

# if then else fi, although marginally faster, is very ugly
[ "$EDITOR" = vim ] && printf "%s\n" "$@" | xargs -ro "$EDITOR" -p
[ "$EDITOR" = vim ] || printf "%s\n" "$@" | xargs -roL1 "$EDITOR"

[ "$#" -eq 0 ] || exit 1


find "." -type f -print0 \
    | grep -zv /.git \
    | sort -z \
    | fzf -e -i -m --preview "head -60 {}" --read0 --print0 \
    | xargs -r0L 1 -I {} sh -c "</dev/tty '$EDITOR' '{}'"

