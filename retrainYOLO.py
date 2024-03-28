from ultralytics import YOLO
import gpu_availablility
import cv2
import numpy as np

if __name__ == '__main__':

    # Check if GPU (mps) is available
    gpu = gpu_availablility.checkgpu()
    print(gpu)

    # Load a COCO-pretrained YOLOv8n model
    # Model	    size    mAPval 	Speed   Speed 	params(M)	FLOPs (B)
    # YOLOv8n	640     37.3	80.4	0.99	3.2	        8.7
    # YOLOv8s	640	    44.9	128.4	1.20	11.2	    28.6
    # YOLOv8m	640	    50.2	234.7	1.83	25.9	    78.9
    # YOLOv8l	640	    52.9	375.2	2.39	43.7	    165.2
    # YOLOv8x	640	    53.9	479.1	3.53	68.2	    257.8
    model = YOLO('yolov8n.pt')

    # Train the model on the COCO8 example dataset for 100 epochs
    # optimizer = 'auto'
    # Choice of optimizer for training. Options include SGD, Adam, AdamW, NAdam, RAdam, RMSProp etc.,
    # or auto for automatic selection based on model configuration. Affects convergence speed and stability.
    # lr0 = 0.01
    # Initial learning rate (i.e. SGD=1E-2, Adam=1E-3) . Adjusting this value is crucial for the
    # optimization process, influencing how rapidly model weights are updated.
    # lrf = 0.01
    # Final learning rate as a fraction of the initial rate = (lr0 * lrf),
    # used in conjunction with schedulers to adjust the learning rate over time.
    # momentum = 0.937
    # Momentum factor for SGD or beta1 for Adam optimizers, influencing the incorporation of past gradients
    # in the current update.
    # -----DOCS-----> https://docs.ultralytics.com/modes/train/#train-settings
    # DFL loss 'considers' the problem of class imbalance while training a NN.
    # Class imbalance occurs when there is one class which occurs too frequently and another which occurs less.
    # For ex: In street imagery say 100 photos, one can have 200 cars and only 10 bicycles. One wants to detect both
    # cars and bikes. This is case of class imbalance, when you train a NN, since there are a lot of cars, NN will learn
    # to accurately localize cars whereas, bikes are too less so, it might not learn to localize it properly. With dfl
    # loss, every time the NN tries to classify bike there is increased loss. So, now NN puts more importance on less
    # frequent classes. This explanation is on a very general level. To know more, refer the paper on Focal loss and
    # then on DFL. There is an explanation on Matlab page:
    # https://www.mathworks.com/matlabcentral/fileexchange/104395-dual-focal-loss-dfl?s_tid=FX_rc2_behav
    # The class loss is computed based on the binary cross-entropy loss for the confidence scores of each
    # and every predicted bounding box. The box loss is summed up over object spatial locations, object shapes and
    # different aspect ratios and is computed as the mean squared error (MSE) between the predicted bounding box
    # parameters and the ground truth ones.
    # Precision is defined as the number of true positives over the number of true positives plus
    # the number of false positives. -> alle echten predicted positiven aus allen predicted positiven
    # Recall is defined as the number of true positives over the number of true positives plus
    # the number of false negatives. -> alle echten predicted positiven aus der Menge aller positiven
    # Precision Recall Curve sollte waagerecht sein udn dann am Ende abfallen.
    # mAP sollte auf 1 kommen... ist basically die Fläche unter PRC.
    results = model.train(data='dataset/data.yaml', epochs=500, imgsz=640, batch=32, patience=100, device=gpu)

    # Run inference with the YOLOv8n model on the 'bus.jpg' image
    results = model('dataset/test/images/20240318_133936_HoloLens.jpg', device=gpu)

    # Get Class_list
    class_list = model.model.names

    # Extract boundingboxes, classes and confidence scores
    result = results[0]
    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")
    confidences = np.array(result.boxes.conf.cpu(), dtype="double")

    # Read image for displaying results
    image = cv2.imread("dataset/test/images/20240318_133936_HoloLens.jpg")

    # Add boundingboxes, class names and confidence scores to image
    for bbox, cls, conf in zip(bboxes, classes, confidences):
        (x, y, x2, y2) = bbox
        cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 225), 3)
        print(str(cls))
        print("x", x, "; y", y)
        cls_name = class_list[cls]
        cv2.putText(image, str(cls) + "; " + str(cls_name) + "; " + str("%.2f" % round(conf, 2)), (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 225), 3)

    # resize the image for display
    image = cv2.resize(image, (image.shape[1]//2, image.shape[0]//2))

    # Display image
    cv2.imshow("Img", image)
    key = cv2.waitKey(0)
