
from argparse import ArgumentParser

def parse_arguments():
    argparser = ArgumentParser()
    argparser.add_argument(
        "-c",
        "--config-path",
        dest="config_path",
        type=str,
        required=True,
        help="Path to the .yaml file containing LMAO configuration",
    )

    argparser.add_argument(
        "--record",
        nargs="?",
        default=False,
        const="debug",
        help="Record telemetry, photos and calculated positions into a folder. The default path is `debug`, "
        "but you can specify a different one. The saved information can be later used "
        "for analyzing performance and mission playback using the `--playback` option.",
    )

    argparser.add_argument(
        "--playback",
        nargs="?",
        default=False,
        const="debug",
        help="Launch LMAO in mission playback mode. This takes information from a folder and uses "
        "it as input to simulate how the system would react in a real mission. The default folder "
        "path is `debug`, but you can specify a different one.",
    )

    return argparser.parse_args()