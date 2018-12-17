import json
from multiprocessing import Process
from multiprocessing.pool import ThreadPool
from pathlib import Path

import urllib3

from models.downloader import Downloader

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_metadata(metadata):
    for course in metadata:
        if len(course.get("lectures")) == 0:
            metadata.remove(course)
    Path('metadata.json').write_text(json.dumps(metadata, indent=4))
    print("Cleaning metadata on './metadata.json'")


def main():

    metadata = []
    loader = Downloader()

    if Path('metadata.json').exists():
        metadata = json.loads(Path('metadata.json').read_text())
        if len(metadata) > 0:
            for course in metadata:
                if len(course.get('lectures')) > 0:
                    print(f'#{course.get("course_id")} - {course.get("course_title")} is already loading, skipping...')
                    continue
                else:
                    check_metadata(metadata)
                    metadata = json.loads(Path('metadata.json').read_text())
                    loader.download_metadata()
    else:
        loader.download_metadata()


    for course in metadata:
        p = Process(target=loader.download_course, args=(course,))
        p.start()
        p.join()


if __name__ == "__main__":
    main()
