#
#   Pull settings, including 'secrets', from local dot file
#

import configparser
import os
import sys
import json

config = configparser.ConfigParser()
config_dir = os.path.expanduser("~/.auto-luc/")
full_path = config_dir + "config"

settings = [
    "REDDIT_CLIENT_SECRET",
    "REDDIT_CLIENT_ID",
    "REDDIT_USER_AGENT",
    "REDDIT_USERNAME",
    "REDDIT_PASSWORD",
    "GITHUB_ACCESS_TOKEN",
]

"""
The ~/.auto-luc/config file is essentially in ".ini" format, like this: 
        [Global]

        # Reddit
        REDDIT_CLIENT_ID = "ABC998EDILHGA"
        REDDIT_CLIENT_SECRET = "ZXCbhRmoLZo4xAIRD754aC3YaQ0"
        REDDIT_USER_AGENT = "thud"
        REDDIT_USERNAME = "smellytoes"
        REDDIT_PASSWORD = "tuulip99Wanderspring!"

        # GitHub
        GITHUB_ACCESS_TOKEN = "fbb9fe26660855920b5dfa098755391095e413d"

(NB these creds are bogus)
"""



try:
    config.read(full_path)
    REDDIT_CLIENT_SECRET = json.loads(config.get("Global", "REDDIT_CLIENT_SECRET"))

except:
    sys.exit(
        "\n[Error]: ",
        "REDDIT_CLIENT_SECRET",
        " not found.\n"
        "\n   The script expects settings to be stored"
        "\n   in the file: ~/.auto-luc/config "
        "\n",
    )

try:
    config.read(full_path)
    REDDIT_CLIENT_ID = json.loads(config.get("Global", "REDDIT_CLIENT_ID"))

except:
    sys.exit(
        "\n[Error]: ",
        "REDDIT_CLIENT_ID",
        " not found.\n"
        "\n   The script expects settings to be stored"
        "\n   in the file: ~/.auto-luc/config "
        "\n",
    )

try:
    config.read(full_path)
    REDDIT_USER_AGENT = json.loads(config.get("Global", "REDDIT_USER_AGENT"))

except:
    sys.exit(
        "\n[Error]: ",
        "REDDIT_USER_AGENT",
        " not found.\n"
        "\n   The script expects settings to be stored"
        "\n   in the file: ~/.auto-luc/config "
        "\n",
    )

try:
    config.read(full_path)
    REDDIT_USERNAME = json.loads(config.get("Global", "REDDIT_USERNAME"))

except:
    sys.exit(
        "\n[Error]: ",
        "REDDIT_USERNAME",
        " not found.\n"
        "\n   The script expects settings to be stored"
        "\n   in the file: ~/.auto-luc/config "
        "\n",
    )

try:
    config.read(full_path)
    REDDIT_PASSWORD = json.loads(config.get("Global", "REDDIT_PASSWORD"))

except:
    sys.exit(
        "\n[Error]: ",
        "REDDIT_PASSWORD",
        " not found.\n"
        "\n   The script expects settings to be stored"
        "\n   in the file: ~/.auto-luc/config "
        "\n",
    )

try:
    config.read(full_path)
    GITHUB_ACCESS_TOKEN = json.loads(config.get("Global", "GITHUB_ACCESS_TOKEN"))

except:
    sys.exit(
        "\n[Error]: ",
        "GITHUB_ACCESS_TOKEN",
        " not found.\n"
        "\n   The script expects settings to be stored"
        "\n   in the file: ~/.auto-luc/config "
        "\n",
    )

