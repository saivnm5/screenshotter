# video_processor.py

import os
from utils import get_video_duration_and_frames, extract_frames

class VideoProcessor:
    def __init__(self, input_folder, output_folder, max_screenshots_per_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.max_screenshots_per_folder = max_screenshots_per_folder

    def process_videos(self):
        """Process all videos in the input folder, either directly or through subfolders."""
        if self._contains_subfolders():
            subfolders = self._get_subfolders()
            for subfolder in subfolders:
                self._process_subfolder(subfolder)
        else:
            self._process_folder(self.input_folder)

    def _contains_subfolders(self):
        """Check if the input folder contains subfolders."""
        for f in os.listdir(self.input_folder):
            if os.path.isdir(os.path.join(self.input_folder, f)):
                return True
        return False

    def _get_subfolders(self):
        """Return a list of subfolders in the input folder."""
        return [f for f in os.listdir(self.input_folder) if os.path.isdir(os.path.join(self.input_folder, f))]

    def _process_subfolder(self, subfolder):
        """Process each subfolder by extracting frames from video files."""
        subfolder_path = os.path.join(self.input_folder, subfolder)
        self._process_folder(subfolder_path, subfolder)

    def _process_folder(self, folder_path, subfolder_name=None):
        """Process a folder (or subfolder) containing video files."""
        videos = self._get_video_files(folder_path)

        if not videos:
            print(f"No video files found in {folder_path}")
            return

        total_duration = self._calculate_total_duration(videos)
        screenshots_taken = 0

        for video_file, duration, total_frames in videos:
            if screenshots_taken >= self.max_screenshots_per_folder:
                break

            num_screenshots = int((duration / total_duration) * self.max_screenshots_per_folder)
            if num_screenshots == 0:
                continue

            frame_interval = int(total_frames / num_screenshots)
            output_dir = os.path.join(self.output_folder, subfolder_name if subfolder_name else os.path.basename(self.input_folder))
            screenshots_taken += extract_frames(
                video_file, output_dir, num_screenshots, total_frames, frame_interval, subfolder_name if subfolder_name else os.path.basename(self.input_folder)
            )

        print(f"Total screenshots taken from folder '{folder_path}': {screenshots_taken}")

    def _get_video_files(self, folder_path):
        """Return a list of video files along with their durations and frame counts."""
        video_files = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.mp4', '.m4v', '.mov', '.avi', '.mkv')):
                video_path = os.path.join(folder_path, filename)
                duration, total_frames = get_video_duration_and_frames(video_path)
                if duration and total_frames:
                    video_files.append((video_path, duration, total_frames))
        return video_files

    def _calculate_total_duration(self, videos):
        """Calculate the total duration of all videos in the folder."""
        return sum(duration for _, duration, _ in videos)
