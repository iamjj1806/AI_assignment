import cv2
import numpy as np
import datetime

# Function to detect balls of a specific color in a frame
def detect_balls(frame, lower_color, upper_color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 100
    valid_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]
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
            return 3
        else:
            return 2
    else:
        if center_y < height / 2:
            return 4
        else:
            return 1

# Open the video file
video_path = 'AI Assignment video.mp4'
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define color ranges for each ball color
color_ranges = {
    'red': ((0, 100, 100), (10, 255, 255)),
    'green': ((40, 40, 40), (80, 255, 255)),
    'blue': ((100, 100, 100), (140, 255, 255)),
    'white': ((0, 0, 200), (255, 50, 255))
}

# Create VideoWriter object to save the processed video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video_path = 'processed_video_2.avi'
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Create or overwrite the text file for event records
text_file_path = 'event_records_2.txt'

# Initialize previous quadrant tracking
previous_quadrants = {color: None for color in color_ranges}

# Loop through each frame
for frame_count in range(total_frames):
    ret, frame = cap.read()
    if not ret:
        break

    # Process each color
    for color, (lower, upper) in color_ranges.items():
        ball_centers = detect_balls(frame, np.array(lower), np.array(upper))
        for center in ball_centers:
            quadrant = get_quadrant(frame.shape, center)
            previous_quadrant = previous_quadrants[color]

            if previous_quadrant is None or previous_quadrant != quadrant:
                event_type = 'Exit' if previous_quadrant is not None and previous_quadrant != quadrant else 'Entry'
                previous_quadrants[color] = quadrant

                # Record the event
                timestamp = datetime.timedelta(seconds=frame_count / fps)

                # Draw a circle around the detected ball
                cv2.circle(frame, center, 10, (0, 255, 0), -1)

                # Overlay text on the frame
                text = f"Quadrant {quadrant}, {color} Ball, {event_type}, Time: {timestamp}"
                cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Save the event data to the text file
                with open(text_file_path, 'a') as f:
                    f.write(f"Timestamp: {timestamp}, Quadrant Number: {quadrant}, Ball Colour: {color}, Type: {event_type}\n")

    # Write the frame to the output video
    out.write(frame)

# Release resources
cap.release()
out.release()

print(f"Processed video saved at: {output_video_path}")
print(f"Event records saved at: {text_file_path}")
