# main.py

from video_processor import VideoProcessor

def get_user_input():
    """Prompt the user for input folder, output folder, and strategy-related inputs."""
    input_folder = input("Enter the path to the input folder (containing videos or subfolders with videos): ").strip()
    output_folder = input("Enter the path to the output folder: ").strip()

    # Prompt user to choose the strategy
    strategy = input("Choose screenshot strategy ('max_screenshots' or 'time_based'): ").strip().lower()

    if strategy == 'max_screenshots':
        max_screenshots_per_folder = int(input("Enter the maximum number of screenshots per folder: ").strip())
        return input_folder, output_folder, strategy, max_screenshots_per_folder, None
    elif strategy == 'time_based':
        interval_duration = float(input("Enter the time interval (in seconds) for screenshots: ").strip())
        return input_folder, output_folder, strategy, None, interval_duration
    else:
        raise ValueError("Invalid strategy specified. Choose 'max_screenshots' or 'time_based'.")

def main():
    # Get user input
    input_folder, output_folder, strategy, max_screenshots_per_folder, interval_duration = get_user_input()

    # Create VideoProcessor with user inputs
    video_processor = VideoProcessor(
        input_folder, 
        output_folder, 
        strategy, 
        max_screenshots_per_folder=max_screenshots_per_folder, 
        interval_duration=interval_duration
    )
    
    # Start processing videos
    video_processor.process_videos()

if __name__ == '__main__':
    main()
