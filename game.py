from tkinter import Tk, Canvas, PhotoImage, Button, Label
from time import time

class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title('Mr. Stick Man Races for the Exit')
        self.tk.resizable(False, False)
        self.tk.wm_attributes('-topmost', 1)

        self.redraw()
        
        self.canvas = Canvas(self.tk, width=500, height=500)
        self.canvas.pack()

        self.redraw()
        
        screenheight = self.tk.winfo_screenheight()
        screenwidth = self.tk.winfo_screenwidth()
        self.x_calc = int(screenwidth / 2 - 250)
        self.y_calc = int(screenheight / 2 - 250)

        self.tk.geometry('+%i+%i' % (self.x_calc, self.y_calc))
        self.redraw()

        self.bg = PhotoImage(file='/home/shark/Minh/Mr_Stickman/B.gif')

        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x * 100, y * 100,
                                         image=self.bg, anchor='nw')
                self.redraw()

        self.sprites = []
        self.running = True

    def dialog(self):
        self.to_return = False

        def true():
            self.to_return = True
            self.dtk.quit()

        def false():
            self.to_return = False
            self.dtk.quit()
            
        self.dtk = Tk()
        self.dtk.title('Are you sure?')
        self.dtk.resizable(False, False)
        self.dtk.wm_attributes('-topmost', 1)

        self.dtk.geometry('250x100+{}+{}'.format(self.x_calc + 125, \
                                                 self.y_calc + 200))

        prompt = Label(self.dtk, text='Are you sure you want to exit?', \
                       font=('Courier', 10)).place(x=5, y=10)

        yes_btn = Button(self.dtk, bg='#00ff00', fg='#ff0000', \
                         text='Yes', command=true).place(x=65, y=50)
        no_btn = Button(self.dtk, bg='#ff0000', fg='#00ff00', \
                        text='No', command=false).place(x=135, y=50)

        self.redraw()
        self.dtk.mainloop()
        self.dtk.destroy()
        
        return self.to_return

    def help(self):
        self.htk = Tk()
        self.htk.title('Mr. Stickman\'s Help Window')
        self.htk.resizable(False, False)
        self.htk.wm_attributes('-topmost', 1)

        self.htk.geometry('265x120+{}+{}'.format(self.x_calc + 125, \
                                                 self.y_calc + 170))

        text = \
            u'Press \u2190 or \u2191 to move.\n' + \
            u'Press \u2192 to jump.\n' + \
            'Press Q to exit.\n' + \
            'Press H to display this window.\n'
        
        directions = Label(self.htk, text=text, font=('Courier', 10))
        directions.place(x=5, y=5)

        ok_btn = Button(self.htk, text='OK', command=self.htk.quit)
        ok_btn.place(x=110, y=80)

        self.redraw()
        self.htk.mainloop()
        self.htk.destroy()

    def redraw(self):
        self.tk.update_idletasks()
        self.tk.update()

    def mainloop(self):
        def forloop():
            for sprite in self.sprites:
                if self.running:
                    sprite.move()
                    self.redraw()

            self.timer = self.tk.after(10, forloop)

        self.timer = self.tk.after(10, forloop)

        self.tk.mainloop()
        self.tk.destroy()

class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Sprite:
    def __init__(self, game):
        self.game = game

        self.game.sprites.append(self)
        
        self.endgame = False
        self.coordinates = None

        self.game.redraw()

    def move(self):
        pass

    def coords(self):
        return self.coordinates
    
    def within_x(self, main, other):
        return (main.x1 > other.x1 and main.x2 < other.x2) or \
               (main.x2 > other.x1 and main.x2 < other.x2) or \
               (other.x1 > main.x1 and other.x1 < main.x2) or \
               (other.x2 > main.x1 and other.x2 < main.x1)

    def within_y(self, main, other):
        return (main.y1 > other.y1 and main.y2 < other.y2) or \
               (main.y2 > other.y1 and main.y2 < other.y2) or \
               (other.y1 > main.y1 and other.y1 < main.y2) or \
               (other.y2 > main.y1 and other.y2 < main.y1)

    def collided_left(self, main, other):
        if self.within_y(main, other):
            if main.x1 <= other.x2 and main.x1 >= other.x1:
                return True

        return False

    def collided_right(self, main, other):
        if self.within_y(main, other):
            if main.x2 <= other.x1 and main.x2 >= other.x2:
                return True

        return False
        
    def collided_top(self, main, other):
        if self.within_x(main, other):
            if main.y1 <= other.y2 and main.y1 >= other.y1:
                return True

        return False
    
    def collided_bottom(self, main, other, y):
        if self.within_x(main, other):
            y_calc = main.y2 + y
            if y_calc <= other.y1 and y_calc >= other.y2:
                return True

        return False

class Platform(Sprite):
    def __init__(self, game, x, y, gifimage):
        Sprite.__init__(self, game)
        self.gifimage = PhotoImage(file=gifimage)
        self.image = self.game.canvas.create_image(x, y, image=self.gifimage, \
                                                   anchor='nw')
        self.coordinates = Coords(x, y, \
                                  x + self.gifimage.width(), \
                                  self.gifimage.height())

class Stickfigure(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)

        self.l_images = [
            PhotoImage(file='/home/shark/Minh/Mr_Stickman/L1.gif'),
            PhotoImage(file='/home/shark/Minh/Mr_Stickman/L2.gif'),
            PhotoImage(file='/home/shark/Minh/Mr_Stickman/L3.gif'),
            PhotoImage(file='/home/shark/Minh/Mr_Stickman/L4.gif')
        ]

        self.r_images = [
            PhotoImage(file='/home/shark/Minh/Mr_Stickman/R1.gif'),
            PhotoImage(file='/home/shark/Minh/Mr_Stickman/R2.gif'),
            PhotoImage(file='/home/shark/Minh/Mr_Stickman/R3.gif'),
            PhotoImage(file='/home/shark/Minh/Mr_Stickman/R4.gif')
        ]

        self.image = self.game.canvas.create_image(10, 450, \
                                                   image=self.r_images[0], \
                                                   anchor='nw')

        self.x = 0
        self.y = 0
        self.cur_img = 0
        self.img_step = 1
        self.jump_count = 0
        self.last_time = time()
        self.coordinates = Coords()

        self.game.canvas.bind_all('<Key>', self.service_keys)

    def service_keys(self, event):
        if event.keysym == 'Left' and self.y == 0:
            self.x = -2

        if event.keysym == 'Right' and self.y == 0:
            self.x = 2

        if event.keysym == 'Up' and self.y == 0:
            self.y = -4
            self.jump_count = 0

        if event.keysym == 'q':
            if self.game.dialog():
                self.game.tk.after_cancel(self.game.timer)
                self.game.running = False
                self.game.tk.quit()

        if event.keysym == 'h':
            self.game.help()

    def jumping(self):
        return self.y < 0

    def falling(self):
        return self.y > 0

    def moving(self):
        return self.x != 0

    def moving_left(self):
        return self.x < 0

    def moving_right(self):
        return self.x > 0

    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 27
        return self.coordinates
    
    def animate(self):
        if self.moving() and not self.jumping() and \
           (time() - self.last_time > 0.15):
            self.last_time = time()
            self.cur_img += self.img_step
            
            if self.cur_img >= 2:
                self.img_step = -1

            if self.cur_img <= 0:
                self.img_step = 1

        if self.moving_left():
            if self.jumping():
                self.game.canvas.itemconfig(self.image, \
                                            image=self.l_images[2])

            else:
                self.game.canvas.itemconfig(self.image, \
                                            image=self.l_images[self.cur_img])

        elif self.moving_right():
            if self.jumping():
                self.game.canvas.itemconfig(self.image, \
                                            image=self.r_images[2])

            else:
                self.game.canvas.itemconfig(self.image, \
                                            image=self.r_images[self.cur_img])

    def move(self):
        self.animate()

        if self.jumping():
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4

        if self.falling():
            self.jump_count -= 1

        co = self.coords()
        
        left = False
        right = False
        top = False
        bottom = False
        falling = False

        if self.falling() and co.y2 >= 500:
            self.y = 0
            bottom = True

        elif self.jumping() and co.y1 <= 0:
            self.y = 0
            top = True

        if self.moving_right() and co.x2 >= 500:
            self.x = 0
            right = True

        elif self.moving_left() and co.x1 <= 0:
            self.x = 0
            left = True

        for sprite in self.game.sprites:
            if sprite == self:
                continue

            sprite_co = sprite.coords()
            
            if not top and self.jumping() and \
               self.collided_top(co, sprite_co):
                self.y = -self.y
                top = True

            if not bottom and self.falling() and \
               self.collided_bottom(co, sprite_co, self.y):
                self.y = sprite_co.y1 - co.y2

                if self.y < 0:
                    self.y = 0
                    bottom = True
                    top = True

            if not bottom and not falling and self.y == 0 and \
               co.y2 < 500 and self.collided_bottom(co, sprite_co, 1):
                falling = True

            if not left and self.moving_left() and \
               self.collided_left(co, sprite_co):
                self.x = 0
                left = True

            if not right and self.moving_right() and \
               self.collided_right(co, sprite_co):
                self.x = 0
                right = True

        if not falling and not bottom and \
           self.y == 0 and co.y2 < 500:
            self.y = 4

        self.game.canvas.move(self.image, self.x, self.y)

g = Game()

platform1 = Platform(g, 0, 480, '/home/shark/Minh/Mr_Stickman/P3.gif')
platform2 = Platform(g, 150, 440,  '/home/shark/Minh/Mr_Stickman/P3.gif')
platform3 = Platform(g, 300, 400, '/home/shark/Minh/Mr_Stickman/P3.gif')
platform4 = Platform(g, 300, 160, '/home/shark/Minh/Mr_Stickman/P3.gif')
platform5 = Platform(g, 175, 350, '/home/shark/Minh/Mr_Stickman/P2.gif')
platform6 = Platform(g, 50, 300, '/home/shark/Minh/Mr_Stickman/P2.gif')
platform7 = Platform(g, 170, 120, '/home/shark/Minh/Mr_Stickman/P2.gif')
platform8 = Platform(g, 45, 60, '/home/shark/Minh/Mr_Stickman/P2.gif')
platform9 = Platform(g, 170, 250, '/home/shark/Minh/Mr_Stickman/P1.gif')
platform10 = Platform(g, 230, 200, '/home/shark/Minh/Mr_Stickman/P1.gif')

sf = Stickfigure(g)


g.mainloop()
