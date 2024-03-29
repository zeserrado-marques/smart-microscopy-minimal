"""
This module is an example of a barebones function plugin for napari

It implements the ``napari_experimental_provide_function`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from enum import Enum
import numpy as np
from napari_plugin_engine import napari_hook_implementation
from skimage.filters import gaussian

if TYPE_CHECKING:
    import napari


# This is the actual plugin function, where we export our function
# (The functions themselves are defined below)
@napari_hook_implementation
def napari_experimental_provide_function():
    # we can return a single function
    # or a tuple of (function, magicgui_options)
    # or a list of multiple functions with or without options, as shown here:
    return [threshold, image_arithmetic, DoG_filter_ze, DoG_filter]


# 1.  First example, a simple function that thresholds an image and creates a labels layer
def threshold(data: "napari.types.ImageData", threshold: int) -> "napari.types.LabelsData":
    """Threshold an image and return a mask."""
    return (data > threshold).astype(int)

def DoG_filter_ze(im_data: "napari.types.ImageData", sigma: float = 2) -> "napari.types.ImageData":

    sig1 = sigma
    sig2 = 5 * sig1

    blurred = gaussian(im_data, sig1)
    mega_blurred = gaussian(im_data, sig2)

    dog = blurred - mega_blurred

    return dog

def DoG_filter(im_data: "napari.types.ImageData", sigma: float = 2) -> "napari.types.ImageData":
    """
        Simple DoG filtering bi givin just one sigma
    """
    sig1 = sigma
    sig2 = 1.414 * sig1

    image_g_sig1 = gaussian(im_data, sigma=sig1)
    image_g_sig2 = gaussian(im_data, sigma=sig2)

    DoG = image_g_sig1 - image_g_sig2

    return DoG

# 2. Second example, a function that adds, subtracts, multiplies, or divides two layers

# using Enums is a good way to get a dropdown menu.  Used here to select from np functions
class Operation(Enum):
    add = np.add
    subtract = np.subtract
    multiply = np.multiply
    divide = np.divide


def image_arithmetic(
    layerA: "napari.types.ImageData", operation: Operation, layerB: "napari.types.ImageData"
) -> "napari.types.LayerDataTuple":
    """Adds, subtracts, multiplies, or divides two same-shaped image layers."""
    return (operation.value(layerA, layerB), {"colormap": "turbo"})
