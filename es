#! /bin/sh


cd "$SCRIPTS" || exit 1
# "if then else fi", although marginally faster, is very ugly
[ "$EDITOR" = vim ] && printf "%s\n" "$@" | xargs -ro "$EDITOR" -p
[ "$EDITOR" = vim ] || printf "%s\n" "$@" | xargs -roL1 "$EDITOR"

[ "$#" -eq 0 ] || exit 1


./snow
exit 0

files="$(find "." -type f \
    | grep -v /.git \
    | sort \
    | fzf -e -i -m --preview "head -60 {}")"

# "if then else fi", although marginally faster, is very ugly
[ "$EDITOR" = vim ] && printf '%s' "$files" | xargs -ro "$EDITOR" -p
[ "$EDITOR" = vim ] || printf '%s' "$files" | xargs -roL1 "$EDITOR"

