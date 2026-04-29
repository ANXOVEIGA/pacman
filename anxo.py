# --- CONTROLES ---
win.listen()
win.onkeypress(lambda: setattr(pacman, "direction", "up"), "w")
win.onkeypress(lambda: setattr(pacman, "direction", "down"), "s")
win.onkeypress(lambda: setattr(pacman, "direction", "left"), "a")
win.onkeypress(lambda: setattr(pacman, "direction", "right"), "d")

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