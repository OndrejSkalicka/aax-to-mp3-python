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


def parse_chapters(ffmpeg, chapters, input, output, activation_bytes, bitrate, title):
    for chapter in chapters['chapters']:
        title = chapter['tags']['title']
        match = re.match('Chapter (\d+)', title)
        if match:
            title = 'Chapter %02d' % int(match.group(1))

        args = {'chapter': title, 'bitrate': bitrate}
        cmd = ['%s/ffmpeg' % ffmpeg, '-y', '-activation_bytes', activation_bytes, '-i', input, '-ab', bitrate,
               '-ss', chapter['start_time'], '-to', chapter['end_time']]

        if title is not None:
            cmd.extend(['-metadata', 'title=%s' % (title % args)])

        cmd.extend(['-vn', output % args])
        print(cmd)
        subprocess.check_output(cmd, universal_newlines=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-o', '--output',
                        help='Output file pattern (with two "%(chapter)s" and %(bitrate)" placeholders)', required=True)
    parser.add_argument('-t', '--title',
                        help='Title of mp3 pattern (with two "%(chapter)s" and %(bitrate)" placeholders)')
    parser.add_argument('-a', '--activation-bytes', help='Activation bytes', required=True)
    parser.add_argument('-b', '--bitrate', help='Bitrate', default='64k')
    parser.add_argument('--ffmpeg', help='Path do directory containing ffmpeg/ffprobe', default='ffmpeg/bin')
    namespace = parser.parse_args()
    print(namespace)

    input = namespace.input
    output = namespace.output
    activation_bytes = namespace.activation_bytes
    bitrate = namespace.bitrate
    ffmpeg = namespace.ffmpeg
    chapters = get_chapters(ffmpeg, input)
    title = namespace.title
    print(chapters)
    parse_chapters(ffmpeg, chapters, input, output, activation_bytes, bitrate, title)
