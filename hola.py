import pygame
import random
import sys

# Inicializar pygame
pygame.init()

# Configuración de colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE_CLARO = (144, 238, 144)

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
TAMAÑO_CELDA = 20

# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('🐍 La Viborita')

# Reloj para controlar la velocidad
reloj = pygame.time.Clock()

class Serpiente:
    def __init__(self):
        self.cuerpo = [(ANCHO // 2, ALTO // 2)]
        self.direccion = (TAMAÑO_CELDA, 0)  # Inicialmente se mueve a la derecha
        self.crecer = False
    
    def mover(self):
        cabeza = self.cuerpo[0]
        nueva_cabeza = (cabeza[0] + self.direccion[0], cabeza[1] + self.direccion[1])
        self.cuerpo.insert(0, nueva_cabeza)
        
        if not self.crecer:
            self.cuerpo.pop()
        else:
            self.crecer = False
    
    def cambiar_direccion(self, nueva_direccion):
        # Evitar que la serpiente se mueva en dirección opuesta
        if (nueva_direccion[0] * -1, nueva_direccion[1] * -1) != self.direccion:
            self.direccion = nueva_direccion
    
    def verificar_colision(self):
        cabeza = self.cuerpo[0]
        
        # Colisión con los bordes
        if (cabeza[0] < 0 or cabeza[0] >= ANCHO or 
            cabeza[1] < 0 or cabeza[1] >= ALTO):
            return True
        
        # Colisión consigo misma
        if cabeza in self.cuerpo[1:]:
            return True
        
        return False
    
    def comer(self):
        self.crecer = True
    
    def dibujar(self, pantalla):
        for i, segmento in enumerate(self.cuerpo):
            if i == 0:  # Cabeza
                pygame.draw.rect(pantalla, VERDE_CLARO, 
                               (segmento[0], segmento[1], TAMAÑO_CELDA, TAMAÑO_CELDA))
                # Dibujar ojos
                pygame.draw.circle(pantalla, NEGRO, 
                                 (segmento[0] + 5, segmento[1] + 5), 2)
                pygame.draw.circle(pantalla, NEGRO, 
                                 (segmento[0] + 15, segmento[1] + 5), 2)
            else:  # Cuerpo
                pygame.draw.rect(pantalla, VERDE, 
                               (segmento[0], segmento[1], TAMAÑO_CELDA, TAMAÑO_CELDA))
                pygame.draw.rect(pantalla, NEGRO, 
                               (segmento[0], segmento[1], TAMAÑO_CELDA, TAMAÑO_CELDA), 1)

class Comida:
    def __init__(self):
        self.posicion = self.generar_posicion()
    
    def generar_posicion(self):
        x = random.randint(0, (ANCHO - TAMAÑO_CELDA) // TAMAÑO_CELDA) * TAMAÑO_CELDA
        y = random.randint(0, (ALTO - TAMAÑO_CELDA) // TAMAÑO_CELDA) * TAMAÑO_CELDA
        return (x, y)
    
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, ROJO, 
                         (self.posicion[0] + TAMAÑO_CELDA // 2, 
                          self.posicion[1] + TAMAÑO_CELDA // 2), 
                         TAMAÑO_CELDA // 2)

def mostrar_puntuacion(pantalla, puntuacion):
    fuente = pygame.font.Font(None, 36)
    texto = fuente.render(f'Puntuación: {puntuacion}', True, BLANCO)
    pantalla.blit(texto, (10, 10))

def mostrar_game_over(pantalla, puntuacion):
    fuente_grande = pygame.font.Font(None, 72)
    fuente_mediana = pygame.font.Font(None, 36)
    
    # Fondo semitransparente
    superficie_overlay = pygame.Surface((ANCHO, ALTO))
    superficie_overlay.set_alpha(128)
    superficie_overlay.fill(NEGRO)
    pantalla.blit(superficie_overlay, (0, 0))
    
    # Texto Game Over
    texto_game_over = fuente_grande.render('GAME OVER', True, ROJO)
    rect_game_over = texto_game_over.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    pantalla.blit(texto_game_over, rect_game_over)
    
    # Puntuación final
    texto_puntuacion = fuente_mediana.render(f'Puntuación Final: {puntuacion}', True, BLANCO)
    rect_puntuacion = texto_puntuacion.get_rect(center=(ANCHO // 2, ALTO // 2))
    pantalla.blit(texto_puntuacion, rect_puntuacion)
    
    # Instrucciones
    texto_reiniciar = fuente_mediana.render('Presiona R para reiniciar o Q para salir', True, BLANCO)
    rect_reiniciar = texto_reiniciar.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
    pantalla.blit(texto_reiniciar, rect_reiniciar)

def mostrar_pausa(pantalla):
    fuente = pygame.font.Font(None, 72)
    texto_pausa = fuente.render('PAUSADO', True, BLANCO)
    rect_pausa = texto_pausa.get_rect(center=(ANCHO // 2, ALTO // 2))
    
    # Fondo semitransparente
    superficie_overlay = pygame.Surface((ANCHO, ALTO))
    superficie_overlay.set_alpha(128)
    superficie_overlay.fill(NEGRO)
    pantalla.blit(superficie_overlay, (0, 0))
    
    pantalla.blit(texto_pausa, rect_pausa)
    
    fuente_pequena = pygame.font.Font(None, 36)
    texto_continuar = fuente_pequena.render('Presiona P para continuar', True, BLANCO)
    rect_continuar = texto_continuar.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
    pantalla.blit(texto_continuar, rect_continuar)

def mostrar_instrucciones(pantalla):
    fuente = pygame.font.Font(None, 28)
    instrucciones = [
        "🐍 LA VIBORITA 🐍",
        "",
        "Controles:",
        "↑ ↓ ← → : Mover la serpiente",
        "P : Pausar/Continuar",
        "R : Reiniciar juego",
        "Q : Salir",
        "",
        "¡Come la comida roja para crecer!",
        "¡Evita chocar con las paredes y contigo mismo!",
        "",
        "Presiona cualquier tecla para comenzar..."
    ]
    
    pantalla.fill(NEGRO)
    y = 100
    for linea in instrucciones:
        if linea == "🐍 LA VIBORITA 🐍":
            fuente_titulo = pygame.font.Font(None, 48)
            texto = fuente_titulo.render(linea, True, VERDE)
        elif linea.startswith("Controles:") or linea.startswith("¡"):
            texto = fuente.render(linea, True, VERDE_CLARO)
        else:
            texto = fuente.render(linea, True, BLANCO)
        
        rect_texto = texto.get_rect(center=(ANCHO // 2, y))
        pantalla.blit(texto, rect_texto)
        y += 35

def main():
    serpiente = Serpiente()
    comida = Comida()
    puntuacion = 0
    juego_terminado = False
    pausado = False
    mostrar_inicio = True
    
    # Bucle principal del juego
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if mostrar_inicio:
                    mostrar_inicio = False
                elif juego_terminado:
                    if evento.key == pygame.K_r:
                        # Reiniciar juego
                        serpiente = Serpiente()
                        comida = Comida()
                        puntuacion = 0
                        juego_terminado = False
                    elif evento.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                else:
                    # Controles de movimiento
                    if evento.key == pygame.K_UP:
                        serpiente.cambiar_direccion((0, -TAMAÑO_CELDA))
                    elif evento.key == pygame.K_DOWN:
                        serpiente.cambiar_direccion((0, TAMAÑO_CELDA))
                    elif evento.key == pygame.K_LEFT:
                        serpiente.cambiar_direccion((-TAMAÑO_CELDA, 0))
                    elif evento.key == pygame.K_RIGHT:
                        serpiente.cambiar_direccion((TAMAÑO_CELDA, 0))
                    elif evento.key == pygame.K_p:
                        pausado = not pausado
                    elif evento.key == pygame.K_r:
                        # Reiniciar juego
                        serpiente = Serpiente()
                        comida = Comida()
                        puntuacion = 0
                        juego_terminado = False
                    elif evento.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
        
        if mostrar_inicio:
            mostrar_instrucciones(pantalla)
        elif not juego_terminado and not pausado:
            # Mover serpiente
            serpiente.mover()
            
            # Verificar colisiones
            if serpiente.verificar_colision():
                juego_terminado = True
            
            # Verificar si comió
            if serpiente.cuerpo[0] == comida.posicion:
                serpiente.comer()
                puntuacion += 10
                # Generar nueva comida
                while True:
                    comida.posicion = comida.generar_posicion()
                    if comida.posicion not in serpiente.cuerpo:
                        break
            
            # Dibujar todo
            pantalla.fill(NEGRO)
            serpiente.dibujar(pantalla)
            comida.dibujar(pantalla)
            mostrar_puntuacion(pantalla, puntuacion)
        
        elif pausado:
            mostrar_pausa(pantalla)
        
        elif juego_terminado:
            mostrar_game_over(pantalla, puntuacion)
        
        pygame.display.flip()
        reloj.tick(7)  # 7 FPS - velocidad más lenta

if __name__ == "__main__":
    main()
