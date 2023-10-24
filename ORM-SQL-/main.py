from sqlalchemy.orm import sessionmaker
from Models import create_tables, engine, Publisher, Shop, Book, Stock, Sale
import json
import datetime

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    create_tables(engine)
    with open("tests_data.json") as f:
	    json_data = json.load(f)
    for string in json_data:
        if string['model'] == 'publisher':
            pub = Publisher(id=string['pk'] , name=string['fields']['name'])
            session.add(pub)

        if string['model'] == 'book':
            book = Book(id=string['pk'], title=string['fields']['title'], publisher_id=string['fields']['id_publisher'])
            session.add(book)

        if string['model'] == 'shop':
            shop = Shop(id=string['pk'], name=string['fields']['name'])
            session.add(shop)

        if string['model'] == 'stock':
            stock = Stock(id=string['pk'], shop_id=string['fields']['id_shop'], book_id=string['fields']['id_book'],
                          count=string['fields']['count'])
            session.add(stock)

        if string['model'] == 'sale':
            date = datetime.datetime.strptime(string['fields']['date_sale'], "%Y-%m-%dT%H:%M:%S.%fZ")
            new_format = "%Y-%m-%d"
            date.strftime(new_format)
            sale = Sale(id=string['pk'], price=string['fields']['price'], date_sale=date,
                        stock_id=string['fields']['id_stock'], count=string['fields']['count'])
            session.add(sale)

    session.commit()
    pub = input('Введите имя издателя: ')
    subq = session.query(Book).join(Publisher, Book.publisher_id == Publisher.id).filter(Publisher.name == pub).subquery()
    subq2 = session.query(Stock).join(subq, Stock.book_id == subq.c.id ).subquery()
    q = session.query(Shop).join(subq2, Shop.id == subq2.c.shop_id).all()
    for s in q:
        print(s)
    session.close()