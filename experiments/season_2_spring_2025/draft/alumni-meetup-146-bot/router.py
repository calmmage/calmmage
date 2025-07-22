from _app import App, City, Registration
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from botspot import commands_menu as bot_commands_menu
from botspot.utils import send_safe

router = Router()
app = App()


class RegistrationForm(StatesGroup):
    city = State()
    full_name = State()
    graduation_info = State()


@bot_commands_menu.add_command("start", "Start the bot")
@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=city.value) for city in City]],
        resize_keyboard=True
    )
    
    await send_safe(
        message.chat.id,
        "Привет! Это бот для регистрации на встречу выпускников школы 146.\n"
        "Выберите город, где планируете посетить встречу:",
        reply_markup=keyboard
    )
    await state.set_state(RegistrationForm.city)


@router.message(RegistrationForm.city, F.text.in_([city.value for city in City]))
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await send_safe(
        message.chat.id,
        "Введите ваши ФИО:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(RegistrationForm.full_name)


@router.message(RegistrationForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await send_safe(
        message.chat.id,
        "Введите год выпуска и букву класса (например: 2015 А):"
    )
    await state.set_state(RegistrationForm.graduation_info)


@router.message(RegistrationForm.graduation_info)
async def process_graduation(message: Message, state: FSMContext):
    try:
        year, letter = message.text.split()
        year = int(year)
        
        data = await state.get_data()
        registration = Registration(
            full_name=data['full_name'],
            graduation_year=year,
            class_letter=letter.upper(),
            city=data['city']
        )
        
        app.registrations[message.from_user.id] = registration
        
        await send_safe(
            message.chat.id,
            "Спасибо за регистрацию! Инструкция по оплате взноса будет отправлена позже."
        )
        await state.clear()
        
    except (ValueError, IndexError):
        await send_safe(
            message.chat.id,
            "Пожалуйста, введите год и букву класса в формате: 2015 А"
        )


@bot_commands_menu.add_command("help", "Show this help message")
@router.message(Command("help"))
async def help_handler(message: Message):
    await send_safe(
        message.chat.id,
        f"Это бот для регистрации на встречу выпускников школы 146.\n"
        f"Используйте /start для начала регистрации."
    )
