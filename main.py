import secrets
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window

SETTINGS = {
    "Easy": (20, 3, 4, 4),
    "Medium": (50, 4, 5, 5),
    "Hard": (100, 5, 6, 6),
    "Expert": (500, 6, 7, 7),
}

class NumberChallenge(App):
    def build(self):
        self.title = "Number Challenge"
        Window.clearcolor = (0.06, 0.08, 0.14, 1)
        self.balance = 1000
        self.points = 0
        self.active = False
        self.turn = 0
        self.stake = 0

        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(9))
        root.add_widget(Label(text="[b]NUMBER CHALLENGE[/b]", markup=True,
                              font_size="25sp", size_hint_y=None, height=dp(48)))
        self.stats = Label(size_hint_y=None, height=dp(40), font_size="16sp")
        root.add_widget(self.stats)

        self.mode = Spinner(text="Easy", values=("Easy", "Medium", "Hard", "Expert"),
                            size_hint_y=None, height=dp(48))
        self.mode.bind(text=self.update_rules)
        root.add_widget(self.mode)

        self.rules = Label(size_hint_y=None, height=dp(40), font_size="14sp")
        root.add_widget(self.rules)

        self.stake_input = TextInput(hint_text="Virtual coin stake", input_filter="int",
                                     multiline=False, size_hint_y=None, height=dp(48))
        root.add_widget(self.stake_input)
        self.start_btn = Button(text="START ROUND", size_hint_y=None, height=dp(48))
        self.start_btn.bind(on_press=self.start_round)
        root.add_widget(self.start_btn)

        self.guess_input = TextInput(hint_text="Enter your guess", input_filter="int",
                                     multiline=False, disabled=True,
                                     size_hint_y=None, height=dp(48))
        root.add_widget(self.guess_input)
        self.guess_btn = Button(text="GUESS", disabled=True,
                                size_hint_y=None, height=dp(48))
        self.guess_btn.bind(on_press=self.guess)
        root.add_widget(self.guess_btn)

        self.message = Label(text="Choose a mode and stake to begin.",
                             halign="center", valign="middle", font_size="16sp")
        self.message.bind(size=lambda obj, size: setattr(obj, "text_size", size))
        root.add_widget(self.message)

        self.again_btn = Button(text="NEW ROUND", size_hint_y=None, height=dp(44))
        self.again_btn.bind(on_press=self.new_round)
        root.add_widget(self.again_btn)
        self.update_rules()
        self.refresh_stats()
        return root

    def refresh_stats(self):
        self.stats.text = f"Coins: {self.balance}     Points: {self.points}"

    def update_rules(self, *_):
        maximum, attempts, multiplier, threshold = SETTINGS[self.mode.text]
        self.rules.text = f"Range 1-{maximum} | Attempts {attempts} | Payout {multiplier}x"

    def start_round(self, *_):
        if self.active:
            self.message.text = "Finish the current round first."
            return
        try:
            stake = int(self.stake_input.text)
        except (ValueError, TypeError):
            self.message.text = "Enter a whole-number stake."
            return
        if stake <= 0 or stake > self.balance:
            self.message.text = "Stake must be positive and no greater than your balance."
            return

        self.maximum, self.attempts, self.multiplier, self.threshold = SETTINGS[self.mode.text]
        self.stake = stake
        self.balance -= stake
        self.secret = secrets.randbelow(self.maximum) + 1
        self.turn = 0
        self.active = True
        self.mode.disabled = True
        self.stake_input.disabled = True
        self.start_btn.disabled = True
        self.guess_input.disabled = False
        self.guess_btn.disabled = False
        self.guess_input.text = ""
        self.message.text = f"{self.mode.text}: guess 1-{self.maximum}. You have {self.attempts} attempts."
        self.refresh_stats()

    def guess(self, *_):
        if not self.active:
            return
        try:
            value = int(self.guess_input.text)
        except (ValueError, TypeError):
            self.message.text = "Enter a whole-number guess."
            return
        if not 1 <= value <= self.maximum:
            self.message.text = f"Choose a number from 1 to {self.maximum}."
            return

        self.turn += 1
        self.guess_input.text = ""
        if value == self.secret:
            payout = self.stake * self.multiplier
            profit = payout - self.stake
            self.balance += payout
            self.points += profit
            self.message.text = (f"YOU WIN!\nSecret: {self.secret}\nPayout: {payout} coins "
                                 f"({self.multiplier}x)\nNet profit/points: +{profit}")
            self.finish()
            return

        message = "Too low! Try higher." if value < self.secret else "Too high! Try lower."
        difference = abs(self.secret - value)
        if difference <= self.threshold:
            message += "\n🔥 Very close!"
        elif difference <= 10:
            message += "\n🙂 Getting closer!"

        remaining = self.attempts - self.turn
        if remaining <= 0:
            message += f"\n\nGAME OVER! Secret: {self.secret}\nStake lost: {self.stake}"
            self.message.text = message
            self.finish()
        else:
            self.message.text = f"{message}\nAttempts remaining: {remaining}"

    def finish(self):
        self.active = False
        self.mode.disabled = False
        self.stake_input.disabled = False
        self.start_btn.disabled = False
        self.guess_input.disabled = True
        self.guess_btn.disabled = True
        self.refresh_stats()
        if self.balance <= 0:
            self.message.text += "\nNo coins left. Restart the app to reset."

    def new_round(self, *_):
        if self.active:
            self.message.text = f"Round abandoned. Stake lost: {self.stake} coins."
            self.finish()
        self.stake_input.text = ""
        self.guess_input.text = ""
        self.refresh_stats()

if __name__ == "__main__":
    NumberChallenge().run()
