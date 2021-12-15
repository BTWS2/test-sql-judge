#!/usr/bin/python
import os
import json
import shutil

script_path = os.path.dirname(os.path.realpath(__file__))

for filename in os.listdir(script_path):
    if filename[0] == "_":
        continue

    subdir_path = os.path.join(script_path, filename)

    if not os.path.isdir(subdir_path):
        continue

    config_json = os.path.join(subdir_path, "config.json")
    with open(config_json, "r") as f:
        config = json.load(f)

    solution_dir = os.path.join(subdir_path, "solution")
    solutions = os.listdir(solution_dir)
    solutions = [sol.removesuffix(".sql") for sol in solutions]
    solutions = ["OK" if sol == "solution" else sol for sol in solutions]

    # reset names
    config["description"]["names"]["nl"] = filename
    config["description"]["names"]["en"] = filename

    if len(solutions) > 1:
        config["description"]["names"]["nl"] += f"({','.join(solutions)})"
        config["description"]["names"]["en"] += f"({','.join(solutions)})"

    with open(config_json, "w") as f:
        json.dump(config, f, indent=2)
