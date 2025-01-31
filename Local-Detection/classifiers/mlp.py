# MLP model 
import keras 
import numpy as np
import time

from utils.utils import save_logs
from utils.utils import calculate_metrics
from sklearn.neural_network import MLPClassifier
from keras.utils import to_categorical

class Classifier_MLP:

	def __init__(self, output_directory, input_shape, nb_classes, verbose=False,build=True):
		self.output_directory = output_directory
		if build == True:
			self.model = self.build_model(input_shape, nb_classes)
			#if(verbose==True):
				#self.model.summary()
			self.verbose = verbose
			#self.model.save_weights(self.output_directory + 'model_init.hdf5')
		return

	def build_model(self, input_shape, nb_classes):
		batch_size = 4096
		nb_epochs = 20

		#mini_batch_size = int(min(x_train.shape[0]/10, batch_size))
		mini_batch_size = batch_size     
		print('selectMLP_L4NV25')
		model = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(20,25,22,16,), verbose=True,random_state=1, batch_size=mini_batch_size, max_iter=nb_epochs)
		#model = keras.models.Model(inputs=input_layer, outputs=output_layer)

		#model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adadelta(),
			#metrics=['accuracy'])

		#reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.5, patience=200, min_lr=0.1)

		#file_path = self.output_directory+'best_model.hdf5' 

		#model_checkpoint = keras.callbacks.ModelCheckpoint(filepath=file_path, monitor='loss', 
			#save_best_only=True)

		#self.callbacks = [reduce_lr,model_checkpoint]

		return model

	def fit(self, x_train, y_train, x_val, y_val,y_true):
		#if len(keras.backend.tensorflow_backend._get_available_gpus())==0:
			#print('error')
			#exit()
		# x_val and y_val are only used to monitor the test loss and NOT for training  

		y_train = to_categorical(y_train)
		start_time = time.time() 
		print('xshape', x_train.shape)
		print('yshape', y_train.shape)
		hist = self.model.fit(x_train, y_train)
		
		duration = time.time() - start_time

		#self.model.save(self.output_directory + 'last_model.hdf5')

		#model = keras.models.load_model(self.output_directory+'best_model.hdf5')

		y_pred = self.model.predict(x_val)

		# convert the predicted from binary to integer 
		y_pred = np.argmax(y_pred , axis=1)

		save_logs(self.output_directory, hist, y_pred, y_true, duration)

		#keras.backend.clear_session()

	def predict(self, x_test, y_true,x_train,y_train,y_test,return_df_metrics = True):
		model_path = self.output_directory + 'best_model.hdf5'
		model = keras.models.load_model(model_path)
		y_pred = model.predict(x_test)
		if return_df_metrics:
			y_pred = np.argmax(y_pred, axis=1)
			df_metrics = calculate_metrics(y_true, y_pred, 0.0)
			return df_metrics
		else:
			return y_pred