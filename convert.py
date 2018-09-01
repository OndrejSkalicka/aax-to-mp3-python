import argparse
import json
import os
import re
import subprocess
from pathlib import Path

"""
See https://wphelp365.com/blog/ultimate-guide-downloading-converting-aax-mp3/ 
on how to use.
Step 3 + 4 will get activation bytes. Step 5 is this script.

Example:
python convert.py -i "The Tower of the Swallow.aax" -a xxxxxx
where -a is the activation code
"""


def get_chapters(ffmpeg, input):
    cmd = ['ffprobe', '-show_chapters', '-loglevel', 'error', '-print_format',
           'json', input]
    output = subprocess.check_output(cmd, universal_newlines=True)
    chapters = json.loads(output)
    return chapters


def parse_chapters(ffmpeg, chapters, input, output, activation_bytes, bitrate,
                   album):
    for i, chapter in enumerate(chapters['chapters']):
        title = chapter['tags']['title']

        cmd = ['ffmpeg', '-y',
               '-activation_bytes', activation_bytes,
               '-i', input,
               '-ss', chapter['start_time'],
               '-to', chapter['end_time'],
               '-metadata', 'title=%s' % title]

        if album is not None:
            cmd.extend(['-metadata', 'album=%s' % album])

        cmd.extend(['-c:a', 'mp3', '-vn', output % i + 1])
        print(cmd)

        subprocess.check_output(cmd, universal_newlines=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-a', '--activation-bytes', help='Activation bytes',
                        required=True)
    parser.add_argument('-b', '--bitrate', help='Bitrate', default='64k')
    parser.add_argument('--ffmpeg',
                        help='Path do directory containing ffmpeg/ffprobe',
                        default='ffmpeg/bin')
    parser.add_argument('--album',
                        help='ID3v2 tag for Album, if not specified, '
                             'uses from aax')
    namespace = parser.parse_args()
    print(namespace)

    # Collate args
    input = namespace.input
    out_arg = Path(input).stem
    output = out_arg + '_%02d.' + 'mp3'
    activation_bytes = namespace.activation_bytes
    bitrate = namespace.bitrate
    ffmpeg = namespace.ffmpeg
    album = namespace.album
    chapters = get_chapters(ffmpeg, input)
    # title = namespace.title
    print(chapters)

    parse_chapters(ffmpeg, chapters, input, output, activation_bytes, bitrate,
                   album)
