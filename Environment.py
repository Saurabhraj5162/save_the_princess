import pygame



class Town:
    def __init__(self, height, width, background_color) -> None:
        
        self.height = height
        self.width = width
        self.rows = 6
        self.cols = 6
        self.block_size = height//self.rows
        self.background_color = background_color
        self.black_color = (0,0,0)
        self.red = (200,0,0)


        self.prince_start = (5,3)
        self.princess_start = (0,5)
        self.castle_pos = (0,5)
        self.enemy_pos = [(0,4), (1,4), (4,3), (3,1), (2,2)]
        self.pub_pos = (3,2)
        self.restaurant_pos = (1,2)
        self.safe_house_pos = (3,0)


        #getting rectangles of objects:
        self.prince = pygame.image.load('images/prince.png')
        self.prince_rect = self.prince.get_rect()

        self.princess = pygame.image.load('images/princess.png')
        self.princess_rect = self.princess.get_rect()

        self.enemy = pygame.image.load('images/enemy.png')
        self.enemy_rect = self.enemy.get_rect()

        self.restaurant = pygame.image.load('images/restaurant.png')
        self.restaurant_rect = self.restaurant.get_rect()

        self.castle = pygame.image.load('images/castle.png')
        self.castle_rect = self.castle.get_rect()

        self.pub = pygame.image.load('images/pub.png')
        self.pub_rect = self.pub.get_rect()

        self.safe_house = pygame.image.load('images/safe_house.png')
        self.safe_house_rect = self.safe_house.get_rect()

        pygame.init()
        self.screen = pygame.display.set_mode((self.height, self.width))
        self.screen.fill(self.background_color)

    def createTown(self,):
        #placing enemies
        self.enemy = pygame.transform.scale(self.enemy,(100,100))
        for (r,c) in self.enemy_pos:
            #Note: rect takes (x,y) x increases as we increase col and y increase as we increase row.
            #pygame.draw.rect(self.screen,self.black_color, (c*self.block_size, r*self.block_size, self.block_size,self.block_size))
            self.screen.blit(self.enemy,self.enemy_rect.move(c*self.block_size, r*self.block_size))
            

        #placing prince:
        self.prince = pygame.transform.scale(self.prince,(90,90))
        self.screen.blit(self.prince,self.prince_rect.move(3*self.block_size, 5*self.block_size))

        #placing castle
        self.castle = pygame.transform.scale(self.castle,(100,100))
        r,c = self.castle_pos 
        self.screen.blit(self.castle,self.castle_rect.move(c*self.block_size, r*self.block_size))

        #placing princess
        self.princess = pygame.transform.scale(self.princess,(90,90))
        r,c = self.princess_start
        self.screen.blit(self.princess,self.princess_rect.move(c*self.block_size, r*self.block_size))

        
        #placing restaurant
        self.restaurant = pygame.transform.scale(self.restaurant,(80,80))
        r,c = self.restaurant_pos 
        self.screen.blit(self.restaurant,self.restaurant_rect.move(c*self.block_size, r*self.block_size))

        #placing pub
        self.pub = pygame.transform.scale(self.pub,(90,90))
        r,c = self.pub_pos 
        self.screen.blit(self.pub,self.pub_rect.move(c*self.block_size, r*self.block_size))

        #placing safehouse
        self.safe_house = pygame.transform.scale(self.safe_house,(100,100))
        r,c = self.safe_house_pos 
        self.screen.blit(self.safe_house,self.safe_house_rect.move(c*self.block_size, r*self.block_size))

        

    def display(self,):
        self.createTown()
        pygame.display.set_caption('The Town')

        
    