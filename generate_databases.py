#!/usr/bin/python
import os
import json
import sqlite3
import shutil

script_path = os.path.dirname(os.path.realpath(__file__))
databases_path = os.path.join(script_path, "_databases")

# generate sqlite files
for filename in os.listdir(databases_path):
    if not filename.endswith(".sql"):
        continue

    sql_file = os.path.join(databases_path, filename)
    sqlite_file = os.path.join(databases_path, filename.removesuffix(".sql"))

    if os.path.exists(sqlite_file):
        continue
    
    with sqlite3.Connection(sqlite_file) as connection:
        with open(sql_file, "r") as f:
            connection.executescript(f.read())

# copy sqlite files to correct locations
for filename in os.listdir(script_path):
    if filename[0] == "_":
        continue

    subdir_path = os.path.join(script_path, filename)

    if not os.path.isdir(subdir_path):
        continue

    construct_db_json = os.path.join(subdir_path, "construct_db.json")
    with open(construct_db_json, "r") as f:
        construct_db = json.load(f)
    
    for path, sql_filename in construct_db.items():
        sqlite_filename = sql_filename.removesuffix(".sql")
        sqlite_file = os.path.join(databases_path, sqlite_filename)
        dest_path = os.path.join(subdir_path, "evaluation", path)

        shutil.copy(sqlite_file, dest_path)
