import cv2
from ultralytics import YOLO
import numpy as np
import os
import gpu_availablility


def check_dir():
    """
    Cheks if the directory exists and if not, it creates it, otherwise asks the user if they want to recalculate the
    images.

    Args:
         None

    Returns:
        void
    """
    if os.path.isdir("runs/detect/train{}/predictions".format(trainNr)):
        in_msg = input('Predictions already satisfied. Do you want to recalculate predictions? [Y/N]')
        if in_msg == 'Y':
            pass
        elif in_msg == 'N':
            exit('Predictions already satisfied, exiting program.')
        else:
            check_dir()
    else:
        os.mkdir("runs/detect/train{}/predictions".format(trainNr))
        print('predictions directory created.')


def check_display():
    """
    Cheks if the user wants to display the images after calculation.

    Args:
         None

    Returns:
        Boolean for whether the user wants to display the images.
    """
    disp = input('Do you want the images to be displayed? [Y/N]')
    if disp == 'Y':
        print('Press ESC to move to next prediction.')
        return True
    elif disp == 'N':
        return False
    else:
        print('Invalid, try again.')
        return check_display()


def initialise_model(path, display_bool):
    """
    Loads the best model of a given run and prints a list of all the classes and calls the iteration of the directory
    of the test images.

    Args:
         path (string): path to the images.
         display_bool (bool): whether to display the images after calculation.

    Returns:
        void
    """
    # load model
    model = YOLO("runs/detect/train{}/weights/best.pt".format(trainNr))
    print('Model loaded.')
    print('==============================================================================')

    # get class names
    class_list = model.model.names
    print('Class List:', class_list)
    print('==============================================================================')

    iterate_directory(model, path, class_list, display_bool)


def iterate_directory(model, path, class_list, display_bool):
    """
    Iterates through a given directory and calls the method for running the model.

    Args:
         model (YOLO model): model with the best result of a given training run.
         path (string): path to the test images.
         class_list (list): list of classes that the model is trained for.
         display_bool (bool): whether to display the images after calculation.

    Returns:
        void
    """
    directory = os.fsencode(path)
    i = 0

    print('Calculating predictions...')

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        if filename.endswith(".jpg"):
            run_model(model, os.path.join(path, str(filename)), class_list, display_bool, i)
            i += 1

        else:
            exit('No images found for {}'.format(
                'C:/Users/manue/PycharmProjects/ML-for_HoloLens-py3.9/dataset/test/images'))


def run_model(model, final_path, class_list, display_bool, i):
    """
    Runs the model and generates the output images, as well as saving the predictions in a given directory.
    Later calls the print_image method, depending on display_bool.

    Args:
         model (YOLO model): model with the best result of a given training run.
         final_path (string): path to the individual test images.
         class_list (list): list of classes that the model is trained for.
         display_bool (bool): whether to display the images after calculation.

    Returns:
        void
    """
    # Run inference with the YOLOv8n model on an image
    results = model(final_path, device=gpu)

    # Extract bounding boxes, classes and confidence scores
    result = results[0]
    bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    classes = np.array(result.boxes.cls.cpu(), dtype="int")
    confidences = np.array(result.boxes.conf.cpu(), dtype="double")

    # CV2 Read image for displaying the results
    image = cv2.imread(final_path)

    # Add bounding boxes, class names and confidence scores to image
    for bbox, cls, conf in zip(bboxes, classes, confidences):

        (x, y, x2, y2) = bbox
        cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 225), 3)

        cls_name = class_list[cls]

        # print results on images
        if y <= 25:
            cv2.putText(image, str(cls) + "; " + str(cls_name) + "; " + str("%.2f" % round(conf, 2)), (x, y2 - 5),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 225), 3)
        else:
            cv2.putText(image, str(cls) + "; " + str(cls_name) + "; " + str("%.2f" % round(conf, 2)), (x, y + 35),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 225), 3)

        # print results in console
        if display_bool:
            print('Found this in image:')
            print("x", x, "; y", y)
            print(str(cls), str(cls_name))

    # save .jpg
    cv2.imwrite('runs/detect/train{}/predictions/prediction{:03d}.jpg'.format(trainNr, i), image)
    print('Image saved in: runs/detect/train{}/predictions/prediction{:03d}.jpg'.format(trainNr, i))
    print('=========================================================')

    if display_bool:
        # resize the image for display
        image = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))
        display_image(image)
    else:
        pass


def display_image(image):
    """
    Displays the resulting images with bounding boxes.

    Args:
         image (np.ndarray):  containing the images pixel information.

    Returns:
        void
    """
    # Display the image
    cv2.imshow("Img", image)
    key = cv2.waitKey(0)


# check if directory is present and exit if necessary
trainNr = '6'
path = r"C:\Users\manue\PycharmProjects\ML-for_HoloLens-py3.9\dataset\test\images"

check_dir()

# check for gpu
gpu = gpu_availablility.checkgpu()
# check if the user wants to display the resulting images with bboxes
display_bool = check_display()
# initialise model, get the images, run the inference, save the images and display the images
initialise_model(path, display_bool)
