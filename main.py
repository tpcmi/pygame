import pygame
from pygame.locals import *
import time
import json

class Text:

    def __init__(self, text, pos, fontsize, background=None, fontcolor=Color('black')):
        self.text = text
        self.pos = pos
        self.fontname = None
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.background = background
        self.set_font()
        self.render()

    def set_font(self):
        self.font = pygame.font.Font(self.fontname, self.fontsize)
  
    def render(self):
        self.img = self.font.render(
            self.text, True, self.fontcolor, self.background)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        App.screen.blit(self.img, self.rect)

class App:

    def __init__(self, file):
        pygame.init()
        self.file = file
        self.time = 60
        self.bgcolor = Color('red')
        self.start = False
        self.t1 = 0
        self.sentenceId = 0
        self.rightnums = 0
        self.clicknums = 1
        self.text = 'Input here'
        App.screen = pygame.display.set_mode((1000, 700))
        App.running = True
        App.startText = Text("Press 's' to start", pos=(325, 250), fontsize=72)
        App.quitText = Text("'ESC' to quit", pos=(30, 10), fontsize=25)

    def timer(self, startTime):

        t2 = time.time()
        if t2 - startTime <= 60:
            self.time = 60 - int(t2 - startTime)
        else:
            self.time = 0

    def multiLine(self, pos, font, text, max_width=900):
        x, y = pos
        space = font.size(' ')[0]
        for word in text:
            word_surface = font.render(word, True, Color('black'))
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height

            App.screen.blit(word_surface, (x, y))
            x += word_width + space

    def sentences(self):
        # choose sentence if time is enough
        if self.time > 0 and self.rightnums == len(self.file[str(self.sentenceId)].split(' ')):
            self.sentenceId = (self.sentenceId + 1) % 3
            self.text = 'Input here'

        # change line
        pos = (150, 70)
        font = pygame.font.Font(None, 45)
        words = self.file[str(self.sentenceId)].split(' ')
        self.multiLine(pos, font, words)

    def wordsCheck(self):
        temp1 = self.text.split(' ')
        temp2 = self.file[str(self.sentenceId)].split(' ')
        num = 0
        if (len(temp1) <= len(temp2)):
            for i in range(len(temp1)):

                if temp1[i] == temp2[i]:
                    num += 1
            for i in range(self.sentenceId):
            	num += len(self.file[str(i)].split(' '))
        self.rightnums = num

    def backgroudcolor(self):
        d = {
            0: Color(255, 51, 0),
            # 1:Color(255,51,0),
            1: Color(255, 102, 0),
            2: Color(255, 255, 0),
            3: Color(153, 255, 0),
            4: Color(102, 255, 0),
            5: Color(87, 196, 60)
        }
        now = time.time()
        if int(self.clicknums / (now - self.t1))>5: 
            self.bgcolor = d[5]
        else:
            self.bgcolor = d[int(self.clicknums / (now - self.t1))]

    def run(self):
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False
                elif event.type == KEYDOWN:
                    if not self.start and event.key == K_s:
                        self.start = True
                        self.t1 = time.time()

                    elif self.start and event.key == K_ESCAPE:
                        self.start = False
                        self.time = 60
                        self.text = 'Input here'
                        self.sentenceId = 0
                        self.rightnums = 0
                        self.clicknums = 0
                        self.bgcolor = Color('red')

                    elif self.start and event.key == K_BACKSPACE and len(self.text) > 0:
                        self.text = self.text[:-1]
                    elif self.start:

                        self.clicknums += 1
                        self.text += event.unicode
                        self.backgroudcolor()

            App.screen.fill(Color('gray'))
            if self.start:
                self.timer(self.t1)
                App.screen.fill(self.bgcolor)
                App.timeText = Text('Time left: ' + str(self.time) + 's',
                                    pos=(400, 10), fontsize=40, fontcolor=Color('gold'))
                App.timeText.draw()
                App.quitText.draw()
                self.wordsCheck()
                App.rightText = Text(
                    "Right nums: " + str(self.rightnums), pos=(800, 10), fontsize=25)
                App.rightText.draw()
                self.sentences()
                pos = (150, 350)
                font = pygame.font.Font(None, 45)
                words = self.text.split(' ')
                self.multiLine(pos, font, words)

            if not self.start:
                App.startText.draw()

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    with open('words.json', 'r') as f:
        words = json.load(f)
        App(words).run()
