from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

from connect import engine


class Base(DeclarativeBase):
    pass


class Activity(Base):
    """
    Class for persisting activities given by Bored API
    """
    __tablename__ = "activities"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    participants: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=True)
    key: Mapped[int] = mapped_column(nullable=False)
    accessibility: Mapped[float] = mapped_column(nullable=False)

    @staticmethod
    def get_last_activities(self, number_of_activities=5):
        activity_session = Session(bind=engine)
        last_activities = activity_session.query(Activity).order_by(Activity.id.desc()).limit(number_of_activities).all()
        return "".join(map(str, last_activities))

    def __repr__(self):
        return f"Activity: {self.name} \n" \
               f"Type: {self.type} \n" \
               f"Participants: {self.participants} \n" \
               f"Price: {self.price} \n" \
               f"Accessibility: {self.accessibility} \n" \
               f"Link: {self.link} \n" \
               "-----------------------------\n"


Base.metadata.create_all(engine)
