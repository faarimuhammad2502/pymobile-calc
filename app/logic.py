class CalculatorLogic:
    def __init__(self):
        self.expression = ""
        self.result = "0"
        self.new_input = True

    def process_input(self, label: str):
        if label == "C":
            self.expression = ""
            self.result = "0"
            self.new_input = True
        elif label == "DEL":
            if not self.new_input and self.result != "0":
                self.result = self.result[:-1]
                if self.result == "" or self.result == "-":
                    self.result = "0"
                    self.new_input = True
        elif label == "+/-":
            if self.result != "0" and "Error" not in self.result:
                if self.result.startswith("-"):
                    self.result = self.result[1:]
                else:
                    self.result = "-" + self.result
        elif label == "%":
            if "Error" not in self.result:
                try:
                    val = float(self.result) / 100
                    self.result = str(val).rstrip('0').rstrip('.') if '.' in str(val) else str(val)
                except:
                    self.result = "Error"
        elif label in ["+", "-", "×", "÷"]:
            op = "*" if label == "×" else "/" if label == "÷" else label
            self.expression = f"{self.result} {op}"
            self.new_input = True
        elif label == "=":
            if self.expression:
                try:
                    calc_exp = self.expression.replace("×", "*").replace("÷", "/") + f" {self.result}"
                    ans = eval(calc_exp)
                    self.result = str(round(ans, 8)).rstrip('0').rstrip('.') if '.' in str(ans) else str(ans)
                    self.expression = ""
                    self.new_input = True
                except ZeroDivisionError:
                    self.result = "Error"
                except Exception:
                    self.result = "Error"
        elif label == ".":
            if self.new_input:
                self.result = "0."
                self.new_input = False
            elif "." not in self.result:
                self.result += "."
        else: # Angka biasa
            if self.new_input or self.result == "0":
                self.result = label
                self.new_input = False
            else:
                if len(self.result) < 15: # Membatasi panjang digit
                    self.result += label

    def get_display(self):
        disp_exp = self.expression.replace("*", "×").replace("/", "÷")
        return disp_exp, self.result