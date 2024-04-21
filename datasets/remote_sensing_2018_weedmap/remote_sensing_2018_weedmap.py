import json
import os
from collections import OrderedDict, defaultdict
from math import ceil
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

import datasets

logger = datasets.logging.get_logger(__name__)

_LICENSE = "GPL-3.0 license"

_CITATION = """\
@article{weedMap-2018,
    author={I. Sa, M. Popovic, R. Khanna, Z. Chen, P. Lottes, F. Liebisch, J. Nieto, C. Stachniss, A. Walter, and R. Siegwart}, 
    journal={MDPI Remote Sensing},
    title={WeedMap: A large-scale semantic weed mapping framework using aerial multispectral imaging and deep neural network for precision farming}, 
    year={2018},
    volume={10},
    number={9}, 
    doi={doi: 10.3390/rs10091423},
    month={Aug}}
}
"""

_HOMEPAGE = "https://projects.asl.ethz.ch/datasets/doku.php?id=weedmap:remotesensing2018weedmap"

_DESCRIPTION = """\
The WeedMap dataset is a comprehensive collection of multispectral images captured from sugar beet fields in Eschikon, Switzerland, and Rheinbach, Germany, using quadrotor UAVs equipped with RedEdge-M and Sequoia multispectral cameras. 
Spanning over five months, it comprises 129 directories with 18,746 image files. The dataset is divided into Orthomosaic and Tiles folders, featuring orthomosaic maps and their segmented tiles, respectively. 
Ground truth annotations are provided, detailing classifications such as background, crop, and weed in both color and indexed formats. This dataset, the largest publicly available for sugar beet fields with pixel-level ground truth, spans a total area of 16,554 square meters. 
It offers a detailed representation of the agricultural landscape, including a ground sample distance of about 1cm, facilitating high precision in weed detection research. This rich dataset supports the development of advanced deep learning models for semantic segmentation in precision agriculture, enhancing weed management practices​​​​.
"""

_URLS = {
    "RED_EDGE": "http://robotics.ethz.ch/~asl-datasets/2018-weedMap-dataset-release/Tiles/RedEdge.zip",
    "SEQUOIA": "http://robotics.ethz.ch/~asl-datasets/2018-weedMap-dataset-release/Tiles/Sequoia.zip",
}

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


class WeedMapConfig(datasets.BuilderConfig):
    """BuilderConfig for WeedMap."""

    def __init__(self, data_url, **kwargs):
        """BuilderConfig for WeedMap.

        Args:
            data_url: `string`, url to download the zip file from.
            **kwargs: keyword arguments forwarded to super.
        """
        super(WeedMapConfig, self).__init__(version=datasets.Version("1.0.0"), **kwargs)
        self.data_url = data_url

class WeedMap(datasets.GeneratorBasedBuilder):
    """Remote Sensing 2018 Weed Map Dataset."""

    BUILDER_CONFIGS = [
        WeedMapConfig(
            name="red_edge",
            description="weedmap dataset with the subset generated by the Red Edge sensor",
            data_url=_URLS["RED_EDGE"],)
        ,
        WeedMapConfig(
            name="sequoia",
            description="weedmap dataset with the subset generated by the Sequoia sensor",
            data_url=_URLS["SEQUOIA"],)
    ]

    DEFAULT_CONFIG_NAME = "red_edge"

    def _info(self):
        if self.config.name == "red_edge":
            features = datasets.Features(
                {
                    "B": datasets.Image(),
                    "CIR": datasets.Image(),
                    "G": datasets.Image(),
                    "NDVI": datasets.Image(),
                    "NIR": datasets.Image(),
                    "R": datasets.Image(),
                    "RE": datasets.Image(),
                    "RGB": datasets.Image(),
                    "annotation": datasets.Image(),
                }
            )
        elif self.config.name == "sequoia":
            features = datasets.Features(
                {
                    "CIR": datasets.Image(),
                    "G": datasets.Image(),
                    "NDVI": datasets.Image(),
                    "NIR": datasets.Image(),
                    "R": datasets.Image(),
                    "RE": datasets.Image(),
                    "annotation": datasets.Image(),
                }
            )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # use the datasets.DownloadManager().download_and_extract() method to download the data
        # in testing time, the data will be downloaded in the default cache directory, which is
        # ~/.cache/huggingface/datasets

        def images_and_masks(images_dict, masks):
            for image_dict, mask in zip(images_dict, masks):
                yield image_dict, mask

        if self.config.name == "red_edge":
            data_dir = dl_manager.download_and_extract(_URLS["RED_EDGE"])
            files_path = dl_manager.iter_files(data_dir)
            train_image_files, train_mask_files = create_list_paths(files_path, subset="red_edge", split_section="train")
            test_image_files, test_mask_files = create_list_paths(files_path, subset="red_edge", split_section="test")


        elif self.config.name == "sequoia":
            data_dir = dl_manager.download_and_extract(_URLS["SEQUOIA"])
            files_path = dl_manager.iter_files(data_dir)
            train_image_files, train_mask_files = create_list_paths(files_path, subset="sequoia", split_section="train")
            test_image_files, test_mask_files = create_list_paths(files_path, subset="sequoia", split_section="test")

        return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "data": images_and_masks(train_image_files, train_mask_files),
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "data": images_and_masks(test_image_files, test_mask_files),
                    },
                ),
            ]     

    def _generate_examples(self, data):

        """Yields examples."""
        if self.config.name == "red_edge":
            for idx, (img_path, msk_path) in enumerate(data):
                print("")
                print("")
                print("")
                print(img_path["B"])
                print("")
                print("")
                print("")
                yield idx, {
                    "B": img_path["B"],
                    "CIR": img_path["CIR"],
                    "G": img_path["G"],
                    "NDVI": img_path["NDVI"],
                    "NIR": img_path["NIR"],
                    "R": img_path["R"],
                    "RE": img_path["RE"],
                    "RGB": img_path["RGB"],
                    "annotation": msk_path,
                }

        elif self.config.name == "sequoia":
            for idx, (img_path, msk_path) in enumerate(data):
                yield idx, {
                    "CIR": img_path["CIR"],
                    "G": img_path["G"],
                    "NDVI": img_path["NDVI"],
                    "NIR": img_path["NIR"],
                    "R": img_path["R"],
                    "RE": img_path["RE"],
                    "annotation": msk_path,
                }
            
def create_list_paths(total_files_path, subset="red_edge", split_section="train"):
    """
    Create a list of paths for the images and masks.

    Args:
        total_files_path (list): A list of file paths.
        subset (str, optional): The subset to filter the files. Defaults to "red_edge".
        split_section (str, optional): The split section to filter the files. Defaults to "train".

    Returns:
        tuple or list: If split_section is "train", returns a tuple containing train_image_files, train_mask_files,
                        val_image_files, val_mask_files. Otherwise, returns a list containing split_image_files and
                        split_mask_files.
    """
    if subset == "red_edge":
        subset_dict = REDEDGE_SPLIT

    elif subset == "sequoia":
        subset_dict = SEQUOIA_SPLIT

    # multi filter
    split_files_path = [
        file_path for file_path in total_files_path
        if (
            (not ".DS_Store" in file_path) and  # don't take account trash files
            ("GroundTruth_color.png" in file_path or  # if the image is a color mask, save the path
            file_path.split("/")[-4] in subset_dict[split_section]  # if the image is in the correct split folder, save the path
            )
        )
                        ]

    split_mask_files = []
    split_image_files = dict()

    # separate every tile by channel name
    for file in split_files_path:
        if "tile" in file:
            image_channel_name = file.split("/")[-2]
            split_image_files.setdefault(image_channel_name, [])
            split_image_files[image_channel_name].append(file)
        else:
            split_mask_files.append(file)

    # sorted the image and mask files by name
    for key, image_paths_channel in split_image_files.items():
        split_image_files[key] = sorted(image_paths_channel, key=lambda path_file: (str(path_file).split("/")[-4], str(path_file).split("/")[-1]))
    split_mask_files = sorted(split_mask_files, key=lambda path_file: (str(path_file).split("/")[-4], str(path_file).split("/")[-1]))

    split_image_files_ld = [dict(zip(split_image_files, t)) for t in zip(*split_image_files.values())]

    return split_image_files_ld, split_mask_files