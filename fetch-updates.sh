#! /bin/sh


export DISPLAY=:0


notify_user() (
    local user; user="$1"; shift
    sudo -u "$user" -- env "DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id --user "$user")/bus" \
        notify-send --expire-time=3000 "$@"
)

notify_all() {
    for user in $(users); do
        notify_user "$user" "$@"
    done
}

notify_all \
    --icon=dialog-information \
    "Fetching package updates."

pacman_output="$(nice -n 10 sudo -- pacman -Syuw --noconfirm --color=always)"
pacman_status=$?
log_file="$(mktemp --tmpdir anacron-fetch-updates-XXXXXX)"
echo "$pacman_output" > "$log_file"

if [ $pacman_status -eq 0 ]; then
    notify_all \
        --icon=dialog-information \
        "Finished fetching updates" 
    exit $pacman_status
fi


notify_error() (
    local user; user="$1"
    local action; action="$(\
        notify_user "$user" \
            --icon=dialog-error \
            --action=copy-to-cb="Copy log filepath to clipboard"\
            "Error fetching package updates" \
            "Log file: '$log_file'" \
    )"

    case "$action" in
        copy-to-cb)
            touch "$log_file.lock"
            echo "$log_file" | sudo -u "$user" -- xsel -ib
            exit 0
            ;;
        *)
            notify_user \
                --icon=dialog-error \
                "Unexpected action chosen" \
                "Bad action: '$action'"
            exit 1
            ;;
    esac
)

for user in $(users); do
    notify_error "$user" &
done

if ! [ -f "$log_file.lock" ]; then
    rm "$log_file"
fi

exit 1

