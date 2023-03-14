class ButtonManager:
    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def draw_buttons(self, win):
        for button in self.buttons:
            button.draw(win)

    def handle_clicks(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                return button
        return None
