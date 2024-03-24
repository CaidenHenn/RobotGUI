from textual.app import App, ComposeResult
from textual.events import Print
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Header, Button, Digits
import serial


class Name(Widget):
    who = reactive("Serial", layout=True)

    def render(self) -> str:
        return f"{self.who}"


class ReturnValues(Widget):

    val = reactive("datastring", recompose=True)

    def __init__(
            self,
            *children: Widget,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
            disabled: bool = False,
    ):
        super().__init__(children, name, id, classes, disabled)
        self.value = None

    ser = serial.Serial('COM14', 9600)
    strang = [0]
    if ser.in_waiting > 0:
        read_serial = ser.readline()
        strang[0] = str(int(ser.readline(), 16))
        print(strang[0])
        print(read_serial)
        def on_print(self, event: Print, read_serial=None, strang=None):
            self.value = f"{strang[0]},{read_serial}"



    def compose(self) -> ComposeResult:
        yield Digits(self.value)



    """def watch_values(self, new_val: str) -> None:
        ser = serial.Serial('COM14', 9600)
        s = [0]
        while True:
            if ser.in_waiting > 0:  # Check if there's data available to read
                read_serial = ser.readline().strip()
                try:
                    value = int(read_serial, 16)
                    self.query_one(Digits).val = str(value)
                except ValueError:
                    print("Invalid hexadecimal value:", read_serial)"""


class RobotGUI(App):
    CSS_PATH = "robot.tcss"
    BINDINGS = [("left", "left"), ("right", "right"), ("up", "up"), ("down", "down")]
    ser = serial.Serial('COM14', 9600)

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header("RobotApp")
        yield Button("Start", id="start")
        yield Name()

        yield ReturnValues(id ="bottom-right")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        SerialObj = serial.Serial('COM14', 9600)

        if event.button.id == "start":
            self.query_one(Name).who = SerialObj


    """ser = serial.Serial('COM14', 9600)
    s = [0]
    while True:
        read_serial = ser.readline()
        s[0] = str(int(ser.readline(), 16))"""

    """"def update_val_from_serial(self) -> None:
        if self.serial_obj and self.serial_obj.in_waiting > 0:
            serial_data = self.serial_obj.readline().strip().decode()
            self.query_one(ReturnValues).val = serial_data"""




if __name__ == "__main__":
    app = RobotGUI()
    app.run()
