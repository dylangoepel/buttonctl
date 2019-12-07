#!/bin/bash
# Generate systemd service file

FILE=/lib/systemd/system/buttond.service

generate() {
	echo [Unit]
	echo Description = buttonctl
	echo
	echo [Service]
	echo ExecStart = /usr/bin/python3 $PWD/button.py
	echo Type = simple
	echo
	echo [Install]
	echo WantedBy=multi-user.target
	echo Alias=buttond.service
}

if test -f $FILE
then
	rm $FILE
fi
touch $FILE
generate >> $FILE
