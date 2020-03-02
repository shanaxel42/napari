from typing import List

from ..base import UpdateContractBase


class ControllerBase:
    """
    Base layer controller class responsible for the interactions between the data layer,
    visual rendering, and gui controls
    """

    def __init__(self, editable_components: List[UpdateContractBase]):
        """
        Parameters
        ----------
        editable_components:
            List of components to update that all adhere to the UpdateContractBase
            ex.  [qt_image, vispy_image, image]
        """

        self.components_to_update = editable_components

    def on_change(self, event=None):
        """
        Process changes when attribute is changed from any interface
        """
        name = event.name
        value = event.value
        for component in self.components_to_update:
            update_method_name = f"_set_{name}"
            update_method = getattr(component, update_method_name)
            update_method(value)
