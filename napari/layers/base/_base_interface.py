from abc import abstractmethod

from napari.utils.base_interface import BaseInterface


class BaseLayerInterface(BaseInterface):
    """
    Base class for UpdateContract. Defines a set of methods shared between the data layer visual
    rendering and controls.
    """

    @abstractmethod
    def _on_refresh_change(self):
        ...

    @abstractmethod
    def _on_set_data_change(self, value):
        ...

    @abstractmethod
    def _on_blending_change(self, value):
        ...

    @abstractmethod
    def _on_opacity_change(self, value):
        ...

    @abstractmethod
    def _on_visible_change(self, value):
        ...

    @abstractmethod
    def _on_select_change(self, value):
        ...

    @abstractmethod
    def _on_deselect_change(self, value):
        ...

    @abstractmethod
    def _on_scale_change(self, value):
        ...

    @abstractmethod
    def _on_translate_change(self, value):
        ...

    @abstractmethod
    def _on_data_change(self, value):
        ...

    @abstractmethod
    def _on_name_change(self, value):
        ...

    @abstractmethod
    def _on_thumbnail_change(self, value):
        ...

    @abstractmethod
    def _on_status_change(self, value):
        ...

    @abstractmethod
    def _on_help_change(self, value):
        ...

    @abstractmethod
    def _on_interactive_change(self, value):
        ...

    @abstractmethod
    def _on_cursor_change(self, value):
        ...

    @abstractmethod
    def _on_cursor_size_change(self, value):
        ...

    @abstractmethod
    def _on_editable_change(self, value):
        ...

    @abstractmethod
    def _on_update_dims(self):
        ...

    # TODO reformat these

    @abstractmethod
    def on_mouse_move(self):
        ...

    @abstractmethod
    def on_mouse_press(self):
        ...

    @abstractmethod
    def on_mouse_release(self):
        ...
