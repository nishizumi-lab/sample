import tensorflow as tf
mnist = tf.keras.datasets.mnist
import time

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(512, activation=tf.nn.relu),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

start = time.perf_counter()
model.fit(x_train, y_train, epochs=5)
end = time.perf_counter()
print(f"Elapsed time : {end - start:.3f} s.")

model.evaluate(x_test, y_test)