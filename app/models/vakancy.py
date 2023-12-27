from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# if TYPE_CHECKING:
# 	from .user import User  # noqa: F401


class Vakancy(Base):
	id = Column(Integer, primary_key=True)
	id_vakancy = Column(Integer)
	name = Column(String)
	kategory = Column(String)
	link = Column(String)
	company = Column(String)
	price = Column(Integer)
	description_short = Column(String)
	description_full = Column(Text)
	date_publikate = Column(String)
	owner_id = Column(Integer, ForeignKey("user.id"))
	owner = relationship("User", back_populates="vakancies")
