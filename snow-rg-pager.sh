#! /bin/sh


cut -d: -f-2 --output-delimiter=' ' - | while read -r file line_number; do
    bat \
        --color=always \
        --paging=never \
        --style=numbers \
        --highlight-line="$line_number" \
        "$file" \
    | less -R +"$line_number"Gu
done

