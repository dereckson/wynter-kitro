#!/bin/sh

set -e

SOURCE_DIR=$(xdg-user-dir PICTURES)
TARGET_ROOT_DIR=$(organize-folders get screenshots)

###
### GNOME screenshots
###

for f in "$SOURCE_DIR"/Screenshot\ from\ *.png; do
    [ -e "$f" ] || break

    YYYY=$(echo "$f" | awk '{print substr($(NF-1), 1, 4)}')
    MM=$(echo "$f" | awk '{print substr($(NF-1), 6, 2)}')
    TARGET_DIR="$TARGET_ROOT_DIR/$YYYY/$MM"

    mkdir -p "$TARGET_DIR/" && mv "$f" "$TARGET_DIR/"
done

###
### Other formats? You can use:
###
### stat --format="mv '%n' 'screenshot-%y.png'" Sc*.png | sh
###
