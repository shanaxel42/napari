from .base import Layer
from ._base_update_contract import UpdateContractBase

from ..image import Image
from ..image.image_controller import ImageController

layer_to_controller = {
    Image: ImageController,
}
