import argparse
import json
import os
import re
import subprocess

"""
See https://wphelp365.com/blog/ultimate-guide-downloading-converting-aax-mp3/ on how to use.

Step 3 + 4 will get activation bytes. Step 5 is this script.
"""


def get_chapters(ffmpeg, input):
    cmd = ['%s/ffprobe' % ffmpeg, '-show_chapters', '-loglevel', 'error', '-print_format', 'json', input]
    output = subprocess.check_output(cmd, universal_newlines=True)
    chapters = json.loads(output)
    return chapters


def parse_chapters(ffmpeg, chapters, input, output, activation_bytes, bitrate, album):
    i = 0
    for chapter in chapters['chapters']:
        i += 1
        title = chapter['tags']['title']

        cmd = ['%s/ffmpeg' % ffmpeg, '-y', '-activation_bytes', activation_bytes, '-i', input, '-ab', bitrate,
               '-ss', chapter['start_time'], '-to', chapter['end_time'], '-metadata', 'title=%s' % title]

        if album is not None:
            cmd.extend(['-metadata', 'album=%s' % album])

        cmd.extend(['-vn', output % i])
        print(cmd)
        subprocess.check_output(cmd, universal_newlines=True)
        break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-o', '--output',
                        help='Output file pattern (with one %d placeholder)', required=True)
    parser.add_argument('-a', '--activation-bytes', help='Activation bytes', required=True)
    parser.add_argument('-b', '--bitrate', help='Bitrate', default='64k')
    parser.add_argument('--ffmpeg', help='Path do directory containing ffmpeg/ffprobe', default='ffmpeg/bin')
    parser.add_argument('--album', help='ID3v2 tag for Album, if not specified, uses from aax')
    namespace = parser.parse_args()
    print(namespace)

    input = namespace.input
    output = namespace.output
    activation_bytes = namespace.activation_bytes
    bitrate = namespace.bitrate
    ffmpeg = namespace.ffmpeg
    album = namespace.album
    chapters = get_chapters(ffmpeg, input)
    # title = namespace.title
    print(chapters)
    parse_chapters(ffmpeg, chapters, input, output, activation_bytes, bitrate, album)
