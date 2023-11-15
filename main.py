import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import logging
import imageio

# Set up logging
logging.basicConfig(level=logging.INFO)


def load_and_process_image(url):
    try:
        arr = np.asarray(
            bytearray(urllib.request.urlopen(url).read()), dtype=np.uint8
        )
        image = cv2.imdecode(arr, -1)
        if image is None:
            raise FileNotFoundError("Image not found.")
        edges = cv2.Canny(image, 100, 200)
        return edges
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


def perform_fft_transformation(coords, n_components, total_length):
    fft_result = np.fft.fft(coords)
    fft_reconstruct = np.zeros_like(fft_result)
    fft_reconstruct[:n_components] = fft_result[:n_components]
    fft_reconstruct[-n_components:] = fft_result[-n_components:]
    reconstructed_coords = np.fft.ifft(fft_reconstruct)
    return reconstructed_coords


def plot_reconstructed_image(ax, image, title):
    ax.imshow(image, cmap="gray")
    ax.set_title(title)


def generate_gif_images(n_steps, fft_length, coords, dimensions):
    gif_images = []
    for i in range(1, n_steps + 1):
        n_components = i * (fft_length // n_steps)
        reconstructed_coords = perform_fft_transformation(
            coords, n_components, fft_length
        )
        x_reconstructed = np.real(reconstructed_coords).astype(int)
        y_reconstructed = np.imag(reconstructed_coords).astype(int)
        x_reconstructed, y_reconstructed = filter_valid_coords(
            x_reconstructed, y_reconstructed, dimensions
        )

        image = np.zeros(
            dimensions, dtype=np.uint8
        )  # Use dimensions for image creation
        image[y_reconstructed, x_reconstructed] = 255
        gif_images.append(image)
    return gif_images


def filter_valid_coords(x, y, shape):
    valid_indices = (x >= 0) & (x < shape[1]) & (y >= 0) & (y < shape[0])
    return x[valid_indices], y[valid_indices]


def main():
    url = "https://as2.ftcdn.net/v2/jpg/00/45/94/11/1000_F_45941111_waPBx3P01ql45vvUWSLHinIXmImriNkU.jpg"
    edges = load_and_process_image(url)
    if edges is None:
        return

    plt.figure(figsize=(15, 10))
    ax1 = plt.subplot(2, 3, 1)
    plot_reconstructed_image(ax1, edges, "Original Edges")

    y, x = np.where(edges == 255)
    coords = x + 1j * y
    fft_length = len(coords)

    n_steps = 200
    plot_interval = n_steps // 5  # Adjust interval for 5 additional plots
    gif_images = generate_gif_images(n_steps, fft_length, coords, edges.shape)

    for i, image in enumerate(gif_images):
        if i % plot_interval == 0:
            plot_index = 2 + (i // plot_interval)
            if plot_index <= 6:  # Ensure we don't exceed the subplot limit
                ax = plt.subplot(2, 3, plot_index)
                n_components = (i + 1) * (
                    fft_length // n_steps
                )  # Calculate the number of components
                plot_reconstructed_image(
                    ax, image, f"{n_components} Components"
                )

    plt.tight_layout()
    plt.show()

    imageio.mimsave("animated_from_fft.gif", gif_images, duration=0.5)


if __name__ == "__main__":
    main()
