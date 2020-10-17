#!/usr/bin/bash
if [ $1 == 'compile' ]; then
    snapcraft clean
    multipass launch --name snapcraft-writernote --cpus 18 --mem 18G --disk 100G
    snapcraft

elif [$1 == 'clean']; then
    snapcraft clean

elif [$1 == 'create']; then
    multipass launch --name snapcraft-writernote --cpus 18 --mem 18G --disk 100G
fi

