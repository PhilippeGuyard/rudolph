# Line Drawings with FFT (or PCA) and Python

## Overview

This repository contains code for illustrating decomposing line drawings using Fast Fourier Transform (FFT) and Python. The project leverages OpenCV for edge detection and NumPy for FFT decomposition and reconstruction.
I have also included a 'bonus track' with the same idea, but using Principle Components Analysis (PCA) instead of FFT. This is in the 'pca.py' file. This is not so interesting as with 3 components, the image is already reconstructed. However, it is interesting to see how the components look like.
There is also a variant of the code in gif.py to produce a gif from the series of FFT decompositions.

## Features

- Edge Detection using OpenCV's Canny algorithm
- FFT Decomposition and Reconstruction using NumPy
- PCA Decomposition and Reconstruction using Scikit learn
- Visualisation using Matplotlib
- gif creation using Imagio

## Detailed Explanations

For a detailed explanation of each step of the FFT, including the logic behind FFT and the image processing techniques used, check out the Jupyter Notebook hosted on Google Colab: [Detailed Notebook](https://colab.research.google.com/drive/1J0PDOwg7EVWOZkXc7qUab7fnZijvnO7i?usp=sharing).

## Bonus features

- PCA Decomposition and Reconstruction using Scikit learn (in pca.py)
- gif creation using Imagio (in gif.py)

## Requirements

- Python 3.x
- OpenCV
- NumPy
- Matplotlib
- Scikit learn (for PCA)
- Imagio (for creating a gif)

## Contributing

Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.