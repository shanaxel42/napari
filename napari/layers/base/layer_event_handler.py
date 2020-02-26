from ...utils.event_handler import EventHandler
from napari.utils.base_interface import BaseInterface


class LayerEventHandler(EventHandler):
    def __init__(self, component: BaseInterface = None):
        super().__init__(component)

    def on_change(self, event=None):
        """
        Process changes made from any interface
        """
        name = event.type
        value = event.value
        print(f"event: {name}")
        for component in self.components_to_update:
            update_method_name = f"_on_{name}_change"
            update_method = getattr(component, update_method_name)
            update_method(value)
