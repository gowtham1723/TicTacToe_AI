from tkinter import Tk, Button
from copy import deepcopy
from tkinter.messagebox import showinfo, askyesno


class Game:

    def __init__(self, other=None):
        self.player = 'X'
        self.bot = 'O'
        self.empty = '_____'
        self.size = 3
        self.won_player = None
        self.starting_player=None
        self.fields = {}
        for y in range(self.size):
            for x in range(self.size):
                self.fields[x, y] = self.empty
        # copy constructor
        if other:
            self.__dict__ = deepcopy(other.__dict__)

    def make_move(self, x, y):
        game = Game(self)
        game.fields[x, y] = game.player
        (game.player, game.bot) = (game.bot, game.player)
        return game

    def bot_firstmove(self,x,y):
        game=Game(self)
        game.fields[x,y]=game.bot
        (game.bot,game.player)=(game.player,game.bot)
        return game

    def __minimax(self, player):
        if self.won():
            if player:
                return -1, None
            else:
                return +1, None
        elif self.tied():
            return 0, None
        elif player:
            best_move = (-2, None)
            for x, y in self.fields:
                if self.fields[x, y] == self.empty:
                    value = self.make_move(x, y).__minimax(not player)[0]
                    if value > best_move[0]:
                        best_move = (value, (x, y))
            return best_move
        else:
            best_move = (+2, None)
            for x, y in self.fields:
                if self.fields[x, y] == self.empty:
                    value = self.make_move(x, y).__minimax(not player)[0]
                    if value < best_move[0]:
                        best_move = (value, (x, y))
            return best_move

    def best_move(self):
        return self.__minimax(True)[1]

    def tied(self):
        for (x, y) in self.fields:
            if self.fields[x, y] == self.empty:
                return False
        return True

    def won(self):
        # horizontal
        for y in range(self.size):
            winning = []
            for x in range(self.size):
                if self.fields[x, y] == self.bot:
                    winning.append((x, y))
            if len(winning) == self.size:
                self.won_player = self.bot
                return winning

        # vertical
        for x in range(self.size):
            winning = []
            for y in range(self.size):
                if self.fields[x, y] == self.bot:
                    winning.append((x, y))
            if len(winning) == self.size:
                self.won_player = self.bot
                return winning

        # diagonal
        winning = []
        for y in range(self.size):
            x = y
            if self.fields[x, y] == self.bot:
                winning.append((x, y))
        if len(winning) == self.size:
            self.won_player = self.bot
            return winning

        # other diagonal
        winning = []
        for y in range(self.size):
            x = self.size - 1 - y
            if self.fields[x, y] == self.bot:
                winning.append((x, y))
        if len(winning) == self.size:
            self.won_player = self.bot
            return winning

        # default
        return None

    def __str__(self):
        string = ''
        for y in range(self.size):
            for x in range(self.size):
                string += self.fields[x, y]
            string += "\n"
        return string


class GUI:

    def __init__(self):
        self.app = Tk()
        self.app.title('TicTacToe')
        self.app.resizable(width=True, height=True)
        self.game = Game()
        self.buttons = {}
        first = askyesno("Start", "Do you want to play as X?")
        if first:
            self.game.player = 'X'
            self.game.bot = 'O'
            self.game.starting_player='player'
        else:
            self.game.player = 'O'
            self.game.bot = 'X'
            self.game.starting_player = 'bot'
        handler = lambda: self.start()
        button = Button(self.app, text='Start game', command=handler)
        button.grid(row=self.game.size + 1, column=0, columnspan=self.game.size, sticky="WE")
        for x, y in self.game.fields:
            handler = lambda x=x, y=y: self.make_move(x, y)
            button = Button(self.app, command=handler, width=10, height=10)
            button.grid(row=y, column=x)
            self.buttons[x, y] = button

        handler = lambda: self.reset()
        button = Button(self.app, text='Reset game', command=handler)
        button.grid(row=self.game.size + 2, column=0, columnspan=self.game.size, sticky="WE")
        self.update()

    def reset(self):
        self.game = Game()
        self.update()
        first = askyesno("Start", "Do you want to play as X? ")
        if first:
            self.game.player = 'X'
            self.game.bot = 'O'
            self.game.starting_player = 'player'
            for x, y in self.game.fields:
                handler = lambda x=x, y=y: self.make_move(x, y)
                button = Button(self.app, command=handler, width=10, height=10)
                button.grid(row=y, column=x)
                self.buttons[x, y] = button
        else:
            self.game.player = 'O'
            self.game.bot = 'X'
            self.game.starting_player = 'bot'

    def start(self):
        self.game = Game()
        make_move = self.game.best_move()
        self.game = self.game.make_move(*make_move)
        self.update()

    def make_move(self, x, y):
        self.app.config(cursor="watch")
        self.app.update()
        self.game = self.game.make_move(x, y)
        self.update()
        make_move = self.game.best_move()
        if make_move:
            self.game = self.game.make_move(*make_move)
            self.update()
        self.app.config(cursor="")


    def update(self):
        for (x, y) in self.game.fields:
            text = self.game.fields[x, y]
            self.buttons[x, y]['text'] = text
            self.buttons[x, y]['disabledforeground'] = 'black'
            if text == self.game.empty:
                self.buttons[x, y]['state'] = 'normal'
            else:
                self.buttons[x, y]['state'] = 'disabled'

        winning = self.game.won()
        tied = self.game.tied()
        if winning:
            for x, y in winning:
                self.buttons[x, y]['disabledforeground'] = 'red'
            for x, y in self.buttons:
                self.buttons[x, y]['state'] = 'disabled'
            if self.game.won_player == 'X':
                if self.game.starting_player=='player':
                    showinfo("Match over", "You Won")
                else:
                    showinfo("Match over", "Bot won")
            else:
                if self.game.starting_player=='player':
                    showinfo("Match over", "Bot Won")
                else:
                    showinfo("Match over", "You won")

        if tied:
            showinfo("Match Over", "Match tied")
        for (x, y) in self.game.fields:
            self.buttons[x, y].update()

    def mainloop(self):
        self.app.mainloop()


if __name__ == '__main__':
    GUI().mainloop()
