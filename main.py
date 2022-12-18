import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
import sys
import datetime
from pylocalstorage import LocalStorage
from app.src.Dash.index import panelGeneral
from app.src.Services.dbConnect import conexionBd
from app.src.Services.querys import findMatricula
from app.src.View.vistaRutaCritica import Ui_MainWindow as ventanaPrincipal
import warnings

warnings.filterwarnings("ignore")


class MyApp(QtWidgets.QMainWindow, ventanaPrincipal):
    def __init__(self):
        #LocalStorage().clear()
        QtWidgets.QMainWindow.__init__(self)
        ventanaPrincipal.__init__(self)
        self.setupUi(self)
        acciones(self)


def acciones(ventana):
    cargarLogo(ventana, "./app/src/Dash/assets/logoUP.png")
    ventana.reinscripcionBotton.clicked.connect(lambda: informacionAlumnado(ventana))#reinscripcion(ventana))


def cargarLogo(ventana, ruta):
    imagen = QPixmap(ruta)  # PyQt5.QPixmap(ruta)
    ventana.photo.setPixmap(imagen)


def mostrarMensajes(ventana, texto):
    msg = QMessageBox()
    msg.setText(texto)
    msg.setWindowTitle("Error")
    msg.setIcon(QMessageBox.Information)
    msg.setStyleSheet("background-color: white;color: rgb(0, 0, 0)")
    msg.exec_()

def informacionAlumnado(ventana):
    if len(ventana.matricula.toPlainText()) == 0:
        mostrarMensajes(ventana,"Ingrese Una Matricula")
    else:
        resultado = pd.read_sql(findMatricula(int(ventana.matricula.toPlainText())), con=conexionBd())
        if len(resultado) > 0:
            # Obtengo matricula del alumno
            matriculaAlumno = int(ventana.matricula.toPlainText()) # 191287

            # obtengo la fecha actual
            dt = datetime.datetime.today().month

            # puerto para despliegue
            puerto = int(str(matriculaAlumno)[0:3] + str(matriculaAlumno)[-1])
            #puerto = int(str(matriculaAlumno)[0] + str(matriculaAlumno % 10000))

            infoAlumno = {"matriculaAlumno": matriculaAlumno, "mes": dt}

            # guardo la informacion del alumno en el storage
            LocalStorage().setItem("informacionAlumno", infoAlumno)
            LocalStorage().setItem("informacionAlumno", infoAlumno)

            # informacion
            panelGeneral(puerto)
        else:
            mostrarMensajes(ventana, "Matricula No Registrada En La Base De Datos")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    window.setFixedSize(window.size())
    app.exec_()