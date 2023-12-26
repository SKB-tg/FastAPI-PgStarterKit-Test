from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base

# if TYPE_CHECKING:
# 	from .user import User  # noqa: F401


class Vakancy(Base):
	__tablename__ = "vakancy"

	id = Column(Integer, primary_key=True, index=True)
	id_vakancy = Column(Integer, index=True)
	name = Column(String, index=True)
	kategory = Column(String, index=True)
	link = Column(String, index=True)
	company = Column(String, index=True)
	price = Column(Integer, index=True)
	description_short = Column(String, index=True)
	description_full = Column(Text, index=True)
	date_publikate = Column(Date, index=True)
