import os
import subprocess

def get_video_duration_and_frames(video_path):
    """Get the duration and total frames of a video using ffmpeg."""
    try:
        # Run ffmpeg to get video duration and frame count
        result = subprocess.run(
            [
                "ffprobe", 
                "-v", "error", 
                "-select_streams", "v:0", 
                "-show_entries", "stream=duration,nb_frames", 
                "-of", "default=noprint_wrappers=1:nokey=1", 
                video_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output = result.stdout.splitlines()
        if len(output) >= 2:
            duration = float(output[0])
            total_frames = int(output[1])
            return duration, total_frames
        else:
            print(f"Error: Could not retrieve duration and frame count for {video_path}")
            return None, None

    except Exception as e:
        print(f"Error while processing {video_path}: {e}")
        return None, None

def extract_frames(video_path, output_dir, num_screenshots, total_frames, max_screenshots, subfolder_name):
    """Extract frames from a video using ffmpeg and save them as images."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_filename = os.path.splitext(os.path.basename(video_path))[0]
    output_pattern = os.path.join(output_dir, f"{video_filename}_frame-%04d.jpg")

    # Calculate the actual number of screenshots we can take
    screenshots_to_take = min(num_screenshots, max_screenshots)

    if screenshots_to_take == 0:
        print(f"No screenshots to take for {video_filename}")
        return 0

    # Calculate the frame interval to achieve the desired number of screenshots
    frame_interval = max(1, total_frames // screenshots_to_take)

    # Use ffmpeg to extract frames at the calculated interval
    try:
        command = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"select=not(mod(n\\,{frame_interval}))",
            "-vsync", "vfr",
            "-q:v", "2",  # Highest quality JPEG
            output_pattern
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Extracted up to {screenshots_to_take} frames for {video_filename}")

        # Count how many frames were saved
        saved_frame_count = len([name for name in os.listdir(output_dir) if name.startswith(video_filename)])
        return min(saved_frame_count, screenshots_to_take)

    except Exception as e:
        print(f"Error while extracting frames from {video_path}: {e}")
        return 0
