#!/usr/bin/env python3

import argparse

from playlist_handler import PlaylistsHandler

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Your proper track exporter :)')
    parser.add_argument('--input-file', help='path to file with links',
            required=True)

    args = parser.parse_args()

    handler = PlaylistsHandler(args.input_file)
    handler.export_to_file()
