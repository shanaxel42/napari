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
                # general changes
                component.events.interpolation.connect(self.on_general_change)
                component.events.rendering.connect(self.on_general_change)
                component.events.iso_threshold.connect(self.on_general_change)
                component.events.attenuation.connect(self.on_general_change)

                if type == ComponentType.DATA:
                    # rendering changes
                    component.events.contrast_limits.connect(
                        self.rendering_change_only
                    )
                    component.events.colormap.connect(
                        self.rendering_change_only
                    )
                    component.events.gamma.connect(self.rendering_change_only)

                    # controls changes
                    component.dims.events.ndisplay.connect(
                        self.controls_change_only
                    )
