# AAX to MP3 in Python

A simple script that wraps over other utils online to convert your own audible library to a more portable / free format.

Requires [ffmpeg](https://ffmpeg.zeranoe.com/builds/) and [inAudible-NG tables](https://github.com/inAudible-NG/tables/).
See [this awesome tutorial](https://wphelp365.com/blog/ultimate-guide-downloading-converting-aax-mp3/) on how to get the
two working. You really only need steps 1-4 to get the Activation Bytes.

Then it's just a matter of calling

```
python convert.py -i "The Tower of the Swallow.aax" -o "The Tower of the Swallow %(chapter)s %(bitrate)s.mp3" -a xxxxxx
```

and have your owned aax converted into mp3s, split by chapters.

Use `-t "The Tower %s(chapter)"` to specify mp3 title.

## Why?

Even though the above mentioned tutorial works great, my mp3 player 
[MortPlayer for Android](https://play.google.com/store/apps/details?id=de.stohelit.audiobookplayer&hl=en) (I really 
recommend) had some issues with mp3s longer than a couple of hours. So I wanted to have the book split by chapters.