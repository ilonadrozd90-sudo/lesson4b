import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib.figure import Figure


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.month_list = []
        self.rainfall_list = []
    

        self.setWindowTitle("Data Viewer")
        self.filename = ""

        self.load_button = QPushButton("Load data")
        self.load_button.clicked.connect(self.load_data)

        self.filename_label = QLabel("No file selected")

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axes = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.filename_label)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.draw_graph()

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a data file",
            "",
            "All files (*);;CSV files (*.csv);;Text files (*.txt)",
        )
        if filename:
            self.month_list.clear()
            self.rainfall_list.clear()
            with open(filename, "r", encoding="utf-8") as f:
                next(f)
                for line in f:
                    parts = line.strip().split(",")
                    self.month_list.append(parts[0].strip())
                    self.rainfall_list.append(float(parts[1].strip()))

            self.filename = filename
            self.filename_label.setText(filename)
            self.draw_graph()

    def draw_graph(self):
        self.axes.clear()
        self.axes.set_title(
            "Monthly Rainfall" if not self.filename else f"Monthly Rainfall ({self.filename})",
            fontsize=14,
            fontweight="bold",
            pad=14,
        )
        self.axes.set_xlabel("Month", labelpad=8)
        self.axes.set_ylabel("Rainfall (mm)", labelpad=8)
        self.axes.set_axisbelow(True)
        self.axes.grid(axis="y", linestyle="--", alpha=0.35)
        self.axes.spines["top"].set_visible(False)
        self.axes.spines["right"].set_visible(False)

        if self.month_list:
            rainfall = [float(value) for value in self.rainfall_list]
            bars = self.axes.bar(
                self.month_list,
                rainfall,
                color="#4F86C6",
                edgecolor="#35618D",
                linewidth=0.7,
                width=0.72,
            )
            self.axes.bar_label(
                bars,
                labels=[f"{value:g}" for value in rainfall],
                padding=3,
                fontsize=8,
            )
            self.axes.set_ylim(0, max(rainfall) * 1.15 if max(rainfall) > 0 else 1)

        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec())