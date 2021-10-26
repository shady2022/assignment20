import random
import arcade

HEIGHT = 600
WIDTH = 600

class Apple(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.apple = arcade.Sprite(':resources:images/enemies/ladybug.png', scale=0.2)
        self.apple.center_x = random.randint(20, w - 20)
        self.apple.center_y = random.randint(20, h - 20)
        
    def draw(self):
        self.apple.draw()
        
class Bomb(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.Bomb = arcade.Sprite(':resources:images/enemies/fly.png', scale=0.8)
        self.Bomb.center_x = random.randint(20, w - 20)
        self.Bomb.center_y = random.randint(20, h - 20)
        
    def draw(self):
        self.Bomb.draw()
    
class Pear(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.pear = arcade.Sprite(':resources:images/enemies/mouse.png', scale=0.5)
        self.pear.center_x = random.randint(20, w - 20)
        self.pear.center_y = random.randint(20, h - 20)
        
    def draw(self):
        self.pear.draw()

class Snake(arcade.Sprite):
    def __init__(self, w, h):
        arcade.Sprite.__init__(self)
        self.color = arcade.color.GREEN
        self.bodycolor = arcade.color.PINK_LAVENDER
        self.speed = 3
        self.width = 25
        self.height = 25
        self.center_x = w // 2
        self.center_y = h // 2
        self.r = 8
        self.change_x = 0
        self.change_y = 0
        self.score = 1
        self.body = []
        self.body.append([self.center_x, self.center_y])
        
    def draw(self):
        for i in range(len(self.body)):
            if i == 0:
                arcade.draw_circle_filled(self.body[i][0], self.body[i][1], self.r, self.color)
            else:
                arcade.draw_circle_outline(self.body[i][0], self.body[i][1], self.r, self.bodycolor)

    def move(self, appleX, appleY):
        self.change_x = 0
        self.change_y = 0
        
        if self.center_x > appleX:
            self.change_x = -1
        if self.center_x < appleX:
            self.change_x = 1        
        if self.center_x == appleX:
            self.change_x = 0
            if self.center_y > appleY:
                self.change_y = -1
            if self.center_y < appleY:
                self.change_y = 1
            if self.center_y == appleY:
                self.change_y = 0
        
        for i in range(len(self.body)-1, 0, -1):
                self.body[i][0] = self.body[i-1][0]
                self.body[i][1] = self.body[i-1][1]
                
        self.center_x += self.speed * self.change_x
        self.center_y += self.speed * self.change_y
        
        if self.body:
            self.body[0][0] += self.speed * self.change_x
            self.body[0][1] += self.speed * self.change_y

    def eat(self, mode):
        # for eat apple
        if mode == 0: 
            self.score += 1
            self.body.append([self.body[len(self.body)-1][0], self.body[len(self.body)-1][1]])
        # for eat bomb
        elif mode == 1: 
            self.score -= 1
            self.body.pop()
        # for eat pear    
        elif mode == 2: 
            self.score += 2
            self.body.append([self.body[len(self.body)-1][0], self.body[len(self.body)-1][1]])
            self.body.append([self.body[len(self.body)-1][0], self.body[len(self.body)-1][1]])
    
class Game(arcade.Window):
    def __init__(self):
        arcade.Window.__init__(self, WIDTH, HEIGHT, "Super Snake")
        arcade.set_background_color(arcade.color.ORANGE_RED)
        self.snake = Snake(WIDTH, HEIGHT)
        self.apple = Apple(WIDTH, HEIGHT)
        self.bomb = Bomb(WIDTH, HEIGHT)
        self.pear = Pear(WIDTH, HEIGHT)
        
    def on_draw(self):
        
        arcade.start_render()
        self.snake.draw()
        self.apple.draw()
        self.bomb.draw()
        self.pear.draw()
        arcade.draw_text('SCORE : ', 20, HEIGHT - 25, arcade.color.BLACK)
        arcade.draw_text(str(self.snake.score), 100, HEIGHT - 25, arcade.color.BLACK, italic=True)
        if self.snake.score == 0 or self.snake.center_x < 0 or self.snake.center_x > WIDTH or self.snake.center_y < 0 or self.snake.center_y > HEIGHT:
            arcade.draw_text('GAME OVER !', WIDTH // 2, HEIGHT // 2, bold=True, font_size=18)
            arcade.exit()
            
    def on_update(self, delta_time: float):
         
        self.snake.move(self.pear.pear.center_x, self.pear.pear.center_y)
        if arcade.check_for_collision(self.apple.apple, self.snake):
            self.snake.eat(0)
            self.apple = Apple(WIDTH, HEIGHT)
            
        if arcade.check_for_collision(self.bomb.Bomb, self.snake): 
            self.snake.eat(1)
            self.bomb = Bomb(WIDTH, HEIGHT)
            
        if arcade.check_for_collision(self.pear.pear, self.snake): 
            self.snake.eat(2)
            self.pear = Pear(WIDTH, HEIGHT) 
        
if __name__ == '__main__':
    game = Game()
    arcade.run()