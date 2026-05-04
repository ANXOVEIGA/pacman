import turtle
import time
import random

# --- CONFIGURACIÓN CRÍTICA ---
win = turtle.Screen()
win.title("Pac-Man Definitive Edition")
win.bgcolor("black")
win.setup(width=600, height=700)
win.tracer(0) 

# --- VARIABLES GLOBALES ---
puntos = 0
vidas = 3
estado_powerup = False
timer_powerup = 0

# --- CLASES ---
class Elemento(turtle.Turtle):
    def __init__(self, color, x, y, forma="square", size=1):
        super().__init__(shape=forma)
        self.penup()
        self.speed(0)
        self.color(color)
        self.shapesize(size, size)
        self.goto(x, y)

class Personaje(Elemento):
    def __init__(self, color, x, y, es_pacman=True):
        forma = "circle" if es_pacman else "square"
        super().__init__(color, x, y, forma)
        self.direction = "stop"
        self.spawn = (x, y)
        self.color_original = color

    def mover(self, muros):
        paso = 20
        old_x, old_y = self.xcor(), self.ycor()
        
        if self.direction == "up": self.sety(old_y + paso)
        if self.direction == "down": self.sety(old_y - paso)
        if self.direction == "left": self.setx(old_x - paso)
        if self.direction == "right": self.setx(old_x + paso)

        # Túnel
        if self.xcor() > 280: self.setx(-280)
        elif self.xcor() < -280: self.setx(280)

        # Colisión con muros
        for m in muros:
            if self.distance(m) < 15:
                self.goto(old_x, old_y)
                return False
        return True

# --- MAPA ---
layout = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X0XXXX.XXXXX.XX.XXXXX.XXXX0X", # '0' son Power-Ups
    "X..........................X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X......XX....XX....XX......X",
    "XXXXXX.XXXXX XX XXXXX.XXXXXX",
    "     X.XX    G     XX.X     ",
    "XXXXXX.XX XXXXXXXX XX.XXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X0..XX.......P........XX..0X",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "X......XX....XX....XX......X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

muros, comida, powerups, fantasmas = [], [], [], []
for r, fila in enumerate(layout):
    for c, char in enumerate(fila):
        x, y = -270 + (c * 20), 220 - (r * 20)
        if char == "X": muros.append(Elemento("blue", x, y))
        elif char == ".":
            dot = Elemento("white", x, y, size=0.2)
            comida.append(dot)
        elif char == "0":
            p = Elemento("white", x, y, forma="circle", size=0.6)
            powerups.append(p)
        elif char == "P": pacman = Personaje("yellow", x, y)
        elif char == "G":
            colores = ["red", "pink", "cyan", "orange"]
            for i in range(4):
                fantasmas.append(Personaje(colores[i], x, y, False))

# --- CONTROLES ---
win.listen()
win.onkeypress(lambda: setattr(pacman, "direction", "up"), "w")
win.onkeypress(lambda: setattr(pacman, "direction", "down"), "s")
win.onkeypress(lambda: setattr(pacman, "direction", "left"), "a")
win.onkeypress(lambda: setattr(pacman, "direction", "right"), "d")
marcador = Elemento("white", 0, 280)
marcador.hideturtle()

def actualizar_marcador():
    marcador.clear()
    marcador.write(f"PUNTOS: {puntos}  VIDAS: {vidas}", align="center", font=("Arial", 16, "bold"))

actualizar_marcador()

# --- BUCLE PRINCIPAL ---
while vidas > 0:
    pacman.mover(muros)

    # Comer puntos
    for c in comida[:]:
        if pacman.distance(c) < 10:
            c.goto(2000, 2000)
            comida.remove(c)
            puntos += 10
            actualizar_marcador()

    # Comer Power-Ups
    for p in powerups[:]:
        if pacman.distance(p) < 15:
            p.goto(2000, 2000)
            powerups.remove(p)
            estado_powerup = True
            timer_powerup = time.time() + 7 # 7 segundos de poder
            for f in fantasmas: f.color("blue")

    # Gestionar tiempo del Power-Up
    if estado_powerup and time.time() > timer_powerup:
        estado_powerup = False
        for f in fantasmas: f.color(f.color_original)

    # Lógica de fantasmas
    for g in fantasmas:
        # Movimiento: persigue o huye según el Power-Up
        if not g.mover(muros) or random.random() < 0.2:
            dirs = ["up", "down", "left", "right"]
            if not estado_powerup: # Perseguir
                if abs(pacman.xcor()-g.xcor()) > abs(pacman.ycor()-g.ycor()):
                    g.direction = "right" if pacman.xcor() > g.xcor() else "left"
                else:
                    g.direction = "up" if pacman.ycor() > g.ycor() else "down"
            else: # Huir
                g.direction = random.choice(dirs)

        # Colisión Pacman - Fantasmas
        if g.distance(pacman) < 15:
            if estado_powerup:
                puntos += 200
                actualizar_marcador()
                g.goto(g.spawn)
                g.direction = "stop"
            else:
                vidas -= 1
                actualizar_marcador()
                pacman.goto(pacman.spawn)
                pacman.direction = "stop"
                for f in fantasmas: f.goto(f.spawn)
                time.sleep(1)

    win.update()
    time.sleep(0.05) # Velocidad ideal para Turtle

win.mainloop()

# --- ESTADO DEL JUEGO ---
puntos = 0
vidas = 3

# Marcador en pantalla
marcador = turtle.Turtle()
marcador.speed(0)
marcador.color("white")
marcador.penup()
marcador.hideturtle()
marcador.goto(0, 280)

def actualizar_marcador():
    marcador.clear()
    marcador.write(f"PUNTOS: {puntos}   VIDAS: {vidas}", align="center", font=("Arial", 16, "bold"))

actualizar_marcador()

# --- BUCLE PRINCIPAL ---
while vidas > 0:
    try:
        pacman.move(muros)

        # Comer puntos
        for c in comida:
            if pacman.distance(c) < 10:
                c.goto(2000, 2000) # Lo quita de la vista
                comida.remove(c)
                puntos += 10
                actualizar_marcador()

        # Lógica de fantasmas
        for g in fantasmas:
            g.move(muros)
            
            # Colisión con Pac-Man
            if g.distance(pacman) < 15:
                vidas -= 1
                actualizar_marcador()
                time.sleep(1)
                pacman.goto(spawn_pacman)
                pacman.direction = "stop"
                if vidas == 0:
                    marcador.goto(0, 0)
                    marcador.write("GAME OVER", align="center", font=("Arial", 30, "bold"))

        win.update()
        time.sleep(0.01)
    except:
        break

win.mainloop()