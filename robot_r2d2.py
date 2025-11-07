import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("R2-D2 en acción 🤖")

r2d2 = pygame.image.load("r2d2.png")
r2d2 = pygame.transform.scale(r2d2, (100, 100))
sonido = pygame.mixer.Sound("beep.wav")

x, y = WIDTH // 2, HEIGHT // 2
velocidad = 5

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidad
        sonido.play()
    if teclas[pygame.K_RIGHT]:
        x += velocidad
        sonido.play()
    if teclas[pygame.K_UP]:
        y -= velocidad
        sonido.play()
    if teclas[pygame.K_DOWN]:
        y += velocidad
        sonido.play()

    pantalla.fill((0, 0, 20))
    pantalla.blit(r2d2, (x, y))
    pygame.display.flip()
