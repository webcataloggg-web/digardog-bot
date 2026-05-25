import json
import secrets
from pathlib import Path

import aiosqlite

from services.cart import cart_lines, cart_total


DB_PATH = Path("data") / "digardog.sqlite3"


async def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_code TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT,
                items_json TEXT NOT NULL,
                items_text TEXT NOT NULL,
                total INTEGER NOT NULL,
                fulfillment TEXT NOT NULL,
                payment_method TEXT NOT NULL,
                address TEXT,
                receipt_file_id TEXT,
                status TEXT NOT NULL DEFAULT 'new',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await db.commit()


async def create_order(
    *,
    user_id: int,
    username: str | None,
    cart: dict[str, int],
    fulfillment: str,
    payment_method: str,
    address: str | None,
) -> dict:
    await init_db()
    order_code = f"{secrets.randbelow(9000) + 1000}L"
    items_text = "\n".join(cart_lines(cart))
    async with aiosqlite.connect(DB_PATH) as db:
        while True:
            try:
                await db.execute(
                    """
                    INSERT INTO orders (
                        order_code, user_id, username, items_json, items_text,
                        total, fulfillment, payment_method, address
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        order_code,
                        user_id,
                        username,
                        json.dumps(cart, ensure_ascii=False),
                        items_text,
                        cart_total(cart),
                        fulfillment,
                        payment_method,
                        address,
                    ),
                )
                await db.commit()
                break
            except aiosqlite.IntegrityError:
                order_code = f"{secrets.randbelow(9000) + 1000}L"
        return await get_order_by_code(order_code)


async def get_order_by_code(order_code: str) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM orders WHERE order_code = ?", (order_code,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def set_receipt(order_code: str, file_id: str) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE orders SET receipt_file_id = ? WHERE order_code = ?", (file_id, order_code))
        await db.commit()
    return await get_order_by_code(order_code)


async def set_status(order_code: str, status: str) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE orders SET status = ? WHERE order_code = ?", (status, order_code))
        await db.commit()
    return await get_order_by_code(order_code)
