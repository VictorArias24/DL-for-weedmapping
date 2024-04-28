# Dataset Requirements

This project uses the 🤗[Huggingface](https://huggingface.co/docs/datasets/index) Dataset library format to consume data in the training and evaluation process. With this library, you can load your dataset with just one line of code and use powerful data processing methods to quickly prepare your data for training in a deep learning model.

*Note:* [**This project includes the same script loaded in the Huggingface Hub**](https://huggingface.co/datasets/viarias/remote_sensing_2018_weedmap/tree/main). To create your own script, use the one located in *datasets/remote_sensing_2018_weedmap* as a reference. Please note that you can select the dataset for both campaigns: **Sequoia** and **RedEdge** (these names are a reference to the sensors used to capture the pictures). More info about the dataset [here](https://projects.asl.ethz.ch/datasets/doku.php?id=weedmap:remotesensing2018weedmap).


## Creating the Loading Script for the Dataset

The dataset loading script defines a dataset's splits and configurations and handles the downloading and generation of a dataset. The steps described here are specifically for this dataset, but the structure is the same for any image dataset. For a complete reference go to the *Loading script* section in the following [link](https://huggingface.co/docs/datasets/image_dataset).


### Defining the Variables


One of the first things to define is the URLs where the dataset is located. In this case, we only need the zip files where the tiles/sections of multispectral images contain:

```python
_URLS = {
    "RED_EDGE": "http://robotics.ethz.ch/~asl-datasets/2018-weedMap-dataset-release/Tiles/RedEdge.zip",
    "SEQUOIA": "http://robotics.ethz.ch/~asl-datasets/2018-weedMap-dataset-release/Tiles/Sequoia.zip",
}
```

Then, other secondary things are defined, things as the dictionary of classes, the channels' names for each dataset, and the orthomosaic maps for training and testing:

```python
WEEDMAP_CLASSES = OrderedDict(
    {
        0: "BACKGROUND",
        1: "CROP",
        2: "WEED",
    }
)

SEQUOIA_CHANNELS = ['CIR', 'G', 'NDVI', 'NIR', 'R', 'RE']
SEQUOIA_SPLIT = {
    "train": ["006", "007"],
    "test": ["005"],
}

REDEDGE_CHANNELS = ['B', 'CIR', 'G', 'NDVI', 'NIR', 'R', 'RE', "RGB"]
REDEDGE_SPLIT = {
    "train": ["000", "001", "002", "004"],
    "test": ["003"],
}
```

Like the documentation, we created a class with three methods to help build the dataset object, and additionally necessary to define an external function and a class. The function manages the paths for a multispectral dataset, and the class is needed to create multiple configurations like subsets in the same dataset.

```python
class WeedMapConfig(datasets.BuilderConfig):
    """BuilderConfig for WeedMap."""
    def __init__(self, data_url, **kwargs):

class WeedMap(datasets.GeneratorBasedBuilder):
    """Remote Sensing 2018 Weed Map Dataset."""

    def _info(self):

    def _split_generators(self, dl_manager):

    def _generate_examples(self, images, metadata_path):


def create_list_paths(total_files_path, subset="red_edge", split_section="train"):
```

For this particular case, we have two configurations, one for the **red edge** campaign and another for the **sequoia** campaign both work as two independent datasets with train/test splits. Now, if you want to load the red_edge configuration, they can use the configuration name:

```python
>>> from datasets import load_dataset
>>> rededge_dataset = load_dataset("viarias/remote_sensing_2018_weedmap", subset="red_edge", split="train")
```

## `_info` method

Adding information about your dataset is useful for users to learn more about it. This information is stored in the **DatasetInfo** class which is returned by the ```_info``` method. Users can access this information by:

```python
from datasets import load_dataset_builder
ds_builder = load_dataset_builder("viarias/remote_sensing_2018_weedmap")
ds_builder.info
```

There is a lot of information you can specify about your dataset, but some important ones to include are:

1. **Description**: provides a concise description of the dataset.
2. **features** specify the dataset column types. 
3. **supervised_keys**: specify the input feature and label.
4. **homepage**: provides a link to the dataset homepage.
5. **citation**: is a BibTeX citation of the dataset.
6. **license**: states the dataset’s license.

All this information is included in the Weedmap dataset.

## `_split_generators` method

As you begin the loading script, the initial step involves handling the input data. This process includes working with a URL to access the file, downloading the raw dataset, and generating the necessary splits. To achieve this, you should be aware of the various methods in the `DownloadManager` class. 

```python
data_dir = dl_manager.download_and_extract(_URLS["RED_EDGE"])
files_path = dl_manager.iter_files(data_dir)
```

These methods allow you to accept:

* a name to a file inside a Hub dataset repository (in other words, the `data/` folder)
* a URL to a file hosted somewhere else
* a list or dictionary of file names or URLs

The last input type is similar to working with a local data folder. Once you have downloaded the dataset, you can use the `SplitGenerator` to organize the images and labels in each split. For the weed mapping dataset, we use the second option, which involves providing public URLs to both datasets.

## `_generate_examples` method

Finally, we use the `GeneratorBasedBuilder` to generate the images and labels in the dataset. It yields a dataset according to the structure specified in `features` from the `info` method.
