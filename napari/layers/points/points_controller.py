from typing import List

from ..base._base_controller import ControllerBase
from .points_update_contract import PointsUpdateContract


class PointsController(ControllerBase):
    def __init__(self, editable_components: List[PointsUpdateContract]):
        super().__init__(editable_components=editable_components)

        # connect to image events
        for component in self.components_to_update:
            if hasattr(component, "events"):
                ...
