from napari.layers.image.image_update_contract import ImageUpdateContract
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel, QComboBox, QSlider
from ...utils.event import Event
from .qt_image_base_layer import QtBaseImageControls
from ...layers.image._constants import Interpolation, Rendering


class QtImageControls(QtBaseImageControls, ImageUpdateContract):
    def __init__(self, layer):
        super().__init__(layer)

        self.events.add(
            interpolation=Event,
            rendering=Event,
            iso_threshold=Event,
            attenuation=Event,
        )

        interp_comboBox = QComboBox()
        interp_comboBox.addItems(Interpolation.keys())
        index = interp_comboBox.findText(
            self.layer.interpolation, Qt.MatchFixedString
        )
        interp_comboBox.setCurrentIndex(index)
        interp_comboBox.activated[str].connect(self.emit_interpolation_event)
        self.interpComboBox = interp_comboBox
        self.interpLabel = QLabel('interpolation:')

        renderComboBox = QComboBox()
        renderComboBox.addItems(Rendering.keys())
        index = renderComboBox.findText(
            self.layer.rendering, Qt.MatchFixedString
        )
        renderComboBox.setCurrentIndex(index)
        renderComboBox.activated[str].connect(self.emit_rendering_event)
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
        self._set_ndisplay()

        # grid_layout created in QtLayerControls
        # addWidget(widget, row, column, [row_span, column_span])
        self.grid_layout.addWidget(QLabel('opacity:'), 0, 0)
        self.grid_layout.addWidget(self.opacitySlider, 0, 1, 1, 2)
        self.grid_layout.addWidget(QLabel('contrast limits:'), 1, 0)
        self.grid_layout.addWidget(self.contrastLimitsSlider, 1, 1, 1, 2)
        self.grid_layout.addWidget(QLabel('gamma:'), 2, 0)
        self.grid_layout.addWidget(self.gammaSlider, 2, 1, 1, 2)
        self.grid_layout.addWidget(self.isoThresholdLabel, 3, 0)
        self.grid_layout.addWidget(self.isoThresholdSlider, 3, 1, 1, 2)
        self.grid_layout.addWidget(self.attenuationLabel, 3, 0)
        self.grid_layout.addWidget(self.attenuationSlider, 3, 1, 1, 2)
        self.grid_layout.addWidget(QLabel('colormap:'), 4, 0)
        self.grid_layout.addWidget(self.colormapComboBox, 4, 2)
        self.grid_layout.addWidget(self.colorbarLabel, 4, 1)
        self.grid_layout.addWidget(QLabel('blending:'), 5, 0)
        self.grid_layout.addWidget(self.blendComboBox, 5, 1, 1, 2)
        self.grid_layout.addWidget(self.renderLabel, 6, 0)
        self.grid_layout.addWidget(self.renderComboBox, 6, 1, 1, 2)
        self.grid_layout.addWidget(self.interpLabel, 7, 0)
        self.grid_layout.addWidget(self.interpComboBox, 7, 1, 1, 2)
        self.grid_layout.setRowStretch(8, 1)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setVerticalSpacing(4)

    def emit_interpolation_event(self, text):
        self.events.interpolation(name="interpolation", value=text)

    def emit_rendering_event(self, text):
        self.events.rendering(name="rendering", value=text)

    def emit_iso_threshold_event(self, value):
        value = value / 100
        self.events.iso_threshold(name="iso_threshold", value=value)

    def emit_attenuation_event(self, value):
        value = value / 100
        self.events.attenuation(name="attenuation", value=value)

    def _set_interpolation(self, text):
        index = self.interpComboBox.findText(text, Qt.MatchFixedString)
        self.interpComboBox.setCurrentIndex(index)

    def _set_rendering(self, text):
        index = self.renderComboBox.findText(text, Qt.MatchFixedString)
        self.renderComboBox.setCurrentIndex(index)
        self._toggle_rendering_parameter_visbility()

    def _set_iso_threshold(self, value):
        self.isoThresholdSlider.setValue(value * 100)

    def _set_attenuation(self, value):
        self.attenuationSlider.setValue(value * 100)

    def _toggle_rendering_parameter_visbility(self):
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

    def _set_ndisplay(self, value=None):
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
