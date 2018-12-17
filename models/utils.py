import json
import re
import datetime
from pathlib import Path


class Utils:

    @staticmethod
    def load_cookies():
        cookie_store = json.loads(Path("cookie.json").read_text())
        cookie_dict = {}
        for cookie in cookie_store:
            cookie_dict[cookie['name']] = cookie['value']
        return cookie_dict

    @staticmethod
    def from_secs_to_time(secs):
        mins = secs / 60
        hours = mins / 60
        secs = secs % 60
        time = datetime.time(int(hours), int(mins), int(secs))
        return time.strftime("%H:%M:%S")

    @staticmethod
    def write_file(path, filename, content):
        completed = False
        path = Path(path)
        if not path.exists():
            print(f"path {path} not exists, creating it...")
            path.mkdir(parents=True)
        try:
            path = Path(path) / filename
            path.write_bytes(content)
            completed = True
        except Exception as ex:
            print("Can't write file! Details: \n{}".format(ex))
        finally:
            if completed:
                print(f"Successfully write file @ {path}")

    @staticmethod
    def get_json_from_callback(string):
        return string[string.index("(") + 1: -1]

    @staticmethod
    def get_id_from_url(url):
        return url[url.rindex('/') + 1:]

    @staticmethod
    def flush(string):
        string = re.sub(r'(\(([\d]+)(.)([\d]+)\))', '', string)  # removes (3:58)
        string = re.sub(r'(\d+)(-)(\s+)', '', string)  # removes 8-
        string = re.sub(r'(\s+){2,}', ' ', string)
        string = re.sub(r'\r?\n\r?', '', string)
        return string.strip()
