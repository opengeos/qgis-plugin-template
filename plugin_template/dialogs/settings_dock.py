"""
Settings Dock Widget for Plugin Template

This module provides a settings panel that demonstrates
how to create configuration panels for QGIS plugins.
"""

from qgis.PyQt.QtCore import Qt, QSettings
from qgis.PyQt.QtWidgets import (
    QDockWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QGroupBox,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QFormLayout,
    QMessageBox,
    QFileDialog,
    QTabWidget,
)
from qgis.PyQt.QtGui import QFont


class SettingsDockWidget(QDockWidget):
    """A settings panel for configuring plugin options."""

    # Settings keys
    SETTINGS_PREFIX = "PluginTemplate/"

    def __init__(self, iface, parent=None):
        """Initialize the settings dock widget.

        Args:
            iface: QGIS interface instance.
            parent: Parent widget.
        """
        super().__init__("Settings", parent)
        self.iface = iface
        self.settings = QSettings()

        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        """Set up the settings UI."""
        # Main widget
        main_widget = QWidget()
        self.setWidget(main_widget)

        # Main layout
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)

        # Header
        header_label = QLabel("Plugin Settings")
        header_font = QFont()
        header_font.setPointSize(12)
        header_font.setBold(True)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)

        # Tab widget for organized settings
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # General settings tab
        general_tab = self._create_general_tab()
        tab_widget.addTab(general_tab, "General")

        # Advanced settings tab
        advanced_tab = self._create_advanced_tab()
        tab_widget.addTab(advanced_tab, "Advanced")

        # Paths settings tab
        paths_tab = self._create_paths_tab()
        tab_widget.addTab(paths_tab, "Paths")

        # Buttons
        button_layout = QHBoxLayout()

        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self._save_settings)
        button_layout.addWidget(self.save_btn)

        self.reset_btn = QPushButton("Reset Defaults")
        self.reset_btn.clicked.connect(self._reset_defaults)
        button_layout.addWidget(self.reset_btn)

        layout.addLayout(button_layout)

        # Stretch at the end
        layout.addStretch()

        # Status label
        self.status_label = QLabel("Settings loaded")
        self.status_label.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(self.status_label)

    def _create_general_tab(self):
        """Create the general settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # General options group
        general_group = QGroupBox("General Options")
        general_layout = QFormLayout(general_group)

        # Auto-load option
        self.auto_load_check = QCheckBox()
        self.auto_load_check.setChecked(True)
        general_layout.addRow("Auto-load on startup:", self.auto_load_check)

        # Show notifications
        self.notifications_check = QCheckBox()
        self.notifications_check.setChecked(True)
        general_layout.addRow("Show notifications:", self.notifications_check)

        # Default action
        self.default_action_combo = QComboBox()
        self.default_action_combo.addItems(["Action 1", "Action 2", "Action 3"])
        general_layout.addRow("Default action:", self.default_action_combo)

        # Language
        self.language_combo = QComboBox()
        self.language_combo.addItems(
            ["English", "Spanish", "French", "German", "Chinese"]
        )
        general_layout.addRow("Language:", self.language_combo)

        layout.addWidget(general_group)

        # Display group
        display_group = QGroupBox("Display Options")
        display_layout = QFormLayout(display_group)

        # Theme
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System"])
        display_layout.addRow("Theme:", self.theme_combo)

        # Font size
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(10)
        display_layout.addRow("Font size:", self.font_size_spin)

        layout.addWidget(display_group)

        layout.addStretch()
        return widget

    def _create_advanced_tab(self):
        """Create the advanced settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Processing group
        processing_group = QGroupBox("Processing")
        processing_layout = QFormLayout(processing_group)

        # Max threads
        self.max_threads_spin = QSpinBox()
        self.max_threads_spin.setRange(1, 32)
        self.max_threads_spin.setValue(4)
        processing_layout.addRow("Max threads:", self.max_threads_spin)

        # Chunk size
        self.chunk_size_spin = QSpinBox()
        self.chunk_size_spin.setRange(256, 4096)
        self.chunk_size_spin.setValue(512)
        self.chunk_size_spin.setSingleStep(256)
        processing_layout.addRow("Chunk size:", self.chunk_size_spin)

        # Memory limit
        self.memory_limit_spin = QSpinBox()
        self.memory_limit_spin.setRange(256, 16384)
        self.memory_limit_spin.setValue(4096)
        self.memory_limit_spin.setSuffix(" MB")
        processing_layout.addRow("Memory limit:", self.memory_limit_spin)

        # Tolerance
        self.tolerance_spin = QDoubleSpinBox()
        self.tolerance_spin.setRange(0.0, 10.0)
        self.tolerance_spin.setValue(0.5)
        self.tolerance_spin.setSingleStep(0.1)
        self.tolerance_spin.setDecimals(2)
        processing_layout.addRow("Tolerance:", self.tolerance_spin)

        layout.addWidget(processing_group)

        # Debug group
        debug_group = QGroupBox("Debug")
        debug_layout = QFormLayout(debug_group)

        # Debug mode
        self.debug_check = QCheckBox()
        self.debug_check.setChecked(False)
        debug_layout.addRow("Debug mode:", self.debug_check)

        # Log level
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["Error", "Warning", "Info", "Debug"])
        self.log_level_combo.setCurrentIndex(2)  # Info
        debug_layout.addRow("Log level:", self.log_level_combo)

        layout.addWidget(debug_group)

        layout.addStretch()
        return widget

    def _create_paths_tab(self):
        """Create the paths settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Paths group
        paths_group = QGroupBox("File Paths")
        paths_layout = QFormLayout(paths_group)

        # Output directory
        output_layout = QHBoxLayout()
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setPlaceholderText("Default output directory...")
        output_layout.addWidget(self.output_dir_input)
        self.output_dir_btn = QPushButton("...")
        self.output_dir_btn.setMaximumWidth(30)
        self.output_dir_btn.clicked.connect(
            lambda: self._browse_directory(self.output_dir_input)
        )
        output_layout.addWidget(self.output_dir_btn)
        paths_layout.addRow("Output directory:", output_layout)

        # Temp directory
        temp_layout = QHBoxLayout()
        self.temp_dir_input = QLineEdit()
        self.temp_dir_input.setPlaceholderText("Temporary files directory...")
        temp_layout.addWidget(self.temp_dir_input)
        self.temp_dir_btn = QPushButton("...")
        self.temp_dir_btn.setMaximumWidth(30)
        self.temp_dir_btn.clicked.connect(
            lambda: self._browse_directory(self.temp_dir_input)
        )
        temp_layout.addWidget(self.temp_dir_btn)
        paths_layout.addRow("Temp directory:", temp_layout)

        # Models directory
        models_layout = QHBoxLayout()
        self.models_dir_input = QLineEdit()
        self.models_dir_input.setPlaceholderText("Models directory...")
        models_layout.addWidget(self.models_dir_input)
        self.models_dir_btn = QPushButton("...")
        self.models_dir_btn.setMaximumWidth(30)
        self.models_dir_btn.clicked.connect(
            lambda: self._browse_directory(self.models_dir_input)
        )
        models_layout.addWidget(self.models_dir_btn)
        paths_layout.addRow("Models directory:", models_layout)

        layout.addWidget(paths_group)

        layout.addStretch()
        return widget

    def _browse_directory(self, line_edit):
        """Open directory browser dialog."""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Directory", line_edit.text() or ""
        )
        if dir_path:
            line_edit.setText(dir_path)

    def _load_settings(self):
        """Load settings from QSettings."""
        # General
        self.auto_load_check.setChecked(
            self.settings.value(f"{self.SETTINGS_PREFIX}auto_load", True, type=bool)
        )
        self.notifications_check.setChecked(
            self.settings.value(f"{self.SETTINGS_PREFIX}notifications", True, type=bool)
        )
        self.default_action_combo.setCurrentIndex(
            self.settings.value(f"{self.SETTINGS_PREFIX}default_action", 0, type=int)
        )
        self.language_combo.setCurrentIndex(
            self.settings.value(f"{self.SETTINGS_PREFIX}language", 0, type=int)
        )

        # Display
        self.theme_combo.setCurrentIndex(
            self.settings.value(f"{self.SETTINGS_PREFIX}theme", 0, type=int)
        )
        self.font_size_spin.setValue(
            self.settings.value(f"{self.SETTINGS_PREFIX}font_size", 10, type=int)
        )

        # Advanced
        self.max_threads_spin.setValue(
            self.settings.value(f"{self.SETTINGS_PREFIX}max_threads", 4, type=int)
        )
        self.chunk_size_spin.setValue(
            self.settings.value(f"{self.SETTINGS_PREFIX}chunk_size", 512, type=int)
        )
        self.memory_limit_spin.setValue(
            self.settings.value(f"{self.SETTINGS_PREFIX}memory_limit", 4096, type=int)
        )
        self.tolerance_spin.setValue(
            self.settings.value(f"{self.SETTINGS_PREFIX}tolerance", 0.5, type=float)
        )
        self.debug_check.setChecked(
            self.settings.value(f"{self.SETTINGS_PREFIX}debug", False, type=bool)
        )
        self.log_level_combo.setCurrentIndex(
            self.settings.value(f"{self.SETTINGS_PREFIX}log_level", 2, type=int)
        )

        # Paths
        self.output_dir_input.setText(
            self.settings.value(f"{self.SETTINGS_PREFIX}output_dir", "", type=str)
        )
        self.temp_dir_input.setText(
            self.settings.value(f"{self.SETTINGS_PREFIX}temp_dir", "", type=str)
        )
        self.models_dir_input.setText(
            self.settings.value(f"{self.SETTINGS_PREFIX}models_dir", "", type=str)
        )

        self.status_label.setText("Settings loaded")
        self.status_label.setStyleSheet("color: gray; font-size: 10px;")

    def _save_settings(self):
        """Save settings to QSettings."""
        # General
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}auto_load", self.auto_load_check.isChecked()
        )
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}notifications", self.notifications_check.isChecked()
        )
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}default_action",
            self.default_action_combo.currentIndex(),
        )
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}language", self.language_combo.currentIndex()
        )

        # Display
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}theme", self.theme_combo.currentIndex()
        )
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}font_size", self.font_size_spin.value()
        )

        # Advanced
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}max_threads", self.max_threads_spin.value()
        )
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}chunk_size", self.chunk_size_spin.value()
        )
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}memory_limit", self.memory_limit_spin.value()
        )
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}tolerance", self.tolerance_spin.value()
        )
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}debug", self.debug_check.isChecked()
        )
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}log_level", self.log_level_combo.currentIndex()
        )

        # Paths
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}output_dir", self.output_dir_input.text()
        )
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}temp_dir", self.temp_dir_input.text()
        )
        self.settings.setValue(
            f"{self.SETTINGS_PREFIX}models_dir", self.models_dir_input.text()
        )

        self.settings.sync()

        self.status_label.setText("Settings saved")
        self.status_label.setStyleSheet("color: green; font-size: 10px;")

        self.iface.messageBar().pushSuccess(
            "Plugin Template", "Settings saved successfully!"
        )

    def _reset_defaults(self):
        """Reset all settings to defaults."""
        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        # General
        self.auto_load_check.setChecked(True)
        self.notifications_check.setChecked(True)
        self.default_action_combo.setCurrentIndex(0)
        self.language_combo.setCurrentIndex(0)

        # Display
        self.theme_combo.setCurrentIndex(0)
        self.font_size_spin.setValue(10)

        # Advanced
        self.max_threads_spin.setValue(4)
        self.chunk_size_spin.setValue(512)
        self.memory_limit_spin.setValue(4096)
        self.tolerance_spin.setValue(0.5)
        self.debug_check.setChecked(False)
        self.log_level_combo.setCurrentIndex(2)

        # Paths
        self.output_dir_input.clear()
        self.temp_dir_input.clear()
        self.models_dir_input.clear()

        self.status_label.setText("Defaults restored (not saved)")
        self.status_label.setStyleSheet("color: orange; font-size: 10px;")
