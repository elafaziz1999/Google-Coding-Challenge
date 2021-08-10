"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_name: str, videos_in_playlist: list):
        self._playlist_name = playlist_name
        self._videos_in_playlist = videos_in_playlist

    @property
    def playlist_name(self) -> str:
        return self._playlist_name

    @property
    def videos_in_playlist(self) -> list:
        return self._videos_in_playlist