from aiogram import Router,F
from aiogram.types import CallbackQuery
router=Router()
@router.callback_query(F.data=="admin")
async def admin(call:CallbackQuery,config):
    if call.from_user.id not in config.admin_ids:return await call.answer("Нет доступа",show_alert=True)
    await call.message.answer("🛠 Админ-панель\n\nНа следующем этапе добавим поиск пользователей, выдачу/снятие/установку Gold, промокоды, блокировки, рассылку и логи.");await call.answer()