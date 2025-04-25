from aiogram.fsm.state import StatesGroup, State


class SearchStates(StatesGroup):
    waiting_for_query = State() # ⁡⁣⁢⁣Обрабатываем FMS⁡
