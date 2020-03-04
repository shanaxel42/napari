from .base import Layer
from ._base_update_contract import UpdateContractBase

from ..image import Image, ImageController
from ..labels import Labels, LabelController
from ..points import Points, PointsController
from ..shapes import Shapes, ShapesController
from ..surface import Surface, SurfaceController
from ..vectors import Vectors, VectorsController


layer_to_controller = {
    Image: ImageController,
    Labels: LabelController,
    Points: PointsController,
    Shapes: ShapesController,
    Surface: SurfaceController,
    Vectors: VectorsController,
}
