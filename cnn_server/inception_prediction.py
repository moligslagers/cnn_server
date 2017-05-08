import tensorflow as tf
import numpy as np
from slim.preprocessing import preprocessing_factory as proc
from slim.nets import nets_factory as nets

slim = tf.contrib.slim

inception_path = '/home/markus/projects/cnn_server/model/root/inception_v3.ckpt'
flower_path = '/home/markus/projects/cnn_server/model/root/'
model_path = flower_path
classes = 5
image_name = 'hund2.jpg'
# PREPROCESSING
preprocessing_fn = proc.get_preprocessing('inception_v3', is_training=False)
network_fn = nets.get_network_fn('inception_v3', classes)

image_file = tf.gfile.FastGFile(image_name, 'rb').read()

image_tensor = tf.image.decode_jpeg(image_file, channels=0)

# image = image_tensor.eval()

image = preprocessing_fn(image_tensor, 299, 299)

image_res = tf.reshape(image, [1,299,299,3])
	
logits, endpoints = network_fn(image_res)

# variables_to_restore = slim.get_model_variables()
restorer = tf.train.Saver()

predictions = None

with tf.Session() as sess:
	tf.global_variables_initializer().run()
	
	# sess.run(image)
	# image = image.eval()
	# print(image.shape)
	if classes <= 5:
		restorer.restore(sess, tf.train.latest_checkpoint(model_path))
	else:
		restorer.restore(sess, model_path)
	
	sess.run(endpoints)
	# print(endpoints)
	predictions = endpoints['Predictions'].eval()
	logits = endpoints['Logits'].eval()
	

if classes > 5:
	labels = []
	f = open('labels.txt')
	for line in f:
		labels.append(line)

	print('%s , %s' %( labels[np.argmax(predictions[0])], predictions[0][np.argmax(predictions[0])] ) )
else:
	print(predictions)
