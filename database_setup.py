## config code

import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()



## class code
class Restaurant(Base):
	#table code
	__tablename__ = 'restaurant'

	## mapper code
	name = Column( String(80), nullable = False)
	id = Column( Integer, primary_key = True)


## class code
class MenuItem(Base):
	#table code
	__tablename__ = 'menu_item'

	## mapper code
	name = Column(String(80), nullable = False)
	id = Column( Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column( Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)




## config code

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)