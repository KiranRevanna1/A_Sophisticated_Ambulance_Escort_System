from ultralytics import YOLO
model = YOLO("yolov8m-seg.pt")
model.predict(source = 0, show=True,save=True,show_labels=False,show_conf=True,conf=0.5,save_txt=False, save_crop=False, line_width=2, box=True, visualize=False)
