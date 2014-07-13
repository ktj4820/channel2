#!/bin/bash
set -e

psql -c "drop database if exists channel2;"
psql -c "create database channel2;"
psql -d channel2 < dump.sql
