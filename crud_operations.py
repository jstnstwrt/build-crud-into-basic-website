from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

session = DBSession()

### crud operations 



## create ##
myFirstRestaurant = Restaurant( name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()

cheesepizza = MenuItem( name = "Cheese Pizza", description = "Made with all natural ingredients"
				, course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()


## read ##
firstResult = session.query(Restaurant).first()
print firstResult.name

items =  session.query(Restaurant).all()
for item in items:
	print item.name


## update ##
urbanVeggieBurger = session.query(MenuItem).filter_by(id = 11).one()
urbanVeggieBurger.price = '$2.99'
session.add(urbanVeggieBurger)
session.commit()


## delete ##
spinach = session.query(MenuItem).filter_by(name = "Spinach Ice Cream").one()
session.delete(spinach)
session.commit()

