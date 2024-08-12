import cv2
import os

def extract_frames(video_path, output_dir, num_screenshots, total_frames, frame_interval, subfolder_name):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the video
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
            frame_filename = os.path.join(output_dir, f"{subfolder_name}_{os.path.splitext(os.path.basename(video_path))[0]}_frame_{saved_frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            saved_frame_count += 1

        frame_count += 1

    video_capture.release()
    print(f"Saved {saved_frame_count} frames from {video_path} to {output_dir}")
    return saved_frame_count

def process_folder(input_folder, output_folder, max_screenshots_per_folder):
    # Create a single output directory named after the input folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for subfolder in os.listdir(input_folder):
        subfolder_path = os.path.join(input_folder, subfolder)
        if os.path.isdir(subfolder_path):
            total_duration = 0
            video_durations = []

            # Calculate the total duration of all videos in the subfolder
            for filename in os.listdir(subfolder_path):
                if filename.lower().endswith(('.mp4', '.m4v', '.mov', '.avi', '.mkv')):
                    video_path = os.path.join(subfolder_path, filename)
                    video_capture = cv2.VideoCapture(video_path)
                    if video_capture.isOpened():
                        fps = video_capture.get(cv2.CAP_PROP_FPS)
                        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
                        duration = total_frames / fps
                        video_durations.append((filename, duration, total_frames))
                        total_duration += duration
                    video_capture.release()

            print(f"Total duration of videos in folder '{subfolder}': {total_duration} seconds")

            screenshots_taken = 0

            for filename, duration, total_frames in video_durations:
                if screenshots_taken >= max_screenshots_per_folder:
                    break
                num_screenshots = int((duration / total_duration) * max_screenshots_per_folder)
                if num_screenshots == 0:
                    continue
                video_path = os.path.join(subfolder_path, filename)
                fps = total_frames / duration
                frame_interval = int(total_frames / num_screenshots)
                subfolder_output_dir = os.path.join(output_folder, subfolder)
                screenshots_taken += extract_frames(video_path, subfolder_output_dir, num_screenshots, total_frames, frame_interval, subfolder)

            print(f"Total screenshots taken from folder '{subfolder}': {screenshots_taken}")

# Example usage
input_folder = '/Volumes/HDD1/Stuff/hair/rapunzel-universe/rapunzel-universe-hair2'
output_folder = 'output'
max_screenshots_per_folder = 12  # Maximum number of screenshots per subfolder
process_folder(input_folder, output_folder, max_screenshots_per_folder)
