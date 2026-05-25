from html import escape

from services.cart import cart_lines, cart_total


WELCOME_TEXT = (
    "🍔 Добро пожаловать в DIGAR-DOG!\n\n"
    "🔥 Самые вкусные:\n"
    "🌯 Шаурма\n"
    "🌭 Хот-доги\n"
    "🍟 Картошка фри\n"
    "🥤 Напитки\n\n"
    "👇 Выберите категорию ниже"
)


def order_summary(cart: dict[str, int]) -> str:
    lines = "\n".join(cart_lines(cart))
    return f"📦 Ваш заказ:\n\n{lines}\n\n💰 Сумма: {cart_total(cart)} смн"


def admin_order_text(order: dict) -> str:
    address = order.get("address") or "Самовывоз"
    username = f"@{order['username']}" if order.get("username") else "без username"
    return (
        f"🆔 Номер заказа: {escape(order['order_code'])}\n"
        f"👤 Клиент: {escape(username)}\n"
        f"🧾 user_id: {order['user_id']}\n\n"
        f"📦 Товары:\n{escape(order['items_text'])}\n\n"
        f"💰 Сумма: {order['total']} смн\n"
        f"🚚 Тип: {escape(order['fulfillment'])}\n"
        f"💳 Оплата: {escape(order['payment_method'])}\n"
        f"📍 Адрес: {escape(address)}"
    )


def confirmed_text(order: dict) -> str:
    tail = "📞 Ждите звонка курьера." if order["fulfillment"] == "Доставка" else "🛍 Мы сообщим вам,\nкогда заказ будет готов."
    return (
        "✅ Заказ подтверждён!\n\n"
        f"🆔 Номер заказа: {order['order_code']}\n\n"
        f"📦 Ваш заказ:\n{order['items_text']}\n\n"
        f"💰 Сумма: {order['total']} смн\n\n"
        f"{tail}"
    )
