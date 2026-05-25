from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from services.catalog import CATEGORIES, Product, products_by_category


def categories_keyboard() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=category.title, callback_data=f"category_{category.id}")] for category in CATEGORIES]
    rows.append([InlineKeyboardButton(text="🛒 Корзина", callback_data="cart_view")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def category_keyboard(category_id: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"{product.name} — {product.price} смн", callback_data=f"add_select_{product.id}")]
        for product in products_by_category(category_id)
    ]
    rows.append([InlineKeyboardButton(text="🛒 Корзина", callback_data="cart_view")])
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data="category_back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def product_keyboard(product: Product, qty: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data=f"qty_minus_{product.id}"),
                InlineKeyboardButton(text=str(qty), callback_data=f"qty_show_{product.id}"),
                InlineKeyboardButton(text="➕", callback_data=f"qty_plus_{product.id}"),
            ],
            [InlineKeyboardButton(text="🛒 Добавить в корзину", callback_data=f"add_cart_{product.id}")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data=f"category_{product.category_id}")],
        ]
    )


def continue_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="cart_yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="cart_no"),
            ]
        ]
    )


def fulfillment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚚 Доставка", callback_data="delivery_start")],
            [InlineKeyboardButton(text="🛍 Самовывоз", callback_data="delivery_pickup")],
        ]
    )
