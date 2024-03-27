from keras.preprocessing.image import *

# lets define a ImageDataGenerator object
# change the arguments below as per the requirment
idg = ImageDataGenerator(rescale = 1/255,
                                     horizontal_flip = True,
                                     rotation_range = 30,
                                     width_shift_range = 0.3,
                                     height_shift_range = 0.3,
                                     brightness_range=[0.2,1.0],
                                     zoom_range=[0.5,1.0]
                         )


# sample code to check if our agumentation is working for a single image
# lets read our image to be processed - change the directory as needed
image = load_img("thanos.jpg")
input_arr = img_to_array(image)
# reshaping the image to a 4D array to be used with keras flow function.
input_arr = input_arr.reshape((1,) + input_arr.shape)

i = 0
# keras flow function usually work for batches
# chnage the directory and number of iterations as required
for batch in idg.flow(input_arr, batch_size=1,
                          save_to_dir='/content/cat', save_prefix='cat', save_format='jpeg'):
    i += 1
    if i > 6:
        break  # need to break the loop otherwise it will run infinite times



import albumentations as A

transform = A.Compose([
    A.RandomCrop(width=450, height=450),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.2),
], bbox_params=A.BboxParams(format='yolo'))
transformed = transform(image=image, bboxes=bboxes)
transformed_image = transformed['image']
transformed_bboxes = transformed['bboxes']

