from aiogram.fsm.state import StatesGroup, State


class SearchStates(StatesGroup):
    waiting_for_query = State() # Обрабатываем FSM для юзеров


class AdminStates(StatesGroup):
    waiting_for_post_id = State() # Обрабатываем FSM для админов


class EditPostStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_rating = State()


class CommentStates(StatesGroup):
    waiting_for_comment = State()
