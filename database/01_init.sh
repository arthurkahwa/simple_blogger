echo "-= Running create database script =-"
psql < /usr/src/init/01_schema.sql

echo "-= Add ample data =-"
psql < /usr/src/init/02_sample_data.sql

psql < /usr/src/init/03_read.sql