import math

class CalculatorLogic:
    def __init__(self):
        self.expression = ""
        self.result = "0"
        self.new_input = True
        self.history = []

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

        elif label in ["sin", "cos", "tan", "log", "ln", "√", "!"]:
            if "Error" not in self.result:
                try:
                    val = float(self.result)
                    if label == "sin": res = math.sin(math.radians(val))
                    elif label == "cos": res = math.cos(math.radians(val))
                    elif label == "tan": res = math.tan(math.radians(val))
                    elif label == "log": res = math.log10(val)
                    elif label == "ln": res = math.log(val)
                    elif label == "√": res = math.sqrt(val)
                    elif label == "!": res = math.factorial(int(val))
                    
                    formatted = f"{res:.8g}".rstrip('0').rstrip('.') if '.' in f"{res:.8g}" else f"{res:.8g}"
                    self.history.append({"exp": f"{label}({self.result})", "res": formatted})
                    self.result = formatted
                    self.new_input = True
                except Exception:
                    self.result = "Error"

        elif label in ["π", "e"]:
            val = str(math.pi) if label == "π" else str(math.e)
            self.result = val[:10]
            self.new_input = False

        elif label in ["+", "-", "×", "÷", "^", "(", ")"]:
            if "Error" in self.result: return
            op = "*" if label == "×" else "/" if label == "÷" else "**" if label == "^" else label
            if label in ["(", ")"]:
                if self.result == "0" or self.new_input:
                    self.expression += f" {op} "
                else:
                    self.expression += f"{self.result} {op} "
            else:
                self.expression = f"{self.result} {op} "
            self.new_input = True

        elif label == "=":
            if self.expression and "Error" not in self.result:
                try:
                    calc_exp = self.expression.replace("×", "*").replace("÷", "/") + f" {self.result}"
                    ans = eval(calc_exp)
                    formatted = f"{ans:.8g}".rstrip('0').rstrip('.') if '.' in f"{ans:.8g}" else f"{ans:.8g}"
                    self.history.append({"exp": calc_exp, "res": formatted})
                    self.result = formatted
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

    def convert_units(self, category: str, from_u: str, to_u: str, val_str: str) -> str:
        try:
            val = float(val_str)
            if category == "Suhu":
                if "Celsius" in from_u: c = val
                elif "Fahrenheit" in from_u: c = (val - 32) * 5/9
                elif "Kelvin" in from_u: c = val - 273.15
                
                if "Celsius" in to_u: res = c
                elif "Fahrenheit" in to_u: res = (c * 9/5) + 32
                elif "Kelvin" in to_u: res = c + 273.15

            elif category == "Panjang":
                to_m = {"Meter (m)": 1, "Kilometer (km)": 1000, "Centimeter (cm)": 0.01, "Millimeter (mm)": 0.001, "Inch (in)": 0.0254, "Feet (ft)": 0.3048}
                m = val * to_m.get(from_u, 1)
                res = m / to_m.get(to_u, 1)

            elif category == "Massa / Berat":
                to_g = {"Kilogram (kg)": 1000, "Gram (g)": 1, "Milligram (mg)": 0.001, "Pound (lbs)": 453.592}
                g = val * to_g.get(from_u, 1)
                res = g / to_g.get(to_u, 1)

            elif category == "Waktu":
                to_s = {"Detik (s)": 1, "Menit (min)": 60, "Jam (h)": 3600, "Hari (d)": 86400}
                s = val * to_s.get(from_u, 1)
                res = s / to_s.get(to_u, 1)

            elif category == "Mata Uang":
                to_idr = {"Rupiah (IDR)": 1, "US Dollar (USD)": 15600, "Euro (EUR)": 16800, "Yen (JPY)": 102, "SGD (S$)": 11800}
                idr = val * to_idr.get(from_u, 1)
                res = idr / to_idr.get(to_u, 1)

            return f"{res:.6g}"
        except Exception:
            return "Error Input"

    def clear_history(self):
        self.history.clear()

    def get_display(self):
        disp_exp = self.expression.replace("*", "×").replace("/", "÷")
        return disp_exp, self.result