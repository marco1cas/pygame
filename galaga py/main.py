import pygame
import random

pygame.init()
pygame.mixer.init()

# Lista de imágenes de fondo
fondos = ['imagenes/fondo1.png', 'imagenes/fondo2.jpg', 'imagenes/fondo3.jpg']
enemigo_imagenes = ['imagenes/E1.png', 'imagenes/E2.png', 'imagenes/E3.png']

# Cargar la primera imagen de fondo
fondo_index = 0
fondo = pygame.image.load(fondos[fondo_index])
nuevo_ancho = 800
nueva_altura = 460
fondo = pygame.transform.scale(fondo, (nuevo_ancho, nueva_altura))
width, height = fondo.get_width(), fondo.get_height()

laser_sonido = pygame.mixer.Sound('laser.wav')
explosion_sonido = pygame.mixer.Sound('explosion.wav')
golpe_sonido = pygame.mixer.Sound('golpe.wav')

explosion_list = []
for i in range(1, 13):
    explosion = pygame.image.load(f'explosion/{i}.png')
    explosion_list.append(explosion)

width = fondo.get_width()
height = fondo.get_height()
window = pygame.display.set_mode((800, 460))  # Tamaño fijo
pygame.display.set_caption('Juego Space Invaders')
run = True
fps = 60
clock = pygame.time.Clock()
score = 0
vida = 100
blanco = (255, 255, 255)
negro = (0, 0, 0)

def texto_puntuacion(frame, text, size, x, y):
    font = pygame.font.SysFont('Small Fonts', size, bold=True)
    text_frame = font.render(text, True, blanco, negro)
    text_rect = text_frame.get_rect()
    text_rect.midtop = (x, y)
    frame.blit(text_frame, text_rect)

def barra_vida(frame, x, y, nivel):
    longitud = 100
    alto = 20
    fill = int((nivel/100)*longitud)
    border = pygame.Rect(x, y, longitud, alto)
    fill = pygame.Rect(x, y, fill, alto)
    pygame.draw.rect(frame, (255, 0, 55), fill)
    pygame.draw.rect(frame, negro, border, 4)

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagenes_jugador = ['imagenes/A1.png', 'imagenes/A2.png', 'imagenes/A3.png']  # Lista de imágenes del jugador
        self.image_index = 0  # Índice de la imagen actual del jugador
        self.image = pygame.image.load(self.imagenes_jugador[self.image_index]).convert_alpha()
        pygame.display.set_icon(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.centery = height - 50
        self.velocidad_x = 0
        self.vida = 100

    def cambiar_imagen(self, fondo_index):
        # Cambiar la imagen del jugador según el fondo actual
        if fondo_index == 1:
            # Cambiar imágenes del jugador para el fondo 1
            self.imagenes_jugador = ['imagenes/A1.png', 'imagenes/A2.png', 'imagenes/A3.png']

        self.image_index = (self.image_index + 1) % len(self.imagenes_jugador)
        self.image = pygame.image.load(self.imagenes_jugador[self.image_index]).convert_alpha()

    def update(self):
        self.velocidad_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.velocidad_x = -5
        elif keystate[pygame.K_RIGHT]:
            self.velocidad_x = 5

        self.rect.x += self.velocidad_x
        if self.rect.right > width:
            self.rect.right = width
        elif self.rect.left < 0:
            self.rect.left = 0


    def disparar(self):
        bala = Balas(self.rect.centerx, self.rect.top)
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        laser_sonido.play()


class Enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.imagenes_enemigo = ['imagenes/E1.png', 'imagenes/E2.png', 'imagenes/E3.png']  # Lista de imágenes de enemigos
        self.image_index = 0  # Índice de la imagen actual de enemigos
        self.image = pygame.image.load(self.imagenes_enemigo[self.image_index]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1, width-50)
        self.rect.y = 10
        self.velocidad_y = random.randrange(-5, 20)

    def cambiar_imagen(self, fondo_index):
        # Cambiar la imagen de los enemigos según el fondo actual
        if fondo_index == 1:
            # Cambiar imágenes de los enemigos para el fondo 1
            self.imagenes_enemigo = ['imagenes/E2.png']
        elif fondo_index == 2:
            # Cambiar imágenes de los enemigos para el fondo 2
            self.imagenes_enemigo = ['imagenes/E3.png']

        self.image_index = (self.image_index + 1) % len(self.imagenes_enemigo)
        self.image = pygame.image.load(self.imagenes_enemigo[self.image_index]).convert_alpha()

    def update(self):
        self.time = random.randrange(-1, pygame.time.get_ticks()//5000)
        self.rect.x += self.time
        if self.rect.x >= width:
            self.rect.x = 0
            self.rect.y += 50

    def disparar_enemigos(self):
        bala = Balas_enemigos(self.rect.centerx, self.rect.bottom)
        grupo_jugador.add(bala)
        grupo_balas_enemigos.add(bala)
        laser_sonido.play()

class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/B2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad = -18

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()

class Balas_enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/B1.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = random.randrange(10, width)
        self.velocidad_y = 4

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom > height:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = explosion_list[0]
        img_scala = pygame.transform.scale(self.image, (20, 20))
        self.rect = img_scala.get_rect()
        self.rect.center = position
        self.time = pygame.time.get_ticks()
        self.velocidad_explo = 30
        self.frames = 0

    def update(self):
        tiempo = pygame.time.get_ticks()
        if tiempo - self.time > self.velocidad_explo:
            self.time = tiempo
            self.frames += 1
            if self.frames == len(explosion_list):
                self.kill()
            else:
                position = self.rect.center
                self.image = explosion_list[self.frames]
                self.rect = self.image.get_rect()
                self.rect.center = position

grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

player = Jugador()
grupo_jugador.add(player)
grupo_balas_jugador.add(player)

for x in range(10):
    enemigo = Enemigos(10, 10)
    grupo_enemigos.add(enemigo)
    grupo_jugador.add(enemigo)
    
while run:
    clock.tick(fps)

    # Cambiar el fondo, la imagen del jugador y la imagen de los enemigos según el puntaje
    if score > 150 and fondo_index == 0:
        fondo_index = 1
        fondo = pygame.image.load(fondos[fondo_index])
        fondo = pygame.transform.scale(fondo, (nuevo_ancho, nueva_altura))
        player.cambiar_imagen(fondo_index)  # Llamada al método cambiar_imagen del jugador
        for enemigo in grupo_enemigos:
            enemigo.cambiar_imagen(fondo_index)  # Llamada al método cambiar_imagen de los enemigos

    elif score > 250 and fondo_index == 1:
        fondo_index = 2
        fondo = pygame.image.load(fondos[fondo_index])
        fondo = pygame.transform.scale(fondo, (nuevo_ancho, nueva_altura))
        player.cambiar_imagen(fondo_index)  # Llamada al método cambiar_imagen del jugador
        for enemigo in grupo_enemigos:
            enemigo.cambiar_imagen(fondo_index)  # Llamada al método cambiar_imagen de los enemigos

    window.blit(fondo, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.disparar()

    grupo_jugador.update()
    grupo_enemigos.update()
    grupo_balas_jugador.update()
    grupo_balas_enemigos.update()

    grupo_jugador.draw(window)

    # Coliciones balas_jugador - enemigo
    colicion1 = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, True, True)
    for i in colicion1:
        score += 10
        enemigo.disparar_enemigos()
        enemigo = Enemigos(300, 10)
        grupo_enemigos.add(enemigo)
        grupo_jugador.add(enemigo)

        explo = Explosion(i.rect.center)
        grupo_jugador.add(explo)
        explosion_sonido.set_volume(0.3)
        explosion_sonido.play()

    # Coliciones jugador - balas_enemigo
    colicion2 = pygame.sprite.spritecollide(player, grupo_balas_enemigos, True)
    for j in colicion2:
        player.vida -= 10
        if player.vida <= 0:
            run = False
        explo1 = Explosion(j.rect.center)
        grupo_jugador.add(explo1)
        golpe_sonido.play()

    # Coliciones jugador - enemigo
    hits = pygame.sprite.spritecollide(player, grupo_enemigos, False)
    for hit in hits:
        player.vida -= 100
        enemigos = Enemigos(10, 10)
        grupo_jugador.add(enemigos)
        grupo_enemigos.add(enemigos)
        if player.vida <= 0:
            run = False

    # Indicador y Score
    texto_puntuacion(window, ('  SCORE: '+ str(score)+'       '), 30, width-85, 2)
    barra_vida(window, width-285, 0, player.vida)

    # Verificar si el juego ha terminado por ganar o perder
    if score >= 500:
        texto_puntuacion(window, "¡Ganaste, Aprobaste Programacion III!", 50, width//2, height//2)
        pygame.display.flip()
        pygame.time.wait(5000)  # Esperar 2 segundos antes de salir
        run = False

    elif player.vida <= 0:
        texto_puntuacion(window, "Game Over", 50, width//2, height//2)
        pygame.display.flip()
        pygame.time.wait(5000)  # Esperar 2 segundos antes de salir
        run = False

    pygame.display.flip()

pygame.quit()