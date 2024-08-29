import cv2
import os

from utils.file_utils import create_folder_if_not_exists

def video_to_frame(video_path, output_directory, prefix, max_duration, frame_rate=1, log_file=None):
    create_folder_if_not_exists(output_directory)
    
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * frame_rate)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    with open(log_file, 'a') as log:
        log.write(f"\nVideo: {video_path}, FPS: {fps}, Duration: {duration} seconds, Total Frames: {total_frames}, Frame Interval: {frame_interval}\n")
    
    count = 0
    extracted_frame_count = 0
    success = True
    while success and (extracted_frame_count < max_duration):
        success, image = vidcap.read()
        if not success:
            break
        if count % frame_interval == 0:
            timestamp = int(vidcap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
            frame_filename = os.path.join(output_directory, f"{timestamp:04d}_{prefix}.jpg")
            cv2.imwrite(frame_filename, image)
            with open(log_file, 'a') as log:
                log.write(f"{extracted_frame_count + 1}. Extracting frame at {timestamp} seconds, saved as {frame_filename}\n")
            extracted_frame_count += 1
        count += 1

    vidcap.release()
    with open(log_file, 'a') as log:
        log.write(f"Frames extracted and saved to {output_directory}, Total frames extracted: {extracted_frame_count}\n")