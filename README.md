# HoloYOLO-models

HoloYOLO-models is a project for object detection on the HoloLens 2. In this part of the project different YOLOv8
architectures are tested, using the ultralytics library.

## Installation

Clone repository and install torch before ultralytics. This way you make sure to be able to install the requirements
for cuda correctly. This ultralytics should install all the different packages you need, such as NumPy.

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install ultralytics
```

## Usage

### retrainYOLO.py

retrainYOLO.py is used to retrain YOLOv8. Here you can easily change the different YOLO-versions.
Simply change following line of code. Different models can be found [here](https://docs.ultralytics.com/models/).

```python
model = YOLO('yolov8n.pt')
```

You can also adjust the training parameters in the following line. For more training parameters visit 
the [ultralytics docs](https://docs.ultralytics.com/modes/train/#train-settings).

```python
results = model.train(data='dataset/data.yaml', epochs=500, imgsz=640, batch=64, patience=100, device=gpu)
```

Before starting the training process be sure to update the 'data.yaml' file, as this file is used to find the training,
validation and test data, as well as the configuration for the classes your model is supposed to find.


### predict_new_images.py

predict_new_images.py is used to test the trained models. Here you can simply change the number of your training run, e.g:

```python
trainNr = '4'
```

Be sure to change the path to your personal dataset.

```python
path = r"\Path\to\your\dataset\test\images"
```
