import logging
import requests
import json
import os

import zipfile


_logger = logging.getLogger(f"--> {__name__}  ")


def make_zip_file(route, delete_input_file=False) -> tuple[bool, str]:
    """get file route, make zip file and save to courent route \n
    return True, new_file_name |or| return False, 'None' \n
    sample: istrue, file_name = make_zip(./test.txt)

    To send a file in Telegram, this file must be zipped
    """

    # input: /home/onion/text.py ooutput: text.zip
    new_file_name = os.path.splitext(os.path.basename(route))[0]
    new_file_name = f"{new_file_name}.zip"

    if not os.path.isfile(route):
        _logger.debug("make_zip_file: is not a file")
        return False, "is not a file"

    try:
        with zipfile.ZipFile(
            new_file_name, "w", compression=zipfile.ZIP_DEFLATED
        ) as zf:
            zf.write(route, os.path.basename(route))

        if delete_input_file:
            os.remove(route)

        return True, new_file_name

    except Exception as error:
        _logger.debug(f"make_zip_file: {error}")
        return False, error


def upload_server_1(
    file: bytes, file_name: str, time_out: int = 1200, file_type: str = "zip"
) -> tuple[bool, str]:
    # time_out 1200 s == 20 min
    """api for upload zip file and return download link \n
    size limit 5GB
    """
    select_storage = requests.post("https://ufile.io/v1/upload/select_storage")

    if select_storage.status_code == 200:
        storageBaseUrl = select_storage.json()["storageBaseUrl"]
    else:
        _logger.debug(f"upload_server_1.select_storage error")
        storageBaseUrl = "https://store-eu-hz-1.ufile.io/"  # default storage

    create_session_api = f"{storageBaseUrl}v1/upload/create_session"
    chunk_api = f"{storageBaseUrl}v1/upload/chunk"  # Send part of the file
    finalise_api = f"{storageBaseUrl}v1/upload/finalise"
    file_size = {"file_size": len(file)}
    files = {"file": file}

    # create session for upload file
    # TODO: add for lop for get a session
    try:
        session = requests.post(create_session_api, data=file_size, timeout=30)
        if session.status_code != 200:
            _logger.debug(
                f"upload_server_1.create session: status code: {session.status_code}, text: {session.text}"
            )
            return False, "upload_server_1.create_session error"
        # session FUID:
        FUID = json.loads(session.text)["fuid"]
    except Exception as error:
        _logger.debug(f"upload_server_1.create session: {error}")
        return False, "upload_server_1.create session error"

    # upload file
    # TODO: Divide the data into small pieces and upload them
    try:
        chunk_data = {"chunk_index": 1, "fuid": FUID}
        chunk_res = requests.post(
            chunk_api, data=chunk_data, files=files, timeout=time_out
        )
        if chunk_res.status_code != 200:
            _logger.debug(
                f"upload_server_1.upload file: status code: {chunk_res.status_code}, text: {chunk_res.text}"
            )
            return False, "upload_server_1.upload file error"
    except Exception as error:
        _logger.debug(f"upload_server_1.upload file : {error}")
        return False,  "upload_server_1.upload file error"

    # close session
    try:
        finalise_headers = {
            "fuid": FUID,
            "file_name": file_name,
            "file_type": file_type,
            "total_chunks": 1,
        }

        finalis_res = requests.post(finalise_api, data=finalise_headers, timeout=30)
        if finalis_res.status_code != 200:
            _logger.debug(
                f"upload_server_1.close session , status code: {finalis_res.status_code}, text: {finalis_res.text}"
            )
            return False , "upload_server_1.close session error"
    except Exception as error:
        _logger.debug(f"upload_server_1.close session error: {error}")
        return False, "upload_server_1.close session error"

    # extract download link
    try:
        download_link = json.loads(finalis_res.text)
        response = ""
        for key, value in download_link.items():
            response = response + f"\n{key}: {value}"
        return True, response
        
    except Exception as error:
        _logger.debug(f"upload_server_1.extract download link error: {error}")
        return False, "upload_server_1.extract download link error"
