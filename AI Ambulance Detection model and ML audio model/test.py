from ultralytics import YOLO
import cv2
import math
import serial

arduino = serial.Serial('COM5', 9600)
# IP webcam URLs for four cameras
ip_webcam_urls = [
    "http://192.168.1.101:8080/video",  # Camera 1 - First direction
    # "http://192.168.1.103:8080/video",  # Camera 2 - Second direction
    # "http://192.168.1.102:8080/video",  # Camera 3 - Third direction
    # "http://192.168.1.104:8080/video"  # Camera 4 - Fourth direction
]

# Initialize four video capture objects
caps = [cv2.VideoCapture(url) for url in ip_webcam_urls]

# Set display size for all cameras
display_width = 400
display_height = 400

for cap in caps:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, display_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, display_height)

# Create four video writers for each camera
outs = [
    cv2.VideoWriter(f'output_{i}.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (display_width, display_height))
    for i in range(4)
]

# Initialize YOLO model
model = YOLO("final.pt")
classNames = ["ambulance"]

# Number of frames to skip
skip_frames = 2

frame_count = 15


# Function for first direction
def process_first_direction(frame):
    # TODO: Implement your logic for the first direction detection here
    print("Detected in the first direction")
    arduino.write('1'.encode())

# # Function for second direction
# def process_second_direction(frame):
#     # TODO: Implement your logic for the second direction detection here
#     print("Detected in the second direction")
#     arduino.write('2'.encode())
#     # ...
#
#
# # Function for third direction
# def process_third_direction(frame):
#     # TODO: Implement your logic for the third direction detection here
#     print("Detected in the third direction")
#     arduino.write('3'.encode())
#     # ...
# #
# #
# # # Function for fourth direction
# def process_fourth_direction(frame):
#      # TODO: Implement your logic for the fourth direction detection here
#      print("Detected in the fourth direction")
#      arduino.write('4'.encode())
#      # ...

while True:
    for i, cap in enumerate(caps):
        success, img = cap.read()
        if frame_count % skip_frames == 0:
            img = cv2.resize(img, (display_width, display_height))  # Resize image for display

            results = model(img, stream=True)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    class_name = classNames[cls]
                    label = f'{class_name}{conf}'
                    t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                    c2 = x1 + t_size[0], y1 - t_size[1] - 3
                    cv2.rectangle(img, (x1, y1), c2, [255, 0, 255], -1, cv2.LINE_AA)  # filled
                    cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

                    # Call different functions based on the camera index
                    if i == 0:
                        process_first_direction(img)
                    elif i == 1:
                        process_second_direction(img)
                    elif i == 2:
                        process_third_direction(img)
                    elif i == 3:
                        process_fourth_direction(img)

            outs[i].write(img)
            cv2.imshow(f"Camera {i + 1}", img)
            if cv2.waitKey(1) & 0xFF == ord('1'):
                break
    frame_count += 1

# Release resources
for cap in caps:
    cap.release()

for out in outs:
    out.release()

cv2.destroyAllWindows()
