from gc import get_objects
from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from my_app.models import Item, Basket, BasketItem

# Создал список словарей, id каждый товар получит автоматически
items_data = [
        {
            'name': 'Очертания алой луны',
            'price': 180000,
            'description': 'Это острое копьё отливает алым лунным блеском. Говорят, во времена древней династии оно служило ритуальным орудием для молитв и было способно объединить два мира, но нынешние люди давно забыли эти традиции и верования.',
            'available': 1,
            'image_path': 'red_moon.jpg',
        },
        {
            'name': 'Шкатулка истин',
            'price': 150000,
            'description': 'Шкатулка с рогами, вырезанная из золота и нефрита. Легенда гласит, что некогда эта шкатулка хранилась в святилище в глубине сапфирового города Тулайтуллы.',
            'available': 2,
            'image_path': 'truth.jpg',
        },
        {
            'name': 'Сияющая жатва',
            'price': 130000,
            'description': 'Нагината для лёгкого «срезания травы». С такой же лёгкостью соберёт свою жатву с вражеской армии.',
            'available': 1,
            'image_path': 'harvest.jpg',
        },
        {
            'name': 'Рассветный иней',
            'price': 60000,
            'description': 'Безупречный ритуальный сосуд, выкованный из чистого серебра. Говорят, что некогда это была священная реликвия, которую девы крайнего севера передавали друг другу из поколения в поколение.',
            'available': 6,
            'image_path': 'moon.jpg',
        },
        {
            'name': 'Сон солнечным утром',
            'price': 90000,
            'description': 'Фонарь-колокольчик, выкованный из прозрачного аметиста. Говорят, он принесёт сладкие сновидения, если повесить его у изголовья.',
            'available': 0,
            'image_path': 'dreams.jpg',
        },
        {
            'name': 'Аква симулякрум',
            'price': 120000,
            'description': 'Лук, цвет которого непредсказуем. На свету кажется синим, словно вода. Среди других диковинных видов оружия этот прекрасный лук выделяется непостижимой властью вызывать воду.',
            'available': 3,
            'image_path': 'aqua.jpg',
        },
]

# Рендерим наши товары если их ещё нет
# решил написать цикл внутри списка, нашёл в интернете, что так компактнее, чем создавать items = [], а потом добавлять через append
def render_items(request):
    if Item.objects.count() == 0:
        items = [
            Item(
                name=item['name'],
                price=item['price'],
                description=item['description'],
                available=item['available'],
                image_path=item['image_path']
            )
                for item in items_data
        ]
        Item.objects.bulk_create(items)
    items = Item.objects.all()

    basket = get_basket(request)
    basket_items = BasketItem.objects.filter(basket=basket)
    basket_counts = {}

    for basket_item in basket_items:
        basket_counts[basket_item.item_id] = basket_item.count

    for item in items:
        item.basket_count = basket_counts.get(item.id, 0)

    # Решил добавить счетчик товаров к иконке корзины
    def get_basket_item_count(request):
        return sum(item.count for item in basket_items)

    basket_item_count = get_basket_item_count(request)

    return render(request, 'catalog.html', {'items':items, 'basket_item_count':basket_item_count, 'basket_counts':basket_counts})

# Получаем id товара из карточки и передаём товар в шаблон
def open_card(request):
    id_card = int(request.GET['id'])
    item = Item.objects.get(id=id_card)
    basket = get_basket(request)
    basket_item = BasketItem.objects.filter(basket=basket, item=item).first()
    basket_count = basket_item.count if basket_item else 0

    return render(request, 'card.html', {'item':item, 'basket_count':basket_count})

def get_basket(request):
    session_key = request.session.session_key
    if not session_key: # получаем идентификатор текущей сессии и на её основе находим либо создаём корзину
        request.session.create()
        session_key = request.session.session_key
    basket, created = Basket.objects.get_or_create(session_key=session_key)
    return basket

# добавление товара в корзину
def add_to_basket(request, item_id):
    item = get_object_or_404(Item, id=item_id) # получим id товара на котором была форма с кнопкой
    basket = get_basket(request) # и получим корзину

    basket_item, created = BasketItem.objects.get_or_create(
        basket=basket,
        item=item,
        defaults={'count': 1}
    )
    if not created: # если товар не создался, то увеличим счётчик текущего товара в корзине
        basket_item.count += 1
        basket_item.save()
    return redirect(request.META.get('HTTP_REFERER', '/')) # возвращаем пользователя на предыдущую страницу

# рендерим корзину товаров
def render_basket(request):
    basket = get_basket(request)
    basket_items = BasketItem.objects.filter(basket=basket).select_related('item')
    total = sum(float(basket_item.item.price) * basket_item.count for basket_item in basket_items)
    return render(request, 'basket.html', {'basket':basket,'basket_items':basket_items, 'total':total})

# удаление товара из корзины
def delete_from_basket(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    basket = get_basket(request)
    basket_item = BasketItem.objects.filter(basket=basket, item=item).first()

    if basket_item: # проверяем есть ли товар и больше ли одного экземпляра
        if basket_item.count > 1:
            basket_item.count -= 1 # если больше 1, то уменьшим счётчик
            basket_item.save()
        else:
            basket_item.delete() # если 1, то удаляем полностью
    return redirect(request.META.get('HTTP_REFERER', '/'))
