import matplotlib.pyplot as plt
import numpy as np

class DibujadorGeometrico:
    
    def __init__(self, titulo="Dibujo Interactivo de Líneas y Polígonos"):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title(titulo)
        self.ax.set_xlim(0, 10)  # Rango del eje X
        self.ax.set_ylim(0, 10)  # Rango del eje Y
        self.ax.set_aspect('equal', adjustable='box') # Para asegurar que las formas no se distorsionen
        
        # Almacenamiento de los puntos
        self.puntos_x = []
        self.puntos_y = []
        
        # Referencia al objeto de línea para actualización en tiempo real (más eficiente)
        self.linea, = self.ax.plot(self.puntos_x, self.puntos_y, 'ro-', 
                                   label='Líneas Sucesivas', picker=5)
        
        # Conexion del evento de clic del raton
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        # Instrucciones en la consola
        print("-" * 40)
        print("Instrucciones:")
        print("Click izquierdo: Añade un nuevo punto y dibuja la línea al anterior.")
        print("Tecla 'c': Cierra el polígono (une el último punto con el primero).")
        print("Tecla 'n': Dibuja un polígono regular de N lados (solicita N por consola).")
        print("Tecla 'r': Limpia la pantalla para un nuevo dibujo.")
        print("-" * 40)

        plt.show() # Muestra la figura

    def on_click(self, event):
        """Maneja el evento de clic del ratón."""
        # Solo procesa clics dentro del área del grafico (no en títulos, etc.)
        if event.inaxes != self.ax:
            return
        
        # Trazado de lineas sucesivas (Click izquierdo - Boton 1)
        if event.button == 1:
            x, y = event.xdata, event.ydata
            self.puntos_x.append(x)
            self.puntos_y.append(y)
            print(f"Punto añadido: ({x:.2f}, {y:.2f})")
            
            # Actualiza el objeto de línea con los nuevos puntos
            self.linea.set_data(self.puntos_x, self.puntos_y)
            self.fig.canvas.draw()
            
        # Trazado de línea recta que une dos puntos (Último punto al primero, al presionar 'c')
        elif event.key == 'c':
            self.cerrar_poligono()
            
        # Dibujar un polígono regular de n lados (al presionar 'n')
        elif event.key == 'n':
            self.dibujar_poligono_n_lados()
            
        # Limpiar (Resetear al presionar 'r')
        elif event.key == 'r':
            self.reset_canvas()

    def cerrar_poligono(self):
        """Une el último punto con el primero para cerrar la forma."""
        n_puntos = len(self.puntos_x)
        if n_puntos < 3:
            print("Se necesitan al menos 3 puntos para cerrar un polígono.")
            return

        # Simplemente duplicamos el primer punto al final para cerrar el trazado
        puntos_x_cerrado = self.puntos_x + [self.puntos_x[0]]
        puntos_y_cerrado = self.puntos_y + [self.puntos_y[0]]

        # Dibujamos el polígono cerrado con un estilo diferente para distinguirlo
        self.ax.plot(puntos_x_cerrado, puntos_y_cerrado, 'b--', linewidth=1, 
                     label='Polígono Cerrado')
        
        print("Polígono cerrado (último punto unido al primero).")
        self.fig.canvas.draw()

    def generar_poligono_regular(self, n_lados, centro_x=5, centro_y=5, radio=3):
        """
        Genera las coordenadas para un polígono regular de n lados.
        Esta es la parte matemática crucial.
        """
        # Genera n ángulos equiespaciados de 0 a 2*pi
        # Utilizamos linspace para asegurar precisión.
        angulos = np.linspace(0, 2 * np.pi, n_lados, endpoint=False)
        
        # Formulas de coordenadas polares a cartesianas: 
        # x = r * cos(theta) + centro_x
        # y = r * sin(theta) + centro_y
        poly_x = radio * np.cos(angulos) + centro_x
        poly_y = radio * np.sin(angulos) + centro_y
        
        # Para cerrar el poligono, añadimos el primer punto al final
        poly_x = np.append(poly_x, poly_x[0])
        poly_y = np.append(poly_y, poly_y[0])
        
        return poly_x, poly_y

    def dibujar_poligono_n_lados(self):
        try:
            n_lados = int(input("Ingrese el número de lados (n >= 3): "))
            if n_lados < 3:
                print("El número de lados debe ser 3 o más.")
                return
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número entero.")
            return

        # Limpiamos el dibujo interactivo para mostrar el polígono regular
        self.reset_canvas(full_reset=False) 
        
        poly_x, poly_y = self.generar_poligono_regular(n_lados)
        
        # Dibujamos el nuevo poligono regular
        self.ax.plot(poly_x, poly_y, 'g-', linewidth=2, label=f'{n_lados}-ágono Regular')
        self.ax.set_title(f"{n_lados}-ágono Regular")
        self.fig.canvas.draw()
        print(f"Polígono regular de {n_lados} lados dibujado.")
        
    def reset_canvas(self, full_reset=True):
        if full_reset:
            self.puntos_x = []
            self.puntos_y = []
            self.linea.set_data([], [])
            
        # Limpia todas las demas lineas añadidas (como el polígono cerrado o regular)
        self.ax.cla() 
        
        # Restablecer la configuración inicial del eje
        self.ax.set_title("Dibujo Interactivo de Líneas y Polígonos")
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.set_aspect('equal', adjustable='box') 
        
        # Vuelve a crear la referencia de linea para el dibujo interactivo
        self.linea, = self.ax.plot(self.puntos_x, self.puntos_y, 'ro-', 
                                   label='Líneas Sucesivas', picker=5)
                                   
        self.fig.canvas.draw()
        print("Lienzo limpiado.")

# Para ejecutar la aplicacion
if __name__ == '__main__':
    DibujadorGeometrico()