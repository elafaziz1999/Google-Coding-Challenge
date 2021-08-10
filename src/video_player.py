"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.current_vid_playing = []
        self.pausing_of_video = False
        self.playlist = {}
        self.flagged_video = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        videos = self._video_library.get_all_videos()                                                                       # gets all the videos from the video_library and stores it into the videos variable
        sorted_vid_list = []
        for x in videos:                                                                                                    # for every object (x) in video # the replace only works for strings sort only works on lists and dictionaries
            if x.video_id in self.flagged_video.keys():
                sorted_vid_list.append(x.title + " ("+x.video_id+") " + str(list(x.tags)).replace(",", "").replace("'", "") + " - FLAGGED (reason: " + self.flagged_video[x.video_id] + ")")
            else:
                sorted_vid_list.append(x.title + " ("+x.video_id+") " + str(list(x.tags)).replace(",", "").replace("'", ""))
        sorted_vid_list.sort()                                                                                              # to sort the video list
        print("Here's a list of all available videos:", *sorted_vid_list, sep= "\n\t")                                                                                # star is used when we want it to print each object inside the list

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        videos = self._video_library.get_video(video_id)
        if videos == None:
            print("Cannot play video: Video does not exist")
        elif video_id in self.flagged_video.keys():
            print("Cannot play video: Video is currently flagged (reason:", self.flagged_video[video_id] + ")")
        elif len(self.current_vid_playing) == 0:
            self.current_vid_playing = [video_id]
            print("Playing video:", videos.title)
            self.pausing_of_video = False
        else:
            self.stop_video()
            self.current_vid_playing = [video_id]
            print("Playing video:", videos.title)
            self.pausing_of_video = False

    def stop_video(self):
        """Stops the current video."""
        if len(self.current_vid_playing) == 0:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video:", self._video_library.get_video(self.current_vid_playing[0]).title)
            self.current_vid_playing = []

    def play_random_video(self):
        """Plays a random video from the video library."""
        random_videos = self._video_library.get_all_videos()
        rand_vid_list = []
        for x in random_videos:
            if x.video_id in self.flagged_video.keys():
                continue
            else:
                rand_vid_list.append(x.video_id)
        if len(rand_vid_list) == 0:
            print("No videos available")
        else:
            random_choice = random.choice(rand_vid_list)
            self.play_video(random_choice)

    def pause_video(self):
        """Pauses the current video."""
        if self.current_vid_playing == []:
            print("Cannot pause video: No video is currently playing")
        elif self.pausing_of_video == False:
            print("Pausing video:", self._video_library.get_video(self.current_vid_playing[0]).title)
            self.pausing_of_video = True
        else:
            print("Video already paused:", self._video_library.get_video(self.current_vid_playing[0]).title)

    def continue_video(self):
        """Resumes playing the current video."""
        if self.pausing_of_video == True:
            print("Continuing video:", self._video_library.get_video(self.current_vid_playing[0]).title)
            self.pausing_of_video = False
        elif self.current_vid_playing == []:
            print("Cannot continue video: No video is currently playing")
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self.current_vid_playing == []:
            print("No video is currently playing")
        elif self.pausing_of_video == True:
            video_object = self._video_library.get_video(self.current_vid_playing[0])
            print("Currently playing:", video_object.title + " ("+video_object.video_id+") " + str(list(video_object.tags)).replace(",", "").replace("'", ""), "- PAUSED")
        else:
            video_object = self._video_library.get_video(self.current_vid_playing[0])
            print("Currently playing:", video_object.title + " ("+video_object.video_id+") " + str(list(video_object.tags)).replace(",", "").replace("'", ""))

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_lowcase = playlist_name.lower()
        if playlist_name_lowcase in self.playlist.keys():
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            print("Successfully created new playlist:", playlist_name)
            self.playlist[playlist_name_lowcase] = Playlist(playlist_name, [])

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist_name_lowcase = playlist_name.lower()
        if playlist_name_lowcase not in self.playlist.keys():
            print("Cannot add video to", playlist_name +": Playlist does not exist")
        elif self._video_library.get_video(video_id) == None:
            print("Cannot add video to", playlist_name +": Video does not exist")
        elif video_id in self.flagged_video.keys():
            print("Cannot add video to", playlist_name + ": Video is currently flagged (reason:", self.flagged_video[video_id] + ")")
        elif video_id in self.playlist[playlist_name_lowcase].videos_in_playlist:
            print("Cannot add video to", playlist_name +": Video already added")
        else:
            videos_already_stored = self.playlist[playlist_name_lowcase].videos_in_playlist
            videos_already_stored = videos_already_stored + [video_id]
            self.playlist[playlist_name_lowcase] = Playlist(playlist_name, videos_already_stored)
            print("Added video to", playlist_name +": "+ self._video_library.get_video(video_id).title)

    def show_all_playlists(self):
        """Display all playlists."""
        sorted_playlist = []
        if len(self.playlist) == 0:
            print("No playlists exist yet")
        else:
            all_playlist = self.playlist.values()
            for x in all_playlist:
                sorted_playlist.append(x.playlist_name)
            sorted_playlist.sort()
            print("Showing all playlists:", *sorted_playlist, sep= "\n\t")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_lowcase = playlist_name.lower()
        if playlist_name_lowcase not in self.playlist.keys():
            print("Cannot show playlist", playlist_name +": Playlist does not exist")
        elif len(self.playlist.get(playlist_name_lowcase).videos_in_playlist) == 0:
            print("Showing playlist:", playlist_name)
            print("\t No videos here yet")
        else:
            video_ids = self.playlist.get(playlist_name_lowcase).videos_in_playlist
            print("Showing playlist:", playlist_name)
            for x in video_ids:
                video_object = self._video_library.get_video(x)
                if video_object.video_id in self.flagged_video.keys():
                    print("\t"+ video_object.title + " (" + video_object.video_id + ") " + str(list(video_object.tags)).replace(",", "").replace("'", "") + " - FLAGGED (reason: " + self.flagged_video[video_object.video_id] + ")", sep= "\n\t")
                else:
                    print("\t"+ video_object.title + " (" + video_object.video_id + ") " + str(list(video_object.tags)).replace(",", "").replace("'", ""), sep= "\n\t")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist_name_lowcase = playlist_name.lower()
        if playlist_name_lowcase not in self.playlist.keys():
            print("Cannot remove video from", playlist_name + ": Playlist does not exist")
        elif self._video_library.get_video(video_id) == None:
            print("Cannot remove video from", playlist_name + ": Video does not exist")
        else:
            videos_already_stored = self.playlist[playlist_name_lowcase].videos_in_playlist
            if video_id in videos_already_stored:
                videos_already_stored.remove(video_id)
                self.playlist[playlist_name_lowcase] = Playlist(playlist_name, videos_already_stored)
                print("Removed video from", playlist_name + ": " + self._video_library.get_video(video_id).title)
            else:
                print("Cannot remove video from", playlist_name + ": Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_lowcase = playlist_name.lower()
        if playlist_name_lowcase not in self.playlist.keys():
            print("Cannot clear playlist", playlist_name + ": Playlist does not exist")
        else:
            self.playlist[playlist_name_lowcase] = Playlist(playlist_name, [])
            print("Successfully removed all videos from", playlist_name)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_name_lowcase = playlist_name.lower()
        if playlist_name_lowcase not in self.playlist.keys():
            print("Cannot delete playlist", playlist_name + ": Playlist does not exist")
        else:
            self.playlist.pop(playlist_name_lowcase)
            print("Deleted playlist:", playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        similar_videos = []
        search_lower = search_term.lower()
        all_videos = self._video_library.get_all_videos()
        for video in all_videos:
            if video.video_id in self.flagged_video.keys():
                continue
            elif video.title.lower().count(search_lower) > 0:
                similar_videos.append(video.video_id)
        if len(similar_videos) == 0:
            print("No search results for", search_term)
        else:
            print("Here are the results for", search_term + ":")
            similar_videos.sort()
            counter = 1
            for x in similar_videos:
                video_object = self._video_library.get_video(x)
                print("\t"+ str(counter) + ")", video_object.title + " (" + video_object.video_id + ") " + str(list(video_object.tags)).replace(",", "").replace("'", ""))
                counter += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            user_answer = input()
            if user_answer.isdigit():
                if 0 < int(user_answer) <= len(similar_videos):
                    self.play_video(similar_videos[int(user_answer)-1])

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        similar_videos = []
        video_tag_lower = video_tag.lower()
        all_videos = self._video_library.get_all_videos()
        for video in all_videos:
            vid_tags = str(video.tags)
            if video.video_id in self.flagged_video.keys():
                continue
            elif vid_tags.lower().count(video_tag_lower) > 0:
                similar_videos.append(video.video_id)
        if len(similar_videos) == 0:
            print("No search results for", video_tag)
        else:
            print("Here are the results for", video_tag + ":")
            similar_videos.sort()
            counter = 1
            for x in similar_videos:
                video_object = self._video_library.get_video(x)
                print("\t" + str(counter) + ")",
                      video_object.title + " (" + video_object.video_id + ") " + str(list(video_object.tags)).replace(
                          ",", "").replace("'", ""))
                counter += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            user_answer = input()
            if user_answer.isdigit():
                if 0 < int(user_answer) <= len(similar_videos):
                    self.play_video(similar_videos[int(user_answer) - 1])

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if self._video_library.get_video(video_id) == None:
            print("Cannot flag video: Video does not exist")
        elif video_id in self.flagged_video.keys():
            print("Cannot flag video: Video is already flagged")
        else:
            if video_id in self.current_vid_playing:
                self.stop_video()
            print("Successfully flagged video:", self._video_library.get_video(video_id).title, "(reason:", flag_reason + ")")
            self.flagged_video[video_id] = flag_reason                                                                   # what is in the square bracket is the key and what is after the equal is the value

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        if self._video_library.get_video(video_id) == None:
            print("Cannot remove flag from video: Video does not exist")
        elif video_id in self.flagged_video.keys():
            self.flagged_video.pop(video_id)
            print("Successfully removed flag from video:", self._video_library.get_video(video_id).title)
        else:
            print("Cannot remove flag from video: Video is not flagged")
