# main.py

from video_processor import VideoProcessor

def get_user_input():
    """Prompt the user for input folder, output folder, and max screenshots per folder."""
    input_folder = input("Enter the path to the input folder (containing videos or subfolders with videos): ").strip()
    output_folder = input("Enter the path to the output folder: ").strip()
    max_screenshots_per_folder = int(input("Enter the maximum number of screenshots per folder: ").strip())
    
    return input_folder, output_folder, max_screenshots_per_folder

def main():
    # Get user input
    input_folder, output_folder, max_screenshots_per_folder = get_user_input()

    # Create VideoProcessor with user inputs
    video_processor = VideoProcessor(input_folder, output_folder, max_screenshots_per_folder)
    
    # Start processing videos
    video_processor.process_videos()

if __name__ == '__main__':
    main()
