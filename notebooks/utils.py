import numpy as np
from typing import List
from tqdm import tqdm as tqdm

##############################################################################################
###### ---------------------------JOIN SEVERAL CHANNELS IN ONE--------------------------######
##############################################################################################

class LoadMultiSpectralDataset:
    def __init__(self, input_channels: List):
        """
        The objective of this class is load the weedmap dataset
        and return the huggingface dataset in the form -> 
        (multispectral_image, rgb_mask).

        Args:
            input_channels (List): The list of all image channels 
                                   that the user wants to ensemble
                                   on one image.
        """
        self._available_3_channels = [
            "RGB",
            "CIR"
        ]

        self._available_1_channel = [
            "R",
            "G",
            "B",
            "NIR",
            "RE",
            "NDVI",
        ]

        self.input_channels = input_channels

        _intersection1 = set(self._available_3_channels).intersection(set(self.input_channels))
        _intersection2 = set(self._available_1_channel).intersection(set(self.input_channels))
        
        assert len(list(_intersection1) + list(_intersection2)) == len(self.input_channels)

    def create_multispectral_feature(self, samples):
        """
        Create a multi-channel image array as a feature
        for a huggingface multispectral dataset.

        Args:
            sample: a sample with all the channels of the 
                    red_edge/sequoia agriculture dataset
        Returns
            A new feature called multispectral that contain
            the concatenation of multiple channels
        """
        multispectral_list = [0] * len(self.input_channels)


        for index, channel in enumerate(self.input_channels):
            if channel in self._available_3_channels:
                samples[channel] = [image.convert("RGB") for image in samples[channel]]
                multispectral_list[index] = np.array(samples[channel])
            elif channel in self._available_1_channel:
                multispectral_list[index] = np.expand_dims(np.array(samples[channel]), axis=-1)
            
        multispectral_array = np.concatenate(multispectral_list, axis=-1)
        samples['multispectral'] = multispectral_array
        
        return samples