import os
import ultralytics
from roboflow import Roboflow
from codecarbon import EmissionsTracker


'''
    pip install ultralytics==8.0.20
    pip install roboflow
    
'''
if __name__ == "__main__":

    HOME = os.getcwd()
    print(HOME)

    ultralytics.checks()

    rf = Roboflow(api_key="KYVsDSdAj7mkkTzXLzEN")
    project = rf.workspace("cvanddl").project("detection-bag-logo")
    dataset = project.version(3).download("yolov8", location="/home/vrai/datasets")
    print(dataset.location)

    os.system('cd ' + HOME)
    dataset_location = dataset.location
    command = "yolo task=detect mode=train model=yolov8s.pt data="+dataset_location+"/data.yaml epochs=50 imgsz=800 plots=True workers=2 val=False"
    tracker = EmissionsTracker()
    tracker.start()
    os.system(command)
    tracker.stop()

    command2 = "yolo task=detect mode=val model="+HOME+"/runs/detect/train/weights/best.pt data="+dataset_location+"/data.yaml"
    os.system(command2)

    command3 = "yolo task=detect mode=predict model="+HOME+"/runs/detect/train/weights/best.pt conf=0.25 source="+dataset_location+"/test/images save=True"
    os.system(command3)
