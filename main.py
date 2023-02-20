from Environment import Town
import pygame

myTown = Town(600,600,(0,100,0))

def main():
    run = True
    while run:
        myTown.display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()

main()
