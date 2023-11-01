import cv2
import numpy as np
import urllib.request
import imageio


def load_and_edge_detect(image_path):
    try:
        url = "https://as2.ftcdn.net/v2/jpg/00/45/94/11/1000_F_45941111_waPBx3P01ql45vvUWSLHinIXmImriNkU.jpg"
        arr = np.asarray(
            bytearray(urllib.request.urlopen(url).read()), dtype=np.uint8
        )

        image = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise FileNotFoundError("Image not found.")
        edges = cv2.Canny(image, 100, 200)
        return edges
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def coords_to_complex(x, y):
    return x + 1j * y


def filter_valid_coords(x, y, shape):
    valid_indices = (x >= 0) & (x < shape[1]) & (y >= 0) & (y < shape[0])
    return x[valid_indices], y[valid_indices]


def plot_reconstructed_image(ax, image, title):
    ax.imshow(image, cmap="gray")
    ax.set_title(title)


def main():
    # Initialize an empty list to store images for the GIF
    gif_images = []

    edges = load_and_edge_detect("rudolph.jpg")
    if edges is None:
        return

    y, x = np.where(edges == 255)
    coords = coords_to_complex(x, y)
    fft_result = np.fft.fft(coords)
    # play around with the number of steps to see how the GIF changes
    n_steps = 200
    step_size = len(fft_result) // (n_steps + 1)
    reconstructed_image = np.zeros_like(edges)

    for i in range(1, n_steps + 1):
        n_components = i * step_size
        fft_reconstruct = np.zeros_like(fft_result)
        fft_reconstruct[:n_components] = fft_result[:n_components]
        fft_reconstruct[-n_components:] = fft_result[-n_components:]

        reconstructed_coords = np.fft.ifft(fft_reconstruct)
        x_reconstructed = np.real(reconstructed_coords).astype(int)
        y_reconstructed = np.imag(reconstructed_coords).astype(int)

        x_reconstructed, y_reconstructed = filter_valid_coords(
            x_reconstructed, y_reconstructed, reconstructed_image.shape
        )

        reconstructed_image.fill(0)
        reconstructed_image[y_reconstructed, x_reconstructed] = 255

        gif_images.append((reconstructed_image.astype(np.uint8)))

    # Create a GIF
    imageio.mimsave("animated_from_fft.gif", gif_images, duration=0.5)


if __name__ == "__main__":
    main()
