#! /bin/sh

file_type="$(file --mime-type --brief "$1")"
case "$file_type" in
    text/*) bat --color always --wrap character --style="numbers" "$1";;
    application/x-shellscript) bat --color always --wrap character --style="numbers" "$1";;
    application/x-perl) bat --color always --wrap character --style="numbers" "$1";;
    application/pdf) pdftotext "$1" - ;;
    image/*) kitty +kitten icat --clear --transfer-mode file --silent "$1" ;;
    *) echo "No suitable preview for file of type: $file_type"
esac

