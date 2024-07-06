import cv2
import numpy as np
import time

time_yellow = []
time_orange = []
time_green = []
time_white = []
quad_yellow = []
quad_orange = []
quad_green = []
quad_white = []

start = time.time()
f = open("myfile.txt", "w")  # file
color = ["yellow", "orange", "green", "white"]

def quad(x, y):
    q = None
    if 1260 < x < 1740 and 540 < y < 1000:
        q = 1
    elif 790 < x < 1215 and 540 < y < 1010:
        q = 2
    elif 800 < x < 1222 and 30 < y < 500:
        q = 3
    elif 1260 < x < 1740 and 30 < y < 500:
        q = 4
    return q

cap = cv2.VideoCapture('AI Assignment video.mp4')

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter object to save the processed video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('Squares_and_Circles.avi', fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    cv2.namedWindow("Squares and Circles", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Squares and Circles", 1280, 720)

    if ret:
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (17, 17), 0)

        # Apply threshold to isolate squares
        _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)

        # Find contours of squares
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Draw rectangles around squares
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            if len(approx) == 4 and abs(area) > 2000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Detect circles
        circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.4, 90, param1=100,
                                   param2=35, minRadius=10, maxRadius=80)

        if circles is not None:
            circles = np.uint16(np.around(circles))

            for (x, y, rad) in circles[0, :]:
                cv2.circle(frame, (x, y), rad, (100, 255, 0), 3)
                b, g, r = frame[y, x]

                # yellow 
                if 57 < r < 213 and 52 < g < 189 and 15 < b < 63:
                    quad_yellow.append(quad(x, y))
                    end_yellow = time.time()
                    time_yellow_in = end_yellow - start
                    time_yellow.append(int(time_yellow_in))
                    cv2.putText(frame, color[0], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                    try:
                        yellow_in = ['\n', color[0], ' enter in ', str(time_yellow[0]), ' at quadrant ', str(quad_yellow[-1]), '\n']
                        yellow_out = ['\n', color[0], ' out at ', str(time_yellow[-1]), ' at quadrant ', str(quad_yellow[-1]), '\n']
                        if time_yellow[-1] - time_yellow[-2] > 3:
                            f.writelines(yellow_in)
                            f.writelines(yellow_out)
                            time_yellow.clear()
                    except:
                        pass

                # green  rgb(12,41,34)   rgb(54,77,69)
                if 12 < r < 55 and 41 < g < 77 and 34 < b < 69:
                    quad_green.append(quad(x, y))
                    end_green = time.time()
                    time_green_in = end_green - start
                    time_green.append(int(time_green_in))
                    cv2.putText(frame, color[2], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    try:
                        green_in = ['\n', color[2], " enter in ", str(time_green[0]), " at quadrant ", str(quad_green[-1]), '\n']
                        green_out = ['\n', color[2], " out at ", str(time_green[-1]), " at quadrant ", str(quad_green[-1]), '\n']
                        if time_green[-1] - time_green[-2] > 2:
                            f.writelines(green_in)
                            f.writelines(green_out)
                            time_green.clear()
                    except:
                        pass

                # orange
                if 176 < r < 255 and 61 < g < 167 and 29 < b < 131:
                    quad_orange.append(quad(x, y))
                    end_orange = time.time()
                    time_orange_in = end_orange - start
                    time_orange.append(int(time_orange_in))
                    cv2.putText(frame, color[1], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    try:
                        orange_in = ['\n', color[1], " enter in ", str(time_orange[0]), " at quadrant ", str(quad_orange[-1]), '\n']
                        orange_out = ['\n', color[1], " out at ", str(time_orange[-1]), " at quadrant ", str(quad_orange[-1]), '\n']
                        if time_orange[-1] - time_orange[-2] > 2:
                            f.writelines(orange_in)
                            f.writelines(orange_out)
                            time_orange.clear()
                    except:
                        pass

                # white
                if 113 < r < 248 and 111 < g < 246 and 94 < b < 226:
                    quad_white.append(quad(x, y))
                    end_white = time.time()
                    time_white_in = end_white - start
                    time_white.append(int(time_white_in))
                    cv2.putText(frame, color[3], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    try:
                        white_in = ['\n', color[3], " enter in ", str(time_white[0]), " at quadrant ", str(quad_white[-1]), '\n']
                        white_out = ['\n', color[3], " out at ", str(time_white[-1]), " at quadrant ", str(quad_white[-1]), '\n']
                        if time_white[-1] - time_white[-2] > 2:
                            f.writelines(white_in)
                            f.writelines(white_out)
                            time_white.clear()
                    except:
                        pass

        # Write the frame to the output video
        out.write(frame)

        # Display the video
        cv2.imshow('Squares and Circles', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Processed video saved as 'Squares_and_Circles.avi'")
