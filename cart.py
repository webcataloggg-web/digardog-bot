import asyncio
from collections import defaultdict

from services.catalog import PRODUCTS


_lock = asyncio.Lock()
_carts: dict[int, dict[str, int]] = defaultdict(dict)
_selected_qty: dict[tuple[int, str], int] = {}


async def set_selected_qty(user_id: int, product_id: str, qty: int) -> int:
    async with _lock:
        qty = max(1, qty)
        _selected_qty[(user_id, product_id)] = qty
        return qty


async def change_selected_qty(user_id: int, product_id: str, delta: int) -> int:
    async with _lock:
        key = (user_id, product_id)
        qty = max(1, _selected_qty.get(key, 1) + delta)
        _selected_qty[key] = qty
        return qty


async def get_selected_qty(user_id: int, product_id: str) -> int:
    async with _lock:
        return _selected_qty.get((user_id, product_id), 1)


async def add_to_cart(user_id: int, product_id: str, qty: int) -> None:
    async with _lock:
        cart = _carts[user_id]
        cart[product_id] = cart.get(product_id, 0) + max(1, qty)
        _selected_qty.pop((user_id, product_id), None)


async def get_cart(user_id: int) -> dict[str, int]:
    async with _lock:
        return dict(_carts.get(user_id, {}))


async def clear_cart(user_id: int) -> None:
    async with _lock:
        _carts.pop(user_id, None)
        for key in list(_selected_qty):
            if key[0] == user_id:
                _selected_qty.pop(key, None)


def cart_total(cart: dict[str, int]) -> int:
    return sum(PRODUCTS[product_id].price * qty for product_id, qty in cart.items())


def cart_lines(cart: dict[str, int]) -> list[str]:
    return [f"• {PRODUCTS[product_id].name} x{qty}" for product_id, qty in cart.items()]
