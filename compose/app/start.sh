#!/bin/bash
/app/checkpip.sh
supervisord -c /etc/supervisord.conf
