from typing import List

from ..base._base_controller import ControllerBase
from .surface_update_contract import SurfaceUpdateContract


class SurfaceController(ControllerBase):
    def __init__(self, editable_components: List[SurfaceUpdateContract]):
        super().__init__(editable_components=editable_components)

        # connect to image events
        for component in self.components_to_update:
            if hasattr(component, "events"):
                ...
