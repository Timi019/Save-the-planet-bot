# imports
from keras.models import load_model
from PIL import Image, ImageOps
import numpy

#function
def detect_trash(path, model,labels):
  # Disable scientific notation for clarity
  numpy.set_printoptions(suppress=True)

  # Load the model
  model = load_model(model, compile=False)

  # Load the labels
  class_names = open(labels, "r").readlines()

  # Create the array of the right shape to feed into the keras model
  # The 'length' or number of images you can put into the array is
  # determined by the first position in the shape tuple, in this case 1
  data = numpy.ndarray(shape=(1, 224, 224, 3), dtype=numpy.float32)

  # Replace this with the path to your image
  image = Image.open(path).convert("RGB")

  # resizing the image to be at least 224x224 and then cropping from the center
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

  # turn the image into a numpy array
  image_array = numpy.asarray(image)

  # Normalize the image
  normalized_image_array = (image_array.astype(numpy.float32) / 127.5) - 1

  # Load the image into the array
  data[0] = normalized_image_array

  # Predicts the model
  prediction = model.predict(data)
  index = numpy.argmax(prediction)
  class_name = class_names[index]
  confidence_score = prediction[0][index]

  # Print prediction and confidence score
  #print("Class:", class_name[2:], end="")
  #print("Confidence Score:", confidence_score)

  return class_name[2:], confidence_score