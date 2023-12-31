import cv2
import time
import requests
import numpy as np
import matplotlib.pyplot as plt

m_frame = 0
s_frame = 0

def point_in_trapezoid(x, y, x1, y1, x2, y2, x3, y3, x4, y4):
    def is_left(p1, p2, p):
        return (p2[0] - p1[0]) * (p[1] - p1[1]) - (p2[1] - p1[1]) * (p[0] - p1[0])

    def point_in_triangle(p, p1, p2, p3):
        b1 = is_left(p1, p2, p) < 0
        b2 = is_left(p2, p3, p) < 0
        b3 = is_left(p3, p1, p) < 0
        return b1 == b2 == b3

    return point_in_triangle((x, y), (x1, y1), (x2, y2), (x3, y3)) or point_in_triangle((x, y), (x1, y1), (x3, y3), (x4, y4))

# Define the trapezoid points
x1, y1 = 766, 456
x2, y2 = 1124, 454
x3, y3 = 686, 755
x4, y4 = 1318, 733

def call_reset_api():
    try:
        response = requests.get('http://10.111.194.26:18088/reset')
        if response.status_code == 200:
            print("Reset API called successfully.")
        else:
            print("Failed to call Reset API.")
    except requests.RequestException as e:
        print(f"Error calling Reset API: {e}")

# Defining a function motionDetection
def motionDetection(debug=False, delay_time=1):
    # capturing video in real time
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("file2.mov")

    # reading frames sequentially
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    total_motion_detected = False
    motion_detected = False
    motion_start_time = time.time()
    printed_once = False
    motion_threshold = 600  # Contour area threshold to detect motion
    min_ball_size = 15  # Minimum ball size (width and height)
    max_ball_size = 60  # Maximum ball size (width and height)
    global m_frame
    global s_frame

    while cap.isOpened():
        # Difference between the frames
        diff = cv2.absdiff(frame1, frame2)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)

        # Identify the sky-blue region
        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        lower_sky_blue = np.array([90, 60, 40])  # Lower threshold for sky-blue color
        upper_sky_blue = np.array([130, 255, 255])  # Upper threshold for sky-blue color
        mask_sky_blue = cv2.inRange(hsv, lower_sky_blue, upper_sky_blue)
        masked_frame = cv2.bitwise_and(frame1, frame1, mask=mask_sky_blue)

        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = False

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            aspect_ratio = float(w) / h if h != 0 else 0

            # Check if the contour is similar to a ball shape, is moving, and has appropriate size,
            # and lies within the sky-blue region
            if point_in_trapezoid(x, y, x1, y1, x2, y2, x3, y3, x4, y4) and area > motion_threshold \
                    and 0.7 <= aspect_ratio <= 1.3 and min_ball_size <= w <= max_ball_size \
                    and min_ball_size <= h <= max_ball_size and mask_sky_blue[y:y + h, x:x + w].any():
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame1, "STATUS: {}".format('MOTION DETECTED'), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (217, 10, 10), 2)
                if debug:
                    print("MOVING Ball Size - Width:", w, " Height:", h, " FRAME: ", m_frame)
                if m_frame >= 20:
                    total_motion_detected = True

                s_frame = 0
                m_frame += 1
                motion_start_time = time.time()
                printed_once = False  # Reset to allow printing when there's motion
                break  # Stop the loop after detecting the first contour resembling a ball

        if not motion_detected and time.time() - motion_start_time >= delay_time and not printed_once:
            s_frame += 1
            m_frame = 0
            if s_frame > 6 and total_motion_detected == True:
                total_motion_detected = False
                printed_once = True
                print("TRIGGER - Current Time:", time.time(), "- Motion Start Time:", motion_start_time, " FRAME:", s_frame)

        cv2.imshow("Video", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(50) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Enable debug mode when debugging
    motionDetection(debug=True, delay_time=1.5)

