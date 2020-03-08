from abc import abstractmethod

from napari.utils.base_interface import BaseInterface


class DimsInterface(BaseInterface):
    @abstractmethod
    def _on_axis_change(self, value):
        ...

    @abstractmethod
    def _on_axis_labels_change(self, value):
        ...

    @abstractmethod
    def _on_ndim_change(self, value):
        ...

    @abstractmethod
    def _on_ndisplay_change(self, value):
        ...

    @abstractmethod
    def _on_order_change(self, value):
        ...

    @abstractmethod
    def _on_range_change(self, value):
        ...

    @abstractmethod
    def _on_camera_change(self, value=None):
        ...
