from typing import Mapping

from ..base._base_controller import ControllerBase, ComponentType
from .image_update_contract import ImageUpdateContract


class ImageController(ControllerBase):
    def __init__(
        self, editable_components: Mapping[ComponentType, ImageUpdateContract]
    ):
        super().__init__(editable_components=editable_components)

        # connect to image events
        for type, component in self.components_to_update.items():
            if hasattr(component, "events"):
                component.events.interpolation.connect(self.on_general_change)
