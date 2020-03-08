from napari.layers.image.image_interface import ImageInterface
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel, QComboBox, QSlider, QHBoxLayout
from .qt_image_base_layer import QtBaseImageControls
from ...layers.image._constants import Interpolation, Rendering


class QtImageControls(QtBaseImageControls, ImageInterface):
    """Qt view and controls for the napari Image layer.

   Parameters
   ----------
   layer : napari.layers.Image
       An instance of a napari Image layer.

   Attributes
   ----------
   attenuationSlider : qtpy.QtWidgets.QSlider
       Slider controlling attenuation rate for `attenuated_mip` mode.
   attenuationLabel : qtpy.QtWidgets.QLabel
       Label for the attenuation slider widget.
   grid_layout : qtpy.QtWidgets.QGridLayout
       Layout of Qt widget controls for the layer.
   interpComboBox : qtpy.QtWidgets.QComboBox
       Dropdown menu to select the interpolation mode for image display.
   interpLabel : qtpy.QtWidgets.QLabel
       Label for the interpolation dropdown menu.
   isoThresholdSlider : qtpy.QtWidgets.QSlider
       Slider controlling the isosurface threshold value for rendering.
   isoThresholdLabel : qtpy.QtWidgets.QLabel
       Label for the isosurface threshold slider widget.
   layer : napari.layers.Image
       An instance of a napari Image layer.
   renderComboBox : qtpy.QtWidgets.QComboBox
       Dropdown menu to select the rendering mode for image display.
   renderLabel : qtpy.QtWidgets.QLabel
       Label for the rendering mode dropdown menu.
   """

    def __init__(self, layer):
        super().__init__(layer)

        self.layer.events.register_component_to_update(self)

        interp_comboBox = QComboBox()
        interp_comboBox.addItems(Interpolation.keys())
        index = interp_comboBox.findText(
            self.layer.interpolation, Qt.MatchFixedString
        )
        interp_comboBox.setCurrentIndex(index)
        interp_comboBox.activated[str].connect(self.events.interpolation)
        self.interpComboBox = interp_comboBox
        self.interpLabel = QLabel('interpolation:')

        renderComboBox = QComboBox()
        renderComboBox.addItems(Rendering.keys())
        index = renderComboBox.findText(
            self.layer.rendering, Qt.MatchFixedString
        )
        renderComboBox.setCurrentIndex(index)
        renderComboBox.activated[str].connect(self.events.rendering)
        self.renderComboBox = renderComboBox
        self.renderLabel = QLabel('rendering:')

        sld = QSlider(Qt.Horizontal)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setMinimum(0)
        sld.setMaximum(100)
        sld.setSingleStep(1)
        sld.setValue(self.layer.iso_threshold * 100)
        sld.valueChanged.connect(self.emit_iso_threshold_event)
        self.isoThresholdSlider = sld
        self.isoThresholdLabel = QLabel('iso threshold:')

        sld = QSlider(Qt.Horizontal)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setMinimum(0)
        sld.setMaximum(200)
        sld.setSingleStep(1)
        sld.setValue(self.layer.attenuation * 100)
        sld.valueChanged.connect(self.emit_attenuation_event)
        self.attenuationSlider = sld
        self.attenuationLabel = QLabel('attenuation:')
        self._on_ndisplay_change()

        colormap_layout = QHBoxLayout()
        colormap_layout.addWidget(self.colorbarLabel)
        colormap_layout.addWidget(self.colormapComboBox)
        colormap_layout.addStretch(1)

        # grid_layout created in QtLayerControls
        # addWidget(widget, row, column, [row_span, column_span])
        self.grid_layout.addWidget(QLabel('opacity:'), 0, 0)
        self.grid_layout.addWidget(self.opacitySlider, 0, 1)
        self.grid_layout.addWidget(QLabel('contrast limits:'), 1, 0)
        self.grid_layout.addWidget(self.contrastLimitsSlider, 1, 1)
        self.grid_layout.addWidget(QLabel('gamma:'), 2, 0)
        self.grid_layout.addWidget(self.gammaSlider, 2, 1)
        self.grid_layout.addWidget(QLabel('colormap:'), 3, 0)
        self.grid_layout.addLayout(colormap_layout, 3, 1)
        self.grid_layout.addWidget(QLabel('blending:'), 4, 0)
        self.grid_layout.addWidget(self.blendComboBox, 4, 1)
        self.grid_layout.addWidget(self.renderLabel, 5, 0)
        self.grid_layout.addWidget(self.renderComboBox, 5, 1)
        self.grid_layout.addWidget(self.interpLabel, 6, 0)
        self.grid_layout.addWidget(self.interpComboBox, 6, 1)
        self.grid_layout.addWidget(self.isoThresholdLabel, 7, 0)
        self.grid_layout.addWidget(self.isoThresholdSlider, 7, 1)
        self.grid_layout.addWidget(self.attenuationLabel, 8, 0)
        self.grid_layout.addWidget(self.attenuationSlider, 8, 1)
        self.grid_layout.setRowStretch(9, 1)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setSpacing(4)

    def _on_interpolation_change(self, text):
        """Change interpolation mode for image display.

       Parameters
       ----------
       text : str
           Interpolation mode used by vispy. Must be one of our supported
           modes:
           'bessel', 'bicubic', 'bilinear', 'blackman', 'catrom', 'gaussian',
           'hamming', 'hanning', 'hermite', 'kaiser', 'lanczos', 'mitchell',
           'nearest', 'spline16', 'spline36'
       """
        index = self.interpComboBox.findText(text, Qt.MatchFixedString)
        self.interpComboBox.setCurrentIndex(index)

    def emit_iso_threshold_event(self, value):
        """Change isosurface threshold on the layer model.

        Parameters
        ----------
        value : float
            Threshold for isosurface.
        """
        self.events.iso_threshold(value=value / 100)

    def _on_iso_threshold_change(self, value):
        """Receive layer model isosurface change event and update the slider.

        Parameters
        ----------
        event : qtpy.QtCore.QEvent
            Event from the Qt context.
        """
        self.isoThresholdSlider.setValue(value * 100)

    def emit_attenuation_event(self, value):
        """Change attenuation rate for attenuated maximum intensity projection.

        Parameters
        ----------
        value : Float
            Attenuation rate for attenuated maximum intensity projection.
        """
        self.events.attenuation(value=value / 100)

    def _on_attenuation_change(self, value):
        """Receive layer model attenuation change event and update the slider.

        Parameters
        ----------
        event : qtpy.QtCore.QEvent
            Event from the Qt context.
        """
        self.attenuationSlider.setValue(value * 100)

    def _on_rendering_change(self, value):
        """Receive layer model rendering change event and update dropdown menu.

        Parameters
        ----------
        event : qtpy.QtCore.QEvent
            Event from the Qt context.
        """
        index = self.renderComboBox.findText(value, Qt.MatchFixedString)
        self.renderComboBox.setCurrentIndex(index)
        self._toggle_rendering_parameter_visbility()

    def _toggle_rendering_parameter_visbility(self):
        """Hide isosurface rendering parameters if they aren't needed."""
        rendering = self.layer.rendering
        if isinstance(rendering, str):
            rendering = Rendering(rendering)
        if rendering == Rendering.ISO:
            self.isoThresholdSlider.show()
            self.isoThresholdLabel.show()
        else:
            self.isoThresholdSlider.hide()
            self.isoThresholdLabel.hide()
        if rendering == Rendering.ATTENUATED_MIP:
            self.attenuationSlider.show()
            self.attenuationLabel.show()
        else:
            self.attenuationSlider.hide()
            self.attenuationLabel.hide()

    def _on_ndisplay_change(self, event=None):
        """Toggle between 2D and 3D visualization modes.

        Parameters
        ----------
        event : qtpy.QtCore.QEvent, optional
            Event from the Qt context, default is None.
        """
        if self.layer.dims.ndisplay == 2:
            self.isoThresholdSlider.hide()
            self.isoThresholdLabel.hide()
            self.attenuationSlider.hide()
            self.attenuationLabel.hide()
            self.renderComboBox.hide()
            self.renderLabel.hide()
            self.interpComboBox.show()
            self.interpLabel.show()
        else:
            self.renderComboBox.show()
            self.renderLabel.show()
            self.interpComboBox.hide()
            self.interpLabel.hide()
            self._toggle_rendering_parameter_visbility()
