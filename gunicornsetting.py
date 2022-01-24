import os

if os.uname().nodename == "MacBook-Air.local":
    print("local run")
    bind = "localhost:5000"
