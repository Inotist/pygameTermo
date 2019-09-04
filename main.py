import pygame, sys
from pygame.locals import *

class Termometro:
    def __init__(self):
        self.custome = pygame.image.load("images/termo0.png")
        
    def convertir(self, grados, toUnidad):
        if toUnidad == 'F': return grados * 9/5 + 32
        elif toUnidad == 'C': return (grados - 32) * 5/9
        else: return grados
        
class Selector:
    def __init__(self, unidad="C"):
        self.__customes = []
        self.__customes.append(pygame.image.load("images/switchF.png"))
        self.__customes.append(pygame.image.load("images/switchC.png"))
        
        self.__tipoUnidad = unidad
        
    def custome(self):
        if self.__tipoUnidad == 'F': return self.__customes[0]
        else: return self.__customes[1]
        
    def change(self):
        if self.__tipoUnidad == 'F': self.__tipoUnidad = 'C'
        else: self.__tipoUnidad = 'F'
        
    def unidad(self):
        return self.__tipoUnidad

class NumberInput:
    __value = 0
    __strValue = "0"
    __position = [0,0]
    __size = [0,0]
    __pointsCount = 0
    
    def __init__(self, value=0):
        self.__font = pygame.font.SysFont("Arial", 24)
        self.value(value)
        
    def on_event(self, event):
        if event.type == KEYDOWN:
            if (event.unicode.isdigit() or (event.unicode == '.' and self.__pointsCount == 0)) and len(self.__strValue) <=7:
                if self.__strValue == "0": self.__strValue = ""
                self.__strValue += event.unicode
                if self.__strValue == '.': self.__strValue = "0"
            elif event.key == K_BACKSPACE:
                self.__strValue = self.__strValue[:-1]
                if self.__strValue == "": self.__strValue = "0"
            self.value(self.__strValue)
        
    def render(self):
        textBlock = self.__font.render(self.__strValue, True, (74,74,74))
        rect = textBlock.get_rect()
        rect.left = self.__position[0]
        rect.top = self.__position[1]
        rect.size = self.__size
        '''
        return {
            "fondo": rect,
            "texto": textBlock
            }
        '''
        return (rect, textBlock)
    
    def value(self, val=None):
        if val is None: return self.__value
        else:
            try:
                self.__value = float(val)
                self.__strValue = str(val)
            except ValueError as e: print(e)
            
        if len(self.__strValue) > 7: self.__strValue = self.__strValue[:8]
        if '.' in self.__strValue: self.__pointsCount = 1
        else: self.__pointsCount = 0
            
    def width(self, val=None):
        if val is None: return self.__size[0]
        else:
            try: self.__size[0] = int(val)
            except ValueError as e: print(e)
            
    def height(self, val=None):
        if val is None: return self.__size[1]
        else:
            try: self.__size[1] = int(val)
            except ValueError as e: print(e)
            
    def size(self, val=None):
        if val is None: return self.__size
        else:
            try: self.__size = [int(val[0]), int(val[1])]
            except (ValueError, TypeError, IndexError) as error: print(error)
            
    def posX(self, val=None):
        if val is None: return self.__position[0]
        else:
            try: self.__position[0] = int(val)
            except ValueError as e: print(e)
            
    def posY(self, val=None):
        if val is None: return self.__position[1]
        else:
            try: self.__position[1] = int(val)
            except ValueError as e: print(e)
            
    def pos(self, val=None):
        if val is None: return self.__position
        else:
            try: self.__position = [int(val[0]), int(val[1])]
            except (ValueError, TypeError, IndexError) as error: print(error)

class mainApp:
    termometro = None
    entrada = None
    selector = None
    
    def __init__(self):
        self.__screen = pygame.display.set_mode((240,349))
        pygame.display.set_caption("Termómetro")
        self.__screen.fill((244,236,203))
        
        self.termometro = Termometro()
        self.entrada = NumberInput()
        self.entrada.pos((87,48))
        self.entrada.size((110,23))
        self.selector = Selector()
        
    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.__on_close()
                    
                self.entrada.on_event(event)
                if event.type == MOUSEBUTTONDOWN:
                    self.selector.change()
                    grados = self.entrada.value()
                    nuevaUnidad = self.selector.unidad()
                    temperatura = self.termometro.convertir(grados, nuevaUnidad)
                    self.entrada.value(temperatura)
            
            # Pintamos el fondo de pantalla
            self.__screen.fill((244,236,203))
            
            # Pintamos el termómetro en su posición
            self.__screen.blit(self.termometro.custome, (41,28))
            
            # Pintamos el cuadro de texto
            text = self.entrada.render() # Obtenemos rectángulo blanco y foto de texto y lo asignamos a text
            pygame.draw.rect(self.__screen, (255,255,255), text[0]) # Creamos el rectángulo blanco con sus datos (posición y tamaño) text[0]
            self.__screen.blit(text[1], self.entrada.pos()) # Pintamos la foto del texto (text[1])
            
            # Pintamos el selector
            self.__screen.blit(self.selector.custome(), (92,128))
            
            pygame.display.flip()
                
    def __on_close(self):
        pygame.quit()
        sys.exit()
        
if __name__ == '__main__':
    pygame.init()
    app = mainApp()
    app.start()