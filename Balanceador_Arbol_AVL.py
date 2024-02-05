import sys #Accede a los argumentos de la línea de comandos y finalizar la aplicación
import matplotlib.pyplot as plt #Genera los nodos y las conexiones del árbol avl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas #Muestra las figuras generadas de Matplotlib en la interfaz de PyQT5 
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget #Crea la ventana principal y sus componentes (etiqueta, input, y boton)


#Definimos la clase nodo
class Nodo:
    def __init__(self, data): #Creamos el constructor que recibe los siguientes atributos
        self.data = data    #Almacena el valor contenido en el nodo cuando se inserta
        self.izquierda = None #Apunta al nodo hijo izquierdo actual, sino hay un nodo el valor sera ninguno 
        self.derecha = None #Apunta al nodo hijo derecho actual, sino hay un nodo el valor sera

class ArbolAVL: #Definimos la clase que inicializará lo que es el nodo raíz como vacio 
    def __init__(self):
        self.raiz = None

    def insertar(self, data): #Inserta un nuevo nodo en el árbol  AVL 
        self.raiz = self._insertar(self.raiz, data) #Inserción y asigna el valor del nodo raíz

    def _insertar(self, raiz, data): #Hace la inserción de un nuevo nodo
        if not raiz: #Si la raíz es ninguna
            return Nodo(data) #Se crea un nuevo nodo y se inserta como raíz
        elif data < raiz.data: #Si el dato ingresado es menor al dato de raíz lo acomodará a la izquierda
            raiz.izquierda = self._insertar(raiz.izquierda, data) #Insertar el dato a la izquierda
        else:
            raiz.derecha = self._insertar(raiz.derecha, data) # Sí es mayor insertar a la derecha

        factor_balance = self._obtener_factor_balance(raiz) #Obtiene el factor de balance

        if factor_balance > 1: #Si el factor de balance es mayor a 1 el nodo raíz 
            if data < raiz.izquierda.data: #Si el dato es menor a la raíz la raíz el dato de la raíz para a la izquierda
                return self._rotar_derecha(raiz) #Asigna el valor a la función de rotación a la derecha
            else: #Si no ocurre lo contrario
                raiz.izquierda = self._rotar_izquierda(raiz.izquierda)
                return self._rotar_derecha(raiz)
        if factor_balance < -1: #Aquí sucede lo mismo, si el valor del factor de balance es menor a -1 el nodo raíz
            if data > raiz.derecha.data:  #El dato de la raíz pasa a el dato de ese nodo a la derecha
                return self._rotar_izquierda(raiz) #Retorna el valor de la raíz a la izquierda
            else: #Sino a la derecha
                raiz.derecha = self._rotar_derecha(raiz.derecha)
                return self._rotar_izquierda(raiz)

        return raiz #Sale del condicional y retorna la raíz de acuerdo al nodo que se tenga en la raíz

    def _obtener_altura(self, raiz): #Obtiene la altura del arbol el maximo valor de la altura del subhijo izquiero y derecho usando recursión
        if not raiz:
            return 0
        return max(self._obtener_altura(raiz.izquierda), self._obtener_altura(raiz.derecha)) + 1

    def _obtener_factor_balance(self, raiz): #Obtiene el factor de balance de cada nodo usando la recursión
        if not raiz:
            return 0
        return self._obtener_altura(raiz.izquierda) - self._obtener_altura(raiz.derecha)

    def _rotar_izquierda(self, z):
        y = z.derecha
        if not y:
            return z

        T3 = y.izquierda
        #Hace la rotación izquierda intercambiando los nodos Y, Z 
        y.izquierda = z
        z.derecha = T3

        return y

    def _rotar_derecha(self, z):
        y = z.izquierda
        if not y:
            return z

        T2 = y.derecha
        #Realiza la rotación derecha intercambiando los nodos Y, Z
        y.derecha = z
        z.izquierda = T2

        return y

    def dibujar(self): # Se encarga de realizar el dibujo pasandole los valore de x, y y el espaciado entre los nodos
        self._dibujar_auxiliar(self.raiz, 0, 0, 20)

    def _dibujar_auxiliar(self, raiz, x, y, espaciado): #Este se encarga de  realizar el dibujo recursivamente de cada subhijo
        if not raiz:
            return
        #Calculan las coordenadas para cada nodo
        x_izquierda = x - espaciado #Posiciona al nodo hijo izquierdo a una distancia horizontal hacia la izauierda respecto a un nodo que se encuentre ya ahí 
        x_derecha = x + espaciado #Calcula el espaciado a la coordenada x y posicionarlo horizotalmente hacia la derecha
        #Se encarga de dibujar el texto de cada nodo de acuerdo a su posicion que es en x y y y darle los estilos
        plt.text(x, y, str(raiz.data), style='italic', bbox={'facecolor': '#37B449', 'edgecolor': 'darkgreen', 'pad': 1, 'boxstyle': 'circle'})

        if raiz.izquierda: #Verifica que el nodo actual tenga un hijo izquierdo, si la tiene la dibuja desde (x, y) hasta (x_izquierda, y -1);
            plt.plot([x, x_izquierda], [y, y - 1], color='black')
            self._dibujar_auxiliar(raiz.izquierda, x_izquierda, y - 1, espaciado / 2)

        if raiz.derecha: #Verifica que el nodo actual tenga un hijo derecho, si la tiene la dibuja desde (x, y) hasta (x_derecha, y -1);
            plt.plot([x, x_derecha], [y, y - 1], color='black')
            self._dibujar_auxiliar(raiz.derecha, x_derecha, y - 1, espaciado / 2)


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.arbol_avl = ArbolAVL()

        self.setWindowTitle("Balanceador de Árboles AVL")

        self.etiqueta = QLabel("Ingresa un número:")
        self.entrada = QLineEdit()
        self.boton = QPushButton("Agregar")
        self.boton.clicked.connect(self.manejar_insercion)

        self.figura = plt.figure()
        self.canvas = FigureCanvas(self.figura)

        layout = QVBoxLayout()
        layout.addWidget(self.etiqueta)
        layout.addWidget(self.entrada)
        layout.addWidget(self.boton)
        layout.addWidget(self.canvas)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def manejar_insercion(self):
        #Maneja el evento de clic en el boton "Agregar"
        valor = self.entrada.text()
        try:
            numero = int(valor)
            self.arbol_avl.insertar(numero)
            self.entrada.clear()
            self.dibujar_arbol_avl()
        except ValueError:
            self.entrada.clear()
            self.entrada.setText("Entrada inválida. Ingresa un número.")

    def dibujar_arbol_avl(self):
        #Borra la figura actual y dibuja el arbol actualizado 
        self.figura.clear()
        self.arbol_avl.dibujar()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()
    ventana_principal.show()
    sys.exit(app.exec_()) #aquí

