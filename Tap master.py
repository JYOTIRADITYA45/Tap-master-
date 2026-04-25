from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from random import random

# -------- Start Screen --------
class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        title = Button(text="TAP MASTER",
                       size_hint=(0.6, 0.2),
                       pos_hint={"center_x": 0.5, "center_y": 0.7},
                       background_color=(0, 0.6, 1, 1))

        start_btn = Button(text="START",
                           size_hint=(0.4, 0.15),
                           pos_hint={"center_x": 0.5, "center_y": 0.4},
                           background_color=(0, 1, 0, 1))
        start_btn.bind(on_press=self.start_game)

        layout.add_widget(title)
        layout.add_widget(start_btn)
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = "game"


# -------- Game Screen --------
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.score = 0
        self.time_left = 30
        self.high_score = 0
        self.size_factor = 0.2

        # Target Button
        self.target = Button(text="TAP!",
                             size_hint=(self.size_factor, self.size_factor),
                             pos_hint={"x": random()*0.8, "y": random()*0.8},
                             background_color=(1, 0, 0, 1))
        self.target.bind(on_press=self.hit_target)

        # Score
        self.score_label = Button(text="Score: 0",
                                  size_hint=(0.3, 0.1),
                                  pos_hint={"x": 0, "y": 0.9},
                                  background_color=(0, 0, 0, 1))

        # Timer
        self.timer_label = Button(text="Time: 30",
                                  size_hint=(0.3, 0.1),
                                  pos_hint={"x": 0.7, "y": 0.9},
                                  background_color=(0, 0, 0, 1))

        # High Score
        self.high_label = Button(text="High: 0",
                                 size_hint=(0.4, 0.1),
                                 pos_hint={"center_x": 0.5, "y": 0.9},
                                 background_color=(0.2, 0.2, 0.2, 1))

        self.layout.add_widget(self.target)
        self.layout.add_widget(self.score_label)
        self.layout.add_widget(self.timer_label)
        self.layout.add_widget(self.high_label)

        self.add_widget(self.layout)

    def on_enter(self):
        self.score = 0
        self.time_left = 30
        self.size_factor = 0.2
        self.target.size_hint = (self.size_factor, self.size_factor)
        self.target.disabled = False
        Clock.schedule_interval(self.update_time, 1)

    def hit_target(self, instance):
        self.score += 1
        self.score_label.text = f"Score: {self.score}"

        # Increase difficulty
        if self.size_factor > 0.08:
            self.size_factor -= 0.005
            self.target.size_hint = (self.size_factor, self.size_factor)

        # Bonus time every 5 points
        if self.score % 5 == 0:
            self.time_left += 2

        # Move randomly
        self.target.pos_hint = {"x": random()*0.8, "y": random()*0.8}

    def update_time(self, dt):
        self.time_left -= 1
        self.timer_label.text = f"Time: {self.time_left}"

        if self.time_left <= 0:
            Clock.unschedule(self.update_time)

            # Update high score
            if self.score > self.high_score:
                self.high_score = self.score

            self.manager.get_screen("gameover").final_score = self.score
            self.manager.get_screen("gameover").high_score = self.high_score
            self.manager.current = "gameover"


# -------- Game Over Screen --------
class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.final_score = 0
        self.high_score = 0

        layout = FloatLayout()

        self.result = Button(text="",
                             size_hint=(0.6, 0.2),
                             pos_hint={"center_x": 0.5, "center_y": 0.6},
                             background_color=(1, 0.5, 0, 1))

        restart_btn = Button(text="PLAY AGAIN",
                             size_hint=(0.5, 0.2),
                             pos_hint={"center_x": 0.5, "center_y": 0.3},
                             background_color=(0, 1, 0, 1))
        restart_btn.bind(on_press=self.restart)

        layout.add_widget(self.result)
        layout.add_widget(restart_btn)
        self.add_widget(layout)

    def on_enter(self):
        self.result.text = f"Score: {self.final_score}\nHigh: {self.high_score}"

    def restart(self, instance):
        self.manager.current = "start"


# -------- App --------
class TapMasterApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(GameOverScreen(name="gameover"))
        return sm


if __name__ == "__main__":
    TapMasterApp().run()