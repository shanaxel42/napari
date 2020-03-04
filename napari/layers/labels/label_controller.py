from typing import List

from ..base._base_controller import ControllerBase
from .label_update_contract import LabelUpdateContract


class LabelController(ControllerBase):
    def __init__(self, editable_components: List[LabelUpdateContract]):
        super().__init__(editable_components=editable_components)

        # connect to image events
        for component in self.components_to_update:
            if hasattr(component, "events"):
                ...
