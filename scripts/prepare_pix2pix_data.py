import os
import cv2
from utils.video_utils import video_to_frame
from utils.file_utils import create_folder_if_not_exists

def combine_frames(rgb_frame_path, ir_frame_path, output_path):
    rgb_image = cv2.imread(rgb_frame_path)
    ir_image = cv2.imread(ir_frame_path)

    if rgb_image is None or ir_image is None:
        raise ValueError(f"Could not load images {rgb_frame_path} or {ir_frame_path}")

    combined_image = cv2.hconcat([rgb_image, ir_image])
    cv2.imwrite(output_path, combined_image)

def prepare_pix2pix_data(rgb_video_path, ir_video_path, output_dir, log_file):
    rgb_output_dir = os.path.join(output_dir, 'rgb_frames')
    ir_output_dir = os.path.join(output_dir, 'ir_frames')
    
    create_folder_if_not_exists(rgb_output_dir)
    create_folder_if_not_exists(ir_output_dir)
    
    vidcap_rgb = cv2.VideoCapture(rgb_video_path)
    vidcap_ir = cv2.VideoCapture(ir_video_path)
    
    duration_rgb = int(vidcap_rgb.get(cv2.CAP_PROP_FRAME_COUNT) / vidcap_rgb.get(cv2.CAP_PROP_FPS))
    duration_ir = int(vidcap_ir.get(cv2.CAP_PROP_FRAME_COUNT) / vidcap_ir.get(cv2.CAP_PROP_FPS))
    
    min_duration = min(duration_rgb, duration_ir)
    
    vidcap_rgb.release()
    vidcap_ir.release()
    
    with open(log_file, 'a') as log:
        log.write(f"\nRGB Video Duration: {duration_rgb} seconds, IR Video Duration: {duration_ir} seconds, Using Minimum Duration: {min_duration} seconds\n")
    
    video_to_frame(rgb_video_path, rgb_output_dir, 'A', min_duration, frame_rate=1, log_file=log_file)
    video_to_frame(ir_video_path, ir_output_dir, 'B', min_duration, frame_rate=1, log_file=log_file)
    
    pix2pix_output_dir = os.path.join(output_dir, 'pix2pix_combined_frames')
    create_folder_if_not_exists(pix2pix_output_dir)
    
    rgb_frames = sorted([os.path.join(rgb_output_dir, f) for f in os.listdir(rgb_output_dir) if f.endswith('.jpg')])
    ir_frames = sorted([os.path.join(ir_output_dir, f) for f in os.listdir(ir_output_dir) if f.endswith('.jpg')])
    
    with open(log_file, 'a') as log:
        log.write(f"Total RGB Frames: {len(rgb_frames)}, Total IR Frames: {len(ir_frames)}\n")
    
    if len(rgb_frames) != len(ir_frames):
        min_length = min(len(rgb_frames), len(ir_frames))
        rgb_frames = rgb_frames[:min_length]
        ir_frames = ir_frames[:min_length]
    
    for i, (rgb_frame, ir_frame) in enumerate(zip(rgb_frames, ir_frames)):
        frame_id = os.path.basename(rgb_frame).split('_')[0]
        combined_frame_path = os.path.join(pix2pix_output_dir, f"{frame_id}.jpg")
        combine_frames(rgb_frame, ir_frame, combined_frame_path)
        with open(log_file, 'a') as log:
            log.write(f"{i + 1}. Combined frame {rgb_frame} and {ir_frame} into {combined_frame_path}\n")

if __name__ == "__main__":
    rgb_video_path = "data/video/rgb/video_rgb.mp4"
    ir_video_path = "data/video/ir/video_ir.mp4"
    output_dir = "data/pix2pix"
    log_file = "data/pix2pix/extraction_log.txt"
    
    prepare_pix2pix_data(rgb_video_path, ir_video_path, output_dir, log_file)
