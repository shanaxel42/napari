from typing import List

from ..base._base_controller import ControllerBase
from .vectors_update_contract import VectorsUpdateContract


class VectorsController(ControllerBase):
    def __init__(self, editable_components: List[VectorsUpdateContract]):
        super().__init__(editable_components=editable_components)

        # connect to image events
        for component in self.components_to_update:
            if hasattr(component, "events"):
                ...
