import logging
import customtkinter as ctk
from typing import Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


def calculate_debt_change(gdp: float, growth: float, balance: float, rate: float, debt_ratio: float) -> float:
    g_dec = (growth * 4) / 100
    r_dec = rate / 100
    debt_share = debt_ratio / 100
    absolute_debt = gdp * debt_share
    annual_interest = absolute_debt * r_dec
    annual_balance = balance * 52
    primary_balance = annual_balance + annual_interest
    primary_deficit = -primary_balance
    p_dec = primary_deficit / gdp
    delta_b = p_dec + (r_dec - g_dec) * debt_share
    return delta_b * 100


class EconomyApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("HOI4 Economy Calculator")
        self.geometry("450x460")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.entry_gdp = self._create_input_group("ВВП (млрд):", "Например: 199.4", 0, 0)
        self.entry_growth = self._create_input_group("Кварт. прирост (%):", "Например: 17", 0, 1)

        self.entry_balance = self._create_input_group("Недельный баланс (млрд):", "Например: -0.605", 1, 0)
        self.entry_rate = self._create_input_group("Ставка по долгу (%):", "Например: 5.82", 1, 1)

        self.entry_debt = self._create_input_group("Долг к ВВП (%):", "Например: 58.2", 2, 0, colspan=2)

        self.calc_button = ctk.CTkButton(
            self,
            text="Рассчитать",
            command=self._on_calculate,
            height=40,
            font=("Arial", 14, "bold")
        )
        self.calc_button.grid(row=3, column=0, columnspan=2, pady=(20, 10), padx=20, sticky="ew")

        self.result_label = ctk.CTkLabel(
            self,
            text="Ожидание данных...",
            font=("Arial", 16),
            fg_color=("gray75", "gray25"),
            corner_radius=8,
            height=60
        )
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=("Arial", 18, "bold")
        )
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(0, 10), sticky="ew")

    def _create_input_group(self, label_text: str, placeholder: str, row: int, col: int,
                            colspan: int = 1) -> ctk.CTkEntry:
        try:
            frame = ctk.CTkFrame(self, fg_color="transparent")
            frame.grid(row=row, column=col, columnspan=colspan, pady=10, padx=10, sticky="nsew")

            label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 12))
            label.pack(anchor="w", pady=(0, 5))

            entry = ctk.CTkEntry(frame, placeholder_text=placeholder, width=180, height=35)
            entry.pack(fill="x")

            return entry
        except Exception as e:
            logger.error("Error creating UI component", exc_info=True)
            raise

    def _get_float_from_entry(self, entry: ctk.CTkEntry) -> float:
        text = entry.get().strip().replace(",", ".")
        if not text:
            raise ValueError("Empty field")
        return float(text)

    def _on_calculate(self) -> None:
        try:
            gdp = self._get_float_from_entry(self.entry_gdp)
            growth = self._get_float_from_entry(self.entry_growth)
            balance = self._get_float_from_entry(self.entry_balance)
            rate = self._get_float_from_entry(self.entry_rate)
            debt_ratio = self._get_float_from_entry(self.entry_debt)

            result = calculate_debt_change(gdp, growth, balance, rate, debt_ratio)

            self.result_label.configure(
                text=f"Изменение долга за год:\n{result:+.2f} процентных пунктов",
                text_color="white"
            )

            if result < 0:
                self.status_label.configure(text="Экономика растет!", text_color="#2ecc71")
            elif result > 0:
                self.status_label.configure(text="Экономика падает!", text_color="#e74c3c")
            else:
                self.status_label.configure(text="Экономика стагнирует", text_color="#f1c40f")

        except ValueError:
            self.result_label.configure(
                text="Ошибка: Проверьте правильность\nвведенных чисел",
                text_color="#ff6b6b"
            )
            self.status_label.configure(text="")
            logger.warning("User input error (ValueError)")
        except Exception as e:
            self.result_label.configure(
                text="Критическая ошибка расчетов",
                text_color="#ff6b6b"
            )
            self.status_label.configure(text="")
            logger.error("Error during calculation", exc_info=True)
try:
    app = EconomyApp()
    app.mainloop()
except Exception as e:
    logger.critical("Application failed to start", exc_info=True)