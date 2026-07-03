from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from menu_texts import ALL_MENU_TEXTS


class MenuInterruptMiddleware(BaseMiddleware):
    """
    Foydalanuvchi biror jarayon (FSM state) ichida bo'lsa-yu,
    lekin asosiy menyudagi tugmalardan birini bossa - bu middleware
    joriy jarayonni avtomatik tozalaydi, shunda handler matnni
    "jarayon davomidagi javob" deb emas, balki "yangi buyruq" deb qabul qiladi.
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        state: FSMContext = data.get("state")
        if state is not None and event.text in ALL_MENU_TEXTS:
            current_state = await state.get_state()
            if current_state is not None:
                await state.clear()
        return await handler(event, data)
