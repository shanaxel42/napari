from abc import abstractmethod
from ..base._base_update_contract import UpdateContractBase


class ImageUpdateContract(UpdateContractBase):
    """
    Defines the getters/setters editable across components for an ImageLayer
    """

    @abstractmethod
    def _set_interpolation(self, value):
        ...
