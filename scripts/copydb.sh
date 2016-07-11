#!/bin/bash
set -e

ssh channel2 sudo -i -u postgres pg_dump channel2 > channel2.sql
scp channel2:/root/channel2.sql channel2.sql

psql -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'channel2' AND pid <> pg_backend_pid();"
psql -c "drop database if exists channel2;"
psql -c "create database channel2;"

psql channel2 < channel2.sql
rm -f channel2.sql
