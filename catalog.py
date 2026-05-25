from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    id: str
    title: str


@dataclass(frozen=True)
class Product:
    id: str
    category_id: str
    name: str
    price: int


CATEGORIES: tuple[Category, ...] = (
    Category("burgers", "🍔 Бургеры"),
    Category("shawarma", "🌯 Шаурма"),
    Category("hotdogs", "🌭 Хот-доги"),
    Category("fries", "🍟 Картошка фри"),
    Category("drinks", "🥤 Напитки"),
)


PRODUCTS: dict[str, Product] = {
    "burger_classic": Product("burger_classic", "burgers", "Классический бургер", 25),
    "burger_chicken": Product("burger_chicken", "burgers", "Чикен Бургер", 20),
    "burger_double": Product("burger_double", "burgers", "Двойной бургер", 35),
    "shawarma_chicken": Product("shawarma_chicken", "shawarma", "Шаурма с курицей", 25),
    "shawarma_beef": Product("shawarma_beef", "shawarma", "Шаурма с говядиной", 30),
    "shawarma_mix": Product("shawarma_mix", "shawarma", "Шаурма микс", 30),
    "hotdog_classic": Product("hotdog_classic", "hotdogs", "Классический хот-дог", 15),
    "hotdog_cheese": Product("hotdog_cheese", "hotdogs", "Сырный хот-дог", 18),
    "fries_small": Product("fries_small", "fries", "Картошка фри маленькая", 10),
    "fries_large": Product("fries_large", "fries", "Картошка фри большая", 15),
    "rc_cola_05": Product("rc_cola_05", "drinks", "RC-Cola 0,5л", 6),
    "rc_cola_1": Product("rc_cola_1", "drinks", "RC-Cola 1л", 10),
    "rc_cola_15": Product("rc_cola_15", "drinks", "RC-Cola 1,5л", 11),
    "rc_green_05": Product("rc_green_05", "drinks", "RC-Cola Green 0,5л", 6),
    "rc_green_1": Product("rc_green_1", "drinks", "RC-Cola Green 1л", 10),
    "rc_green_15": Product("rc_green_15", "drinks", "RC-Cola Green 1,5л", 11),
    "sprite_1": Product("sprite_1", "drinks", "Sprite 1л", 10),
    "fusetea_05": Product("fusetea_05", "drinks", "Fusetea 0,5л", 6),
    "fusetea_1": Product("fusetea_1", "drinks", "Fusetea 1л", 10),
    "water_05": Product("water_05", "drinks", "Минеральная вода 0,5л", 5),
    "water_1": Product("water_1", "drinks", "Минеральная вода 1л", 10),
}


def products_by_category(category_id: str) -> list[Product]:
    return [product for product in PRODUCTS.values() if product.category_id == category_id]


def get_category(category_id: str) -> Category | None:
    return next((category for category in CATEGORIES if category.id == category_id), None)
