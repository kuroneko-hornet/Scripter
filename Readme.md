# How to use
1. create directory and make movie file, json file
2. edit json file (see following "json spec")
3. set the path to `create_video.py`
4. run

```python:
python create_video.py
```

# json spec
Please set params sorted by "start".  
(but python reads json file as dictionary type so...if needed, fix in the future)

```
{
    <any>: {
        "text": String: ex. "Hello, World!!"
        "fontsize": Int: ex. 36
        "start": Float: ex. 10
            time at the telop starts. specify in second
        "end": Float: ex. 11.5
            time at the telop ends. specify in second
        (option)"xy_mode": String: ex. "center"
            text position
            the default is the bottom of center
        (option)"color": String: "blue"
            text border color
            the default is black
    },
    ...
}
```