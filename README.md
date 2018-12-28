# AAX to MP3 in Python

A simple script that wraps over other utils online to convert your own audible library to a more portable / free format.

Requires Python 3.6 and up, [ffmpeg](https://ffmpeg.zeranoe.com/builds/) and [inAudible-NG tables](https://github.com/inAudible-NG/tables/).
See [this awesome tutorial](https://wphelp365.com/blog/ultimate-guide-downloading-converting-aax-mp3/) on how to get the
two working. You really only need steps 1-4 to get the Activation Bytes.

Then it's just a matter of calling

```
python convert.py -i "The Tower of the Swallow.aax" -a xxxxxx
```

and have your owned aax converted into mp3s, split by chapters, automatically with '_{Chapter_number}' appended to the end.

## Why?

Splitting the very long audio book files by chapters seemed like a much more sensible way of handling extended audio.