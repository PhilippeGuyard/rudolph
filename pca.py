# Importing Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from sklearn.decomposition import PCA

# Downloading and Loading Image
url = "https://authorfoleywestern.files.wordpress.com/2013/12/santa-and-sleigh.jpg"
arr = np.asarray(bytearray(urllib.request.urlopen(url).read()), dtype=np.uint8)
image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

# Flatten the image into a 2D array
h, w, c = image.shape
image_flattened = image.reshape(h * w, c)

# Create an empty array for reconstruction
reconstructed_image = np.zeros_like(image)

# Display the original image
plt.figure(figsize=(15, 10))
plt.subplot(2, 3, 1)
plt.imshow(image)
plt.title("Original Image")

# Reconstructing with Increasing Components
for i in range(1, 4):  # Using 1, 2, and 3 components for demonstration
    pca = PCA(n_components=i)
    reconstructed_data = pca.inverse_transform(
        pca.fit_transform(image_flattened)
    )

    # Reshape the reconstructed data back into the original image shape
    reconstructed_image = reconstructed_data.reshape(h, w, c).astype(np.uint8)

    # Plotting
    plt.subplot(2, 3, i + 1)
    plt.imshow(reconstructed_image)
    plt.title(f"{i} Components")

plt.tight_layout()
plt.show()
