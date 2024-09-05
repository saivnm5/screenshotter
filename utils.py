# utils.py

import os
import subprocess
import re

def get_video_duration_and_frames(video_path):
    """Get the duration and total frames of a video using FFmpeg."""
    command = [
        'ffmpeg', 
        '-i', video_path,
        '-hide_banner'
    ]
    
    try:
        result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        stderr_output = result.stderr

        # Extract duration
        duration_match = re.search(r"Duration: (\d+:\d+:\d+\.\d+)", stderr_output)
        if duration_match:
            duration_str = duration_match.group(1)
            time_parts = duration_str.split(':')
            
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds_and_ms = float(time_parts[2])
            
            # Calculate total duration in seconds
            duration = hours * 3600 + minutes * 60 + seconds_and_ms
        else:
            print(f"Error: Could not find the duration of {video_path}")
            return None, None
        
        # Extract fps
        fps_match = re.search(r"(\d+(\.\d+)?) fps", stderr_output)
        if fps_match:
            fps = float(fps_match.group(1))
        else:
            print(f"Error: Could not find fps for {video_path}")
            return None, None
        
        # Calculate total frames
        total_frames = int(duration * fps)

        return duration, total_frames

    except Exception as e:
        print(f"Error while processing {video_path}: {str(e)}")
        return None, None


def extract_frames(video_path, output_dir, num_screenshots, total_frames, frame_interval, subfolder_name):
    """Extract frames from a video using FFmpeg and save them as images."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    saved_frame_count = 0
    print(f"Processing video: {video_path}")
    print(f"Extracting {num_screenshots} screenshots...")

    # Calculate the time interval for screenshots based on the total frames and desired number
    duration, _ = get_video_duration_and_frames(video_path)
    if duration is None:
        return 0

    for i in range(num_screenshots):
        # Calculate the timestamp for the current frame based on the interval
        timestamp = i * (duration / num_screenshots)

        # Create a unique filename for each frame to avoid overwriting
        frame_filename = os.path.join(
            output_dir, 
            f"{os.path.splitext(os.path.basename(video_path))[0]}_frame_{i:04d}.jpg"
        )

        # Use FFmpeg to extract a frame at the calculated timestamp
        command = [
            'ffmpeg', '-ss', str(timestamp),
            '-i', video_path,
            '-frames:v', '1',  # Extract only 1 frame
            '-q:v', '2',  # High-quality image (lower q means higher quality in FFmpeg)
            frame_filename,
            '-hide_banner', '-loglevel', 'error'
        ]

        try:
            subprocess.run(command, check=True)
            saved_frame_count += 1
        except subprocess.CalledProcessError as e:
            print(f"Error while extracting frame at {timestamp}s: {str(e)}")
            break

    print(f"Saved {saved_frame_count} frames from {video_path} to {output_dir}")
    return saved_frame_count
