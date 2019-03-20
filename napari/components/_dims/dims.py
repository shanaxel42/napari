import numpy
from copy import copy
from enum import Enum
from typing import Union, Tuple, Iterable, Sequence

from ...util.event import EmitterGroup


class DimsMode(Enum):
    Point = 0
    Interval = 1


class Dims():
    """Dimensions object modeling multi-dimensional slicing, cropping, and
    displaying in Napari

    Parameters
    ----------
    init_max_dims : int, optional
        Initial number of dimensions
    """
    def __init__(self, init_max_dims=0):

        super().__init__()

        # Events:
        self.changed = EmitterGroup(source=self,
                                    auto_connect=True,
                                    axis=None,
                                    nbdims=None)

        self.range = []
        self.point = []
        self.interval = []
        self.mode = []
        self.display = []

        self._ensure_axis_present(init_max_dims - 1)

    def __str__(self):
        return "~~".join([str(self.range),
                         str(self.point),
                         str(self.interval),
                         str(self.mode),
                         str(self.display)])

    @property
    def num_dimensions(self):
        """Returns the number of dimensions

        Returns
        -------
        num_dims : int
            Number of dimensions
        """
        return len(self.point)

    @num_dimensions.setter
    def num_dimensions(self, num_dimensions):
        if self.num_dimensions < num_dimensions:
            self._ensure_axis_present(num_dimensions - 1)
        elif self.num_dimensions > num_dimensions:
            self._trim_nb_dimensions(num_dimensions)

    def set_all_ranges(self, all_ranges: Sequence[Union[int, float]]):
        """Sets ranges for all dimensions

        Parameters
        ----------
        ranges : tuple
            Ranges of all dimensions
        """
        nb_dim = len(all_ranges)
        modified_dims = self._ensure_axis_present(nb_dim-1, no_event=True)
        self.range=all_ranges

        self.changed.nbdims()
        for axis_changed in modified_dims:
            self.changed.axis(axis=axis_changed)

    def set_range(self, axis: int, range: Sequence[Union[int, float]]):
        """Sets the range (min, max, step) for a given axis (dimension)

        Parameters
        ----------
        axis : int
            Dimension index
        range : tuple
            Range specified as (min, max, step)
        """
        self._ensure_axis_present(axis)
        if self.range[axis] != range:
            self.range[axis] = range
            self.changed.axis(axis=axis)

    def get_range(self, axis: int):
        """Returns the point at which this dimension is sliced

        Parameters
        ----------
        axis : int
            Dimension index

        Returns
        ----------
        range : tuple
            Range specified as (min, max, step)
        """
        return self.range[axis]

    def set_point(self, axis: int, value: Union[int, float]):
        """Sets the point at which to slice this dimension

        Parameters
        ----------
        axis : int
            Dimension index
        value : int or float
            Value of the point
        """
        self._ensure_axis_present(axis)
        if self.point[axis] != value:
            self.point[axis] = value
            self.changed.axis(axis=axis)

    def get_point(self, axis: int):
        """Returns the point at which this dimension is sliced

        Parameters
        ----------
        axis : int
            Dimension index

        Returns
        ----------
        value : int or float
            Value of the point
        """
        return self.point[axis]

    def set_interval(self, axis: int, interval: Sequence[Union[int, float]]):
        """Sets the interval used for cropping and projecting this dimension

        Parameters
        ----------
        axis : int
            Dimension index
        interval : tuple
            Interval specified with (min, max)
        """
        self._ensure_axis_present(axis)
        if self.interval[axis] != interval:
            self.interval[axis] = interval
            self.changed.axis(axis=axis)

    def get_interval(self, axis: int):
        """Returns interval for this dimension

        Parameters
        ----------
        axis : int
            Dimension index

        Returns
        ----------
        interval : tuple
            Interval specified with (min, max)
        """
        return self.interval[axis]

    def set_mode(self, axis: int, mode: DimsMode):
        """Sets the mode: Point or Interval

        Parameters
        ----------
        axis : int
            Dimension index
        mode : Point or Interval
            Whether dimension is in the Point or Interval mode
        """
        self._ensure_axis_present(axis)
        if self.mode[axis] != mode:
            self.mode[axis] = mode
            self.changed.axis(axis=axis)

    def get_mode(self, axis: int):
        """Returns the mode for a given axis

        Parameters
        ----------
        axis : int
            Dimension index

        Returns
        ----------
        mode : Point or Interval
            Whether dimension is in the Point or Interval mode
        """
        return self.mode[axis]

    def _set_2d_viewing(self):
        """Sets the 2d viewing
        """
        self.display = [False] * len(self.display)
        self.display[-1] = True
        self.display[-2] = True

    def set_display(self, axis: int, display: bool):
        """Sets the display boolean flag for a given axis

        Parameters
        ----------
        axis : int
            Dimension index
        display : bool
            Bool which is `True` for display and `False` for slice or project.
        """
        self._ensure_axis_present(axis)
        if self.display[axis] != display:
            self.display[axis] = display
            self.changed.axis(axis=axis)

    def get_display(self, axis: int):
        """Returns the display boolean flag for a given axis

        Parameters
        ----------
        axis : int
            Dimension index

        Returns
        ----------
        display : bool
            Bool which is `True` for display and `False` for slice or project.
        """
        return self.display[axis]

    @property
    def displayed_dimensions(self):
        """Returns the displayed dimensions

        Returns
        -------
        dimensions : np.ndarray
            Displayed dimensions
        """
        displayed_one_hot = copy(self.display)
        displayed_one_hot =  ([False if elem is None else elem for elem in
                              displayed_one_hot])
        return numpy.nonzero(list(displayed_one_hot))[0]

    def _ensure_axis_present(self, axis: int, no_event = None):
        """Makes sure that the given axis is in the dimension model

        Parameters
        ----------
        axis : int
            Dimension index

        Returns
        -------
        dimensions : list
            List of axes
        """
        if axis >= self.num_dimensions:
            old_nb_dimensions = self.num_dimensions
            margin_length = 1 + axis - self.num_dimensions
            self.range.extend([(None, None, None)] * (margin_length))
            self.point.extend([0.0] * (margin_length))
            self.interval.extend([None] * (margin_length))
            self.mode.extend([DimsMode.Interval] * (margin_length))
            self.display.extend([False] * (margin_length))

            if not no_event:
                # First we notify listeners that the number of dimensions have changed:
                self.changed.nbdims()

                # Then we notify listeners of which dimensions have been affected.
                for axis_changed in range(old_nb_dimensions - 1, self.num_dimensions):
                    self.changed.axis(axis=axis_changed)

            return list(range(old_nb_dimensions, 1 + axis))

        return []

    def _trim_nb_dimensions(self, nb_dimensions: int):
        """This internal method is used to trim the number of axis.

        Parameters
        ----------
        nb_dimensions : int
            The new number of dimensions
        """
        if nb_dimensions < self.num_dimensions:
            self.range = self.range[:nb_dimensions]
            self.point = self.point[:nb_dimensions]
            self.interval = self.interval[:nb_dimensions]
            self.mode = self.mode[:nb_dimensions]
            self.display = self.display[:nb_dimensions]

            # Notify listeners that the number of dimensions have changed:
            self.changed.nbdims()

    @property
    def slice_and_project(self):
        """Returns the slice and project tuples that specify how to slice and
        project arrays.

        Returns
        -------
        slice : tuple
            The slice tuple
        project : tuple
            The projection tuple
        """

        slice_list = []
        project_list = []

        for (mode, display, point, interval) in zip(self.mode, self.display, self.point, self.interval):

            if mode == DimsMode.Point or mode is None:
                if display:
                    # no slicing, cropping or projection:
                    project_list.append(False)
                    slice_point = round(point)
                    slice_point = 1 if slice_point==0 else slice_point
                    slice_list.append(slice(0,slice_point))
                else:
                    # slice:
                    project_list.append(False)
                    slice_list.append(round(point))
            elif mode == DimsMode.Interval:
                if display:
                    # crop for display:
                    project_list.append(False)
                    if interval is None:
                        slice_list.append(slice(None))
                    else:
                        slice_list.append(slice(round(interval[0]), round(interval[1])))
                else:
                    # crop before project:
                    project_list.append(True)
                    if interval is None:
                        slice_list.append(slice(None))
                    else:
                        slice_list.append(slice(round(interval[0]), round(interval[1])))

        slice_tuple = tuple(slice_list)
        project_tuple = tuple(project_list)

        return slice_tuple, project_tuple
