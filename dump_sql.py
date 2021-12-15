#!/usr/bin/python
import os
import json
import shutil
import subprocess
from types import SimpleNamespace

script_path = os.path.dirname(os.path.realpath(__file__))

full_list = {}

for filename in os.listdir(script_path):
    if filename[0] == "_":
        continue

    subdir_path = os.path.join(script_path, filename)

    if not os.path.isdir(subdir_path):
        continue

    config_json = os.path.join(subdir_path, "config.json")
    with open(config_json, "r") as f:
        config = json.load(f)
    
    config = config.get("evaluation", {})

    evaluation_path = os.path.join(subdir_path, "evaluation")
    config.update(
        {
            "resources": evaluation_path,
        }
    )

    config = SimpleNamespace(**config)

    if hasattr(config, "database_files"):
        config.database_files = [
            (str(filename), os.path.join(config.resources, filename)) for filename in config.database_files
        ]
    else:
        config.database_dir = str(getattr(config, "database_dir", "."))
        config.database_dir = os.path.join(config.resources, config.database_dir)

        if not os.path.exists(config.database_dir):
            continue

        config.database_files = [
            (filename, os.path.join(config.database_dir, filename))
            for filename in sorted(os.listdir(config.database_dir))
            if filename.endswith(".sqlite")
        ]

    construct_db_path = os.path.join(subdir_path, "construct_db")

    hashes = {}

    os.makedirs(construct_db_path, exist_ok=True)
    for name, path in config.database_files:
        if not os.path.exists(path):
            continue

        sql_path = os.path.join(construct_db_path, os.path.basename(name) + ".sql")

        dump = subprocess.run(["sqlite3", path, ".dump"], capture_output=True)

        with open(sql_path, 'w') as f:
            f.write(dump.stdout.decode('utf8'))

        new_name = os.path.relpath(path, subdir_path + "/evaluation")
        print(new_name)
        hashes[new_name] = subprocess.run(["sha1sum", sql_path], capture_output=True).stdout.decode('utf8').split()[0]

        full_list[hashes[new_name]] = path

    construct_db_json_path = os.path.join(subdir_path, "construct_db.json")
    
    temp = [os.path.relpath(path, subdir_path + "/evaluation") for name, path in config.database_files if os.path.exists(path)]

    temp = {path: os.path.basename(path) + ".sql" for path in temp }

    with open(construct_db_json_path, 'w') as f:
        json.dump(temp, f)


databases_path = os.path.join(script_path, "_databases")
for hash, path in full_list.items():
    print(hash, path)

    databases_path_file = os.path.join(databases_path, os.path.basename(path))

    shutil.copy(path, databases_path_file)
