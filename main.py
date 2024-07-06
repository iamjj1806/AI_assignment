import cv2
import numpy as np
import datetime
from moviepy.editor import VideoFileClip

# Function to detect balls of a specific color in a frame


def detect_balls(frame, lower_color, upper_color):
    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area to remove small noise
    min_contour_area = 100
    valid_contours = [contour for contour in contours if cv2.contourArea(
        contour) > min_contour_area]

    # Get the center coordinates of each valid contour
    centers = []
    for contour in valid_contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers.append((cX, cY))

    return centers

# Function to determine the quadrant based on the frame dimensions and ball coordinates


def get_quadrant(frame_shape, ball_coordinates):
    height, width = frame_shape[:2]
    center_x, center_y = ball_coordinates

    if center_x < width / 2:
        if center_y < height / 2:
            return 1
        else:
            return 3
    else:
        if center_y < height / 2:
            return 2
        else:
            return 4


# Open the video file
video_path = 'AI Assignment video.mp4'
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define color ranges for each ball color (you may need to adjust these values)
color_ranges = {
    'red': ((0, 100, 100), (10, 255, 255)),
    'green': ((40, 40, 40), (80, 255, 255)),
    'blue': ((100, 100, 100), (140, 255, 255)),
    'white': ((0, 0, 200), (255, 50, 255))  # Adjust the range for white color
}

# Create VideoWriter object to save the processed video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video_path = 'processed_video.avi'
out = cv2.VideoWriter(output_video_path, fourcc, fps,
                      (frame_width, frame_height))

# Create or overwrite the text file for event records
text_file_path = 'event_records.txt'

# Loop through each frame
for frame_count in range(total_frames):
    ret, frame = cap.read()
    if not ret:
        break

    # Process each color
    for color, (lower, upper) in color_ranges.items():
        ball_centers = detect_balls(frame, np.array(lower), np.array(upper))

        # Process each ball
        for center in ball_centers:
            quadrant = get_quadrant(frame.shape, center)

            # Record the event
            timestamp = datetime.timedelta(seconds=frame_count / fps)
            event_type = 'Entry'  # or 'Exit' based on your logic

            # Draw a circle around the detected ball
            cv2.circle(frame, center, 10, (0, 255, 0), -1)

            # Overlay text on the frame
            text = f"Quadrant {quadrant}, {color} Ball, {event_type}, Time: {timestamp}"
            cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 255), 2, cv2.LINE_AA)

            # Save the event data to the text file
            with open(text_file_path, 'a') as f:
                f.write(
                    f"Timestamp: {timestamp}, Quadrant Number: {quadrant}, Ball Colour: {color}, Type: {event_type}\n")

    # Write the frame to the output video
    out.write(frame)

# Release resources
cap.release()
out.release()

print(f"Processed video saved at: {output_video_path}")
print(f"Event records saved at: {text_file_path}")

# """
# #Only if you need to convert your output file from .avi to .mp4
# def convert_avi_to_mp4(input_file, output_file):
#     # Load the AVI file
#     clip = VideoFileClip(input_file)

#     # Write the video to an MP4 file
#     clip.write_videofile(output_file, codec='libx264', audio_codec='aac')


# if __name__ == "__main__":
#     input_file = "processed_video.avi"  # Replace with your AVI file name
#     output_file = "processed_video.mp4"  # Replace with the desired MP4 file name

#     convert_avi_to_mp4(input_file, output_file)