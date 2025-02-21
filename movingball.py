from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Ellipse, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from random import randint

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=90, padding=90)
        
        label = Label(text="Welcome to the Moving Ball", font_size=60)
        start_button = Button(text="Start ", font_size=60, size_hint=(None, None), size=(900, 90))
        start_button.bind(on_press=self.start_game)

        layout.add_widget(label)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = "game"

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_pos = [Window.width / 2, Window.height / 2]
        self.ball_velocity = [0, 0]
        self.obstacles = []
        self.score = 0
        self.level = 1
        self.level_completed = False  # Prevent multiple level completions

        with self.canvas.before:
            from kivy.graphics import Color
            Color(0.53, 0.81, 0.92, 1)

        self.init_game()
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def init_game(self):
        self.canvas.clear()
        self.level_completed = False

        with self.canvas.before:
            from kivy.graphics import Color
            Color(0.53, 0.81, 0.92, 1)  

        with self.canvas:
            self.ball = Ellipse(pos=self.ball_pos, size=(50, 50))

        self.create_obstacles()

    def create_obstacles(self):
        self.obstacles.clear()
        num_obstacles = max(5, self.level * 3)
        for _ in range(num_obstacles):
            x = randint(50, Window.width - 100)
            y = randint(100, Window.height - 100)
            with self.canvas:
                obstacle = Rectangle(pos=(x, y), size=(50, 50))
                self.obstacles.append(obstacle)

    def update(self, dt):
        self.ball_pos[0] += self.ball_velocity[0]
        self.ball_pos[1] += self.ball_velocity[1]

        self.ball_pos[0] = max(0, min(Window.width - 50, self.ball_pos[0]))
        self.ball_pos[1] = max(0, min(Window.height - 50, self.ball_pos[1]))

        for obstacle in self.obstacles[:]:
            if (self.ball_pos[0] < obstacle.pos[0] + 50 and
                self.ball_pos[0] + 50 > obstacle.pos[0] and
                self.ball_pos[1] < obstacle.pos[1] + 50 and
                self.ball_pos[1] + 50 > obstacle.pos[1]):
                self.obstacles.remove(obstacle)
                self.canvas.remove(obstacle)
                self.score += 10
                break

        self.ball.pos = self.ball_pos

        if not self.obstacles and not self.level_completed:
            self.level_completed = True
            self.level_complete()

    def move_left(self):
        self.ball_velocity[0] = -5

    def move_right(self):
        self.ball_velocity[0] = 5

    def stop_movement(self):
        self.ball_velocity[0] = 0
        self.ball_velocity[1] = 0

    def move_up(self):
        self.ball_velocity[1] = 5

    def move_down(self):
        self.ball_velocity[1] = -5

    def level_complete(self):
        self.ball_velocity = [0, 0]
        self.canvas.clear()

        with self.canvas:
            from kivy.graphics import Color
            Color(1, 1, 0, 1)
            self.level_label = Label(
                text=f"Level {self.level} Complete!\nScore: {self.score}",
                font_size=100,
                pos=(Window.width / 2 - 100, Window.height / 2)
            )

        self.level += 1
        self.score += 100
        self.ball_pos = [Window.width / 2, Window.height / 2]

        Clock.schedule_once(self.restart_level, 3)

    def restart_level(self, dt):
        self.init_game()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        self.game_widget = GameWidget()

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=80)

        move_left_button = Button(text="Left", size_hint=(None, None), size=(150, 80))
        move_right_button = Button(text="Right", size_hint=(None, None), size=(150, 80))
        stop_button = Button(text="Stop", size_hint=(None, None), size=(150, 80))
        move_up_button = Button(text="Up", size_hint=(None, None), size=(150, 80))
        move_down_button = Button(text="Down", size_hint=(None, None), size=(150, 80))

        move_left_button.bind(on_press=lambda instance: self.game_widget.move_left())
        move_right_button.bind(on_press=lambda instance: self.game_widget.move_right())
        stop_button.bind(on_press=lambda instance: self.game_widget.stop_movement())
        move_up_button.bind(on_press=lambda instance: self.game_widget.move_up())
        move_down_button.bind(on_press=lambda instance: self.game_widget.move_down())

        button_layout.add_widget(move_left_button)
        button_layout.add_widget(move_right_button)
        button_layout.add_widget(move_up_button)
        button_layout.add_widget(move_down_button)
        button_layout.add_widget(stop_button)

        main_layout.add_widget(self.game_widget)
        main_layout.add_widget(button_layout)
        self.add_widget(main_layout)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(GameScreen(name="game"))
        return sm

if __name__ == '__main__':
    MyApp().run()