from aiogram.fsm.state import State, StatesGroup

class CalculatorStates(StatesGroup):
    choosing_product = State()
    choosing_niche = State()
    choosing_integration = State()
    entering_contact = State()

class OrderStates(StatesGroup):
    entering_details = State()
    entering_contact = State()

class SupportAuditStates(StatesGroup):
    entering_bot_link = State()
    entering_contact = State()
