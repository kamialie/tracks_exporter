import requests
import json
import csv

from datetime import datetime

def parse_int(string):
    end = 0

    for letter in string:
        if letter in "0123456789":
            end += 1
        else:
            break

    # TODO raise expection if no digits found
    # if end == 0:
    #     raise error
    return string[:end]

class PlaylistsHandler:
    def __init__(self, input_file):
        input_data = self._parse_input(input_file)
        self.playlists = self._fetch_playlists(input_data)
        self.tracks = self._prepare_track_dict(self.playlists)
        #print(self.tracks)

    def _parse_input(self, input_file):
        input_data = {}
        # TODO add exception handler
        with open(input_file) as fh:
            json_data = json.load(fh)

            for entry in json_data["playlists"]:
                fields = entry.split("/")
                owner = fields[4]
                playlist_id = parse_int(fields[6])

                if owner in input_data:
                    input_data[owner].append(playlist_id)
                else:
                    input_data[owner] = [playlist_id]

        return input_data

    def _fetch_playlists(self, input_data):
        playlists = []

        for owner, playlist_ids in input_data.items():
            for playlist_id in playlist_ids:
                playlist_data = self._get_playlist_data(owner, playlist_id)
                if playlist_data is not None:
                    playlists.append(playlist_data)

        return playlists

    def _get_playlist_data(self, owner, playlist_id):
        endpoint = f"https://music.yandex.ru/handlers/playlist.jsx?owner={owner}&kinds={playlist_id}"

        response = requests.get(endpoint)
        if (response.ok):
            return json.loads(response.content)
        else:
            print(f"Error:{response.status_code} {response.url} {response.content}")

    def _prepare_track_dict(self, playlists):
        track_list = []

        for playlist in self.playlists:
            tracks = playlist["playlist"]["tracks"]
            owner = playlist["playlist"]["owner"]["login"]

            for track in tracks:
                artists = []

                for artist in track["artists"]:
                    artists.append(artist["name"])

                track_list.append({
                    "title": track["title"],
                    "artist(s)": "|".join(artists),
                    "owner": owner
                })

        return track_list


    def export_to_file(self, name_prefix="tracks"):
        today = datetime.today().strftime("%Y-%m-%d")

        with open(f"tracks-{today}.csv", "w") as fh:
            # TODO explore other way to pass header fields
            dw = csv.DictWriter(fh, self.tracks[0].keys())
            dw.writeheader()
            dw.writerows(self.tracks)

handler = PlaylistsHandler("input.json")
handler.export_to_file()
