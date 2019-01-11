# Imports
from parameters import *

from keras.models import load_model

import time
import matplotlib.pyplot as plt
import numpy as np

from imageio import imread
from imageio import mimsave

from sklearn.datasets import make_blobs
from sklearn.datasets import make_gaussian_quantiles
from sklearn.datasets import make_moons
from sklearn.datasets import make_circles

# Loads the saved model
model = load_model('{}{}'.format(path_models, NAME))

###  Test Set  ###
# Creates a new data set that the model will be tested with
x_test, y_test = make_blobs(n_samples = n_testing_samples + n_training_samples, 
	n_features = n_features,
	centers = n_classes,
	center_box = center_box,
	cluster_std =  cluster_std, 
	random_state = seed)
x_test = x_test[-n_testing_samples:]
y_test = y_test[-n_testing_samples:]

# Gets the predictions of the model on the test set
predictions = model.predict(x_test)
# Takes the position of the largest output prediction value for each sample (gets the predicted class)
predictions = [predictions[i,:].argmax() for i in range(int(predictions.shape[0]))]

# Measures the accuracy of the predictions
n_correct = 0
for i in range(n_testing_samples):
	if (predictions[i] == y_test[i]):
		n_correct += 1
accuracy = n_correct / n_testing_samples
print("Accuracy = {}%".format(str(accuracy * 100.0)))

# scatterplot of the predictions generated by the neural network
plt.scatter(x_test[:, 0], x_test[:, 1], c = predictions, cmap = colors)
plt.draw()
plt.savefig('{}{}'.format(path_plots, 'prediction_set.png'))
plt.close()

# scatterplot of the actual test data
plt.scatter(x_test[:, 0], x_test[:, 1], c = y_test, cmap = colors)
plt.draw()
plt.savefig('{}{}'.format(path_plots, 'test_set.png'))


###  Area Map Set  ###
xstart = int((x_test[:, 0].min() - 1) * points_per_int) # min start point of the x data
xrang = int((x_test[:, 0].max() + 1) * points_per_int - xstart) # range of the data on x

ystart = int((x_test[:, 1].min()  - 1) * points_per_int) # min start poing of the y data
yrang = int((x_test[:, 1].max() + 1) * points_per_int - ystart) # range of teh data on y

# Creates an array with all the coordinates of area map set
area_map_set = np.array([[x + xstart, y + ystart] for x in range(xrang) for y in range(yrang)])
area_map_set = area_map_set / points_per_int

# Gets the filepaths of the saved models/weights from the training process
weightpaths = ['{}weights-{}.hdf5'.format(path_models, str(i + 1).zfill(2)) for i in range(n_epochs)]
paths = []

# Algorithim to generate all the area maps for each model in training
for n, weightpath in enumerate(weightpaths):
	print('Epoch Prediction #{}'.format(str(n)))

	# gets the current model for the epoch
	current_model = load_model(weightpath)

	# gets the prediction the model made for the area map set
	pred = current_model.predict(area_map_set)
	pred = [pred[i,:].argmax() for i in range(int(pred.shape[0]))]

	# saves the path that the image will be saved to
	path = '{}{}.png'.format(path_plots, 'prediction_map-{}'.format(str(n)))
	paths.append(path)

	# draws the current area map and the test set overtop it, saves the scatter
	plt.scatter(x_test[:, 0], x_test[:, 1], c = y_test, cmap =colors)
	plt.scatter(area_map_set[:, 0], area_map_set[:, 1], c = pred, alpha = alpha, cmap = colors)
	plt.draw()
	plt.savefig(path)
	plt.close()

# saves the final area map - test plot as result.png
plt.scatter(x_test[:, 0], x_test[:, 1], c = y_test, cmap = colors)
plt.scatter(area_map_set[:, 0], area_map_set[:, 1], c = pred, alpha = 0.1, cmap = colors)
plt.savefig('{}{}'.format(path_plots, 'result.png'))
plt.close()

# combines all the areamap plots into a gif
images = []
for img in paths:
    images.append(imread(img))

cur_time = time.time()
mimsave('{}neural_network{}.gif'.format(path_networks, cur_time), images)
mimsave('{}neural_network_current.gif'.format(path_plots), images)

# Output message to complete execution of code
print("Plots and predictions saved, done executing tester.py")

