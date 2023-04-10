#! /bin/sh


preview_for_binary() {

    if [ "$SNOW_RUN_BIN" -eq 1 ]; then

        out="$("$1" --help 2>&1)"
        [ $? -eq 0 ] && echo "$out" && return

        out="$("$1" -h 2>&1)"
        [ $? -eq 0 ] && echo "$out" && return
    fi

    out="$(man "$1" 2>&1)"
    [ $? -eq 0 ] && echo "$out" && return

    echo "No suitable preview for binary: '$1'"
}

file_type="$(file --mime-type --brief "$1")"
case "$file_type" in
    text/*) bat --color always --style="numbers" "$1";;
    application/x-shellscript) bat --color always --style="numbers" "$1";;
    application/x-perl) bat --color always --style="numbers" "$1";;
    application/pdf) pdftotext "$1" - || pdfinfo "$1" ;;
    application/zip) zipinfo "$1" ;;
    image/*) iinfo "$1" ;;
    video/*) ffprobe -hide_banner "$1" ;;
    audio/*) ffprobe -hide_banner "$1" ;;
    application/x-pie-executable) preview_for_binary "$1" ;;
    *) echo "No suitable preview for file of type: $file_type"
esac

