print("GPU Check")

import tensorflow as tf
import platform

print(f"Python Platform: {platform.platform()}")
print(f"Tensor Flow Version: {tf.__version__}")

is_gpu_available = len(tf.config.list_physical_devices('GPU')) > 0
print("GPU is", "available ✅" if is_gpu_available else "not available ❌")