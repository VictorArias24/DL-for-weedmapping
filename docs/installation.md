# Installation

## Dependencies

In order to properly run all scripts in this repository, ensure you have all the following dependencies installed in your environment:

* **Tensorflow** (tested with v2.13.1)
* 🤗 **Hugginface datasets**
* **Numpy >=1.17.3**
* **CUDA drivers**
* Matplotlib (for compression visualization)
* PIL (for loading images)


## Lambda Stack

Lambda Stack provides a one line installation and managed upgrade path for: PyTorch®, TensorFlow, CUDA, cuDNN, and NVIDIA Drivers. It's compatible with Ubuntu 22.04 LTS and 20.04 LTS. More info [here](https://lambdalabs.com/lambda-stack-deep-learning-software).

### Install Lambda Stack in one command (Ubuntu)
```bash
wget -nv -O- https://lambdalabs.com/install-lambda-stack.sh | sh -
sudo reboot
```

### Create an Ubuntu 20.04 Docker image with PyTorch® & TensorFlow support (Windows & MacOS)
Build a Docker image for Ubuntu 20.04 (focal). You can substitute focal for bionic or xenial to change the ubuntu version.
```bash
sudo docker build -t lambda-stack:20.04 -f Dockerfile.focal git://github.com/lambdal/lambda-stack-dockerfiles.git
```

## Install the addional libraries with using pip
The easiest way to get started is to install all addtional libraries is using pip. Start off with installing Datasets

```bash
pip install datasets
```

Then some other optional libraries for using jupyterlab and more complex visualizations
```bash
pip install jupyterlab
pip install seaborn
```


