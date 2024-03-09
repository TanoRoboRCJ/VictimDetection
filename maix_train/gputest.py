import tensorflow as tf
a = tf.random.normal([1000, 1000])
print(tf.reduce_sum(a))
tf.config.list_physical_devices('GPU')