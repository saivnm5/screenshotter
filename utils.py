# utils.py

import cv2
import os

def get_video_duration_and_frames(video_path):
    """Get the duration and total frames of a video."""
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return None, None

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    video_capture.release()
    return duration, total_frames


def extract_frames(video_path, output_dir, num_screenshots, total_frames, frame_interval, subfolder_name):
    """Extract frames from a video and save them as images."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return 0

    frame_count = 0
    saved_frame_count = 0

    print(f"Processing video: {video_path}")
    print(f"Extracting {num_screenshots} screenshots...")

    while True:
        success, frame = video_capture.read()

        if not success:
            break

        if frame_count % frame_interval == 0 and saved_frame_count < num_screenshots:
            frame_filename = os.path.join(
                output_dir, 
                f"{os.path.splitext(os.path.basename(video_path))[0]} | frame-{saved_frame_count:04d}.jpg"
            )
            # Save the frame with the highest quality
            cv2.imwrite(frame_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            saved_frame_count += 1

        frame_count += 1

    video_capture.release()
    print(f"Saved {saved_frame_count} frames from {video_path} to {output_dir}")
    return saved_frame_count