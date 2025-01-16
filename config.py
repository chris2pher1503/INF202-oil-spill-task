import toml
import os
import argparse


def parseInput():
    parser = argparse.ArgumentParser(
        description=" input config file name with -f or --file"
    )
    parser.add_argument(
        "-c", "--config", default="input.toml", type=str, help="input config file name"
    )
    parser.add_argument(
        "-f", "--file", type=str, help="folder including the config file"
    )
    parser.add_argument("--find-all", action="store_true", help="find all files")
    args = parser.parse_args()
    return args


def readConfig(name):
    if not os.path.exists(name):
        raise FileNotFoundError(f"The config file {name} does not exist.")

    with open(name, "r") as file:
        config = toml.load(file)

    geometry = config["geometry"]
    fish_area = geometry.get("fish_area")
    start_point = geometry.get("initial_oil_area")
    filepath = geometry.get("filepath")

    settings = config["settings"]
    steps = settings.get("nSteps")
    t_start = settings.get("t_start", 0)
    t_end = settings.get("t_end")

    IO = config["IO"]
    writeFrequency = IO["writeFrequency"]
    restartFile = IO["restartFile"]
    logName = IO["logName"]

    if not filepath or not os.path.exists(filepath):
        raise FileNotFoundError(f"The mesh file {filepath} does not exist.")

    if not fish_area:
        raise ValueError("Missing fish_area in geometry section.")

    if not start_point:
        raise ValueError("Missing initial_oil_area in geometry section.")

    if not steps or steps <= 0:
        raise ValueError("Missing nSteps in settings section.")

    if restartFile and not t_start:
        raise ValueError("if restarFile given, must give t_start.")

    if t_end is None or t_end <= t_start:
        raise ValueError("Missing t_end in or t_end <= t_start in settings section.")

    if not writeFrequency:
        writeFrequency = -1000

    if not restartFile:
        t_start = 0

    if not logName:
        logName = "logfile.log"

    return config
