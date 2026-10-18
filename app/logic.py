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
                    self.result = f"{val:.8g}".rstrip('0').rstrip('.') if '.' in f"{val:.8g}" else f"{val:.8g}"
                except Exception:
                    self.result = "Error"

        elif label in ["+", "-", "×", "÷"]:
            if "Error" in self.result:
                return
            op = "*" if label == "×" else "/" if label == "÷" else label
            self.expression = f"{self.result} {op}"
            self.new_input = True

        elif label == "=":
            if self.expression and "Error" not in self.result:
                try:
                    calc_exp = self.expression.replace("×", "*").replace("÷", "/") + f" {self.result}"
                    ans = eval(calc_exp)
                    if isinstance(ans, float):
                        res_str = f"{ans:.8g}".rstrip('0').rstrip('.') if '.' in f"{ans:.8g}" else f"{ans:.8g}"
                    else:
                        res_str = str(ans)
                    self.result = res_str
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

        else: # Angka (0-9)
            if self.new_input or self.result == "0" or "Error" in self.result:
                self.result = label
                self.new_input = False
            else:
                if len(self.result) < 14:
                    self.result += label

    def get_display(self):
        disp_exp = self.expression.replace("*", "×").replace("/", "÷")
        return disp_exp, self.result