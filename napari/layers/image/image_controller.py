from typing import List

from ..base._base_controller import ControllerBase
from .image_update_contract import ImageUpdateContract


class ImageController(ControllerBase):
    def __init__(self, editable_components: List[ImageUpdateContract]):
        super().__init__(editable_components=editable_components)

        # connect to image events
        for component in self.components_to_update:
            if hasattr(component, "events"):
                component.events.interpolation.connect(self.on_change)
