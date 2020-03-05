from enum import Enum
from typing import Mapping

from ..base import UpdateContractBase


class ComponentType(Enum):
    DATA = "DATA"
    RENDERING = "RENDERING"
    CONTROLS = "CONTROLS"


class ControllerBase:
    """
    Base layer controller class responsible for the interactions between the data layer,
    visual rendering, and gui controls
    """

    def __init__(
        self, editable_components: Mapping[ComponentType, UpdateContractBase]
    ):
        """
        Parameters
        ----------
        editable_components:
            List of components to update that all adhere to the UpdateContractBase
            ex.  [qt_image, vispy_image, image]
        """

        self.components_to_update = editable_components

    @property
    def rendering_component(self):
        if ComponentType.RENDERING in self.components_to_update:
            return self.components_to_update[ComponentType.RENDERING]
        return None

    @property
    def controls_component(self):
        if ComponentType.CONTROLS in self.components_to_update:
            return self.components_to_update[ComponentType.CONTROLS]
        return None

    @property
    def data_component(self):
        if ComponentType.DATA in self.components_to_update:
            return self.components_to_update[ComponentType.DATA]
        raise ValueError("No data")

    def on_general_change(self, event=None):
        """
        Process changes when attribute is changed from any interface
        """
        name = event.name
        value = event.value
        for type, component in self.components_to_update.items():
            update_method_name = f"_set_{name}"
            update_method = getattr(component, update_method_name)
            update_method(value)

    def rendering_change_only(self, event=None):
        """
        Process changes when attribute is changed and only the rendering component needs updating
        """
        name = event.name
        value = event.value
        update_method_name = f"_set_{name}"
        update_method = getattr(self.rendering_component, update_method_name)
        update_method(value)

    def controls_change_only(self, event=None):
        """
        Process changes when attribute is changed and only the controls component needs updating
        """
        name = event.name
        value = event.value
        update_method_name = f"_set_{name}"
        update_method = getattr(self.controls_component, update_method_name)
        update_method(value)

    def data_change_only(self, event=None):
        """
        Process changes when attribute is changed and only the data component needs updating
        """
        name = event.name
        value = event.value
        update_method_name = f"_set_{name}"
        update_method = getattr(self.data_component, update_method_name)
        update_method(value)

    def on_mouse_move(self, event):
        self.rendering_component.on_mouse_move(event)

        self.data_component.on_mouse_move(event)
