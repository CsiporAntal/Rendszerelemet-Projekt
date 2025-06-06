import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtGui import QAction, QPalette, QColor
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QSplitter, QTextEdit, QSlider, QMenuBar,
    QMenu, QStyleFactory, QMessageBox
)
from PyQt6.QtCore import Qt
import control as ctrl
from scipy.signal import TransferFunction, impulse


class TransferFunctionGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Átviteli Függvény Elemző')
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.init_menu()
        self.initUI()

    def init_menu(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Menük létrehozása
        actions_menu = QMenu("Actions", self)
        settings_menu = QMenu("Settings", self)
        help_menu = QMenu("Help", self)

        # Actions menüpont – export funkció
        export_action = QAction("Export", self)
        export_action.triggered.connect(self.export_data)
        actions_menu.addAction(export_action)

        # Settings menüpont – témaválasztás
        theme_follow = QAction("Follow system", self)
        theme_follow.triggered.connect(self.apply_no_theme)

        theme_white = QAction("White", self)
        theme_white.triggered.connect(self.apply_white_theme)

        settings_menu.addAction(theme_follow)
        settings_menu.addAction(theme_white)

        # Help menüpont – info megjelenítés
        help_action = QAction("About", self)
        help_action.triggered.connect(self.show_help_dialog)
        help_menu.addAction(help_action)

        # Menüsor hozzáadása megfelelő sorrendben
        menu_bar.addMenu(actions_menu)
        menu_bar.addMenu(settings_menu)
        menu_bar.addMenu(help_menu)

    def show_help_dialog(self):
        QMessageBox.information(
            self,
            "Névjegy / Súgó",
            "Átviteli függvény elemző\n\n"
            "Írj be egy számlálót és nevezőt, például:\n"
            "Számláló: 1\n"
            "Nevező: 1, 2, 2\n\n"
            "Az alkalmazás megmutatja a rendszer pólusait, "
            "impulzusválaszát és a |H(s)| 3D felületét."
        )

    def export_data(self):
        # Egyelőre csak üzenet – későbbi bővítéshez alap
        QMessageBox.information(
            self,
            "Export",
            "Export funkció még nincs implementálva."
        )

    def apply_white_theme(self):
        app.setStyle("Fusion")  # opcionális: egységesítés

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("white"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        palette.setColor(QPalette.ColorRole.Base, QColor("white"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#f0f0f0"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("white"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("black"))
        palette.setColor(QPalette.ColorRole.Text, QColor("black"))
        palette.setColor(QPalette.ColorRole.Button, QColor("white"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("black"))
        palette.setColor(QPalette.ColorRole.BrightText, QColor("red"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#87cefa"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("black"))

        app.setPalette(palette)
        self.central_widget.setStyleSheet("background-color: white; color: black;")

    def apply_no_theme(self):
        app.setStyle("Fusion")  # vagy akár visszaállíthatod a rendszer stílusát
        app.setPalette(app.style().standardPalette())
        self.central_widget.setStyleSheet("")  # minden saját stílus törlése


    def initUI(self):

        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        control_widget = QWidget()
        control_layout = QVBoxLayout()

        # Számláló input
        num_layout = QHBoxLayout()
        num_layout.addWidget(QLabel('Számláló együtthatók:'))
        self.num_input = QLineEdit('1')
        num_layout.addWidget(self.num_input)

        # Nevező input
        den_layout = QHBoxLayout()
        den_layout.addWidget(QLabel('Nevező együtthatók:'))
        self.den_input = QLineEdit('1, 2, 2')
        den_layout.addWidget(self.den_input)

        # Gombok, címkék
        self.button = QPushButton('Frissítés')
        self.button.clicked.connect(self.update_plots)
        self.stability_label = QLabel('')
        self.poles_label = QLabel('Pólus koordináták:')
        self.poles_label.setWordWrap(True)

        # Azimut csúszka
        self.azimuth_slider = QSlider(Qt.Orientation.Horizontal)
        self.azimuth_slider.setMinimum(-90)
        self.azimuth_slider.setMaximum(90)
        self.azimuth_slider.setValue(-60)
        self.azimuth_slider.valueChanged.connect(self.update_plots)

        # Leírás
        description = QTextEdit()
        description.setReadOnly(True)
        description.setPlainText(
            "A számláló és nevező együtthatók a következő alakban kerülnek az átviteli függvénybe:\n\n"
            "                Számláló\n"
            "H(s) = ------------------\n"
            "                Nevező\n\n"
            "Példa: \n"
            "Számláló: 1\n"
            "Nevező: 1, 2, 2\n"
            "Ekkor H(s) = 1 / (s² + 2s + 2)\n\n"
            "Ha több együtthatót írsz be:\n"
            "- Számláló: 2, 5, 3 esetén\n H(s) = 2s² + 5s + 3\n"
            "- Nevező: 1, 4, 5, 0, 2 esetén\n H(s) = s⁴ + 4s³ + 5s² + 0s + 2"
        )

        control_layout.addWidget(description)
        control_layout.addLayout(num_layout)
        control_layout.addLayout(den_layout)
        control_layout.addWidget(self.button)
        control_layout.addWidget(self.stability_label)
        control_layout.addWidget(self.poles_label)
        control_layout.addWidget(QLabel('3D nézet (azimut forgatás):'))
        control_layout.addWidget(self.azimuth_slider)

        control_widget.setLayout(control_layout)
        control_widget.setFixedWidth(240)

        # Plotok
        plot_splitter = QSplitter(Qt.Orientation.Vertical)
        plot_splitter.setSizes([350, 650])  # kb. 35% és 65% ha az ablak magassága 1000px


        self.figure_top = plt.figure()
        self.canvas_top = FigureCanvas(self.figure_top)

        self.figure_bottom = plt.figure()
        self.canvas_bottom = FigureCanvas(self.figure_bottom)
        self.canvas_top.setMinimumHeight(150)

        self.canvas_bottom.setMinimumHeight(150)

        plot_splitter.addWidget(self.canvas_top)
        plot_splitter.addWidget(self.canvas_bottom)

        main_splitter.addWidget(control_widget)
        main_splitter.addWidget(plot_splitter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(main_splitter)

        self.central_widget.setLayout(main_layout)

        # 35% felső plot, 65% 3D alsó plot
        plot_splitter.setSizes([350, 650])

        self.update_plots()

    def update_plots(self):
        try:
            num = [float(x) for x in self.num_input.text().split(',')]
            den = [float(x) for x in self.den_input.text().split(',')]
        except ValueError:
            self.stability_label.setText("Hiba: Nem szám érték!")
            return

        system_ctrl = ctrl.tf(num, den)
        system_scipy = TransferFunction(num, den)
        poles = ctrl.poles(system_ctrl)

        # Stabilitás vizsgálat
        is_asymptotically_stable = all(np.real(poles) < 0)
        is_marginally_stable = np.all(np.real(poles) <= 0) and np.any(np.real(poles) == 0)
        if is_asymptotically_stable:
            stab_type = "Aszimptotikusan stabil"
        elif is_marginally_stable:
            stab_type = "Marginálisan stabil"
        else:
            stab_type = "Instabil"

        # Kiírás: új sorban
        self.stability_label.setText(f'A rendszer stabilitása:\n{stab_type}')

        # Pólusok szövegesen
        pole_text = '\n'.join([
            f"s{i + 1} = {p.real:.2f} {'+' if p.imag >= 0 else '-'} {abs(p.imag):.2f}j"
            for i, p in enumerate(poles)
        ])
        self.poles_label.setText(
            f'Pólus koordináták:\n{pole_text}' if poles.size > 0 else 'Nincsenek pólusok.'
        )

        # Plotok – 2x2: pólus, impulzus, Bode amplitúdó és fázis
        self.figure_top.clf()
        # gs = self.figure_top.add_gridspec(2, 2, width_ratios=[1.3, 2.2], height_ratios=[1, 1])
        # ax1 = self.figure_top.add_subplot(gs[0, 0])
        # ax2 = self.figure_top.add_subplot(gs[1, 0])
        # axb1 = self.figure_top.add_subplot(gs[0, 1])
        # axb2 = self.figure_top.add_subplot(gs[1, 1])
        gs_bode = self.figure_top.add_gridspec(1, 2, left=0.02, right=0.98, top=0.90, bottom=0.2, wspace=0.3)
        ax1 = self.figure_top.add_subplot(gs_bode[0, 0])
        ax2 = self.figure_top.add_subplot(gs_bode[0, 1])

        # Pólustérkép
        ax1.axhline(0, color='gray', lw=0.5)
        ax1.axvline(0, color='gray', lw=0.5)
        ax1.scatter(np.real(poles), np.imag(poles), marker='x', color='red', label='Pólus')
        ax1.set_title('Pólus térkép')
        ax1.set_xlabel('Re')
        ax1.set_ylabel('Im')
        ax1.grid(True)
        ax1.legend(fontsize='small')

        # Impulzusválasz
        t, y = impulse(system_scipy)
        ax2.plot(t, y)
        ax2.set_title('Impulzusválasz h(t)')
        ax2.set_xlabel('t')
        ax2.grid(True)

        # # Bode-adatok: amplitúdó és fázis
        # try:
        #     omega = np.logspace(-2, 2, 500)
        #     mag, phase, omega = system_ctrl.frequency_response(omega)
        #
        #     # lapítás és konvertálás
        #     mag = mag.flatten()
        #     phase = np.unwrap(phase.flatten()) * 180 / np.pi
        #
        #     axb1.semilogx(omega, 20 * np.log10(mag), label='|H(jω)| [dB]')
        #     axb1.set_title('Bode amplitúdó')
        #     axb1.set_xlabel('ω [rad/s]')
        #     axb1.set_ylabel('dB')
        #     axb1.grid(True, which='both')
        #     axb1.legend(fontsize='small')
        #
        #     axb2.semilogx(omega, np.degrees(phase), label='arg(H(jω)) [fok]', color='tab:orange')
        #     axb2.set_title('Bode fázis')
        #     axb2.set_xlabel('ω [rad/s]')
        #     axb2.set_ylabel('Fázis [°]')
        #     axb2.grid(True, which='both')
        #     axb2.legend(fontsize='small')
        # except Exception as e:
        #     axb1.text(0.5, 0.5, f"Bode hiba:\n{e}", ha='center', va='center', color='red')
        #     axb2.text(0.5, 0.5, f"Bode hiba:\n{e}", ha='center', va='center', color='red')
        #
        # self.figure_top.tight_layout()



        self.canvas_top.draw()

        # 3D |H(s)| plot – marad, ahogy volt
        if len(poles) > 0:
            real_parts = np.real(poles)
            imag_parts = np.imag(poles)
            real_min = np.min(real_parts) - 2
            real_max = np.max(real_parts) + 2
            imag_min = np.min(imag_parts) - 2
            imag_max = np.max(imag_parts) + 2
        else:
            real_min, real_max = -5, 1
            imag_min, imag_max = -5, 5

        re = np.linspace(real_min, real_max, 50)
        im = np.linspace(imag_min, imag_max, 50)
        Re, Im = np.meshgrid(re, im)
        s = Re + 1j * Im

        H_s = np.vectorize(lambda s_val: ctrl.evalfr(system_ctrl, s_val))(s)
        Z = np.abs(H_s)

        self.figure_bottom.clf()
        ax3 = self.figure_bottom.add_subplot(111, projection='3d')
        ax3.plot_surface(Re, Im, Z, cmap='viridis', edgecolor='none', antialiased=True)
        ax3.set_title('|H(s)| a komplex sík felett (3D)')
        ax3.set_xlabel('Re(s)')
        ax3.set_ylabel('Im(s)')
        ax3.set_zlabel('|H(s)|')

        azim_angle = self.azimuth_slider.value()
        ax3.view_init(elev=30, azim=azim_angle)

        self.canvas_bottom.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    gui = TransferFunctionGUI()
    gui.show()
    sys.exit(app.exec())
