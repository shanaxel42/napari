from typing import List, Optional

from ._base_interface import BaseInterface


class EventHandlerBase:
    """
    Base layer controller class responsible for the interactions between the data layer,
    visual rendering, and gui controls
    """

    def __init__(self, component: Optional[BaseInterface]):
        self.components_to_update: List[BaseInterface] = []
        self.register(component)

    def register(self, component):
        self.components_to_update.append(component)
        if hasattr(component, "events"):
            for name in component.events:
                if (
                    name == "interpolation"
                    or name == "contrast_limits"
                    or name == "rendering"
                    or name == "iso_threshold"
                    or name == "attenuation"
                    or name == "gamma"
                    or name == "colormap"
                ):
                    event = getattr(component.events, name)
                    event.connect(self.on_change)

    def on_change(self, event=None):
        """
        Process changes when attribute is changed from any interface
        """
        name = event.type
        value = event.value
        for component in self.components_to_update:
            update_method_name = f"_set_{name}"
            update_method = getattr(component, update_method_name)
            update_method(value)
