import os
from glob import glob
from dotenv import load_dotenv
load_dotenv(".env")


IS_LOCAL = os.uname().nodename == "MacBook-Air.local"
if IS_LOCAL:
    os.environ["IS_LOCAL"] = "True"
    os.environ["FONTPATHDIR"] = "/System/Library/Fonts/"
    os.environ["TMP_DIR"] = ""
    os.environ["BROKER_URL"] = "redis://localhost"
    os.environ["DOWNLOAD_LIST"] = glob("telop_*.mp4")

else:
    os.environ["IS_LOCAL"] = ""
    os.environ["FONTPATHDIR"] = "/tmp/"
    os.environ["TMP_DIR"] = "/tmp/"
    os.environ["BROKER_URL"] = os.environ["REDIS_URL"]
    os.environ["DOWNLOAD_LIST"] = glob("/tmp/*.mp4")
