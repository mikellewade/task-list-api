from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_dict = {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": True if self.completed_at else False
            }

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict
        
    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data["title"],
            description=data["description"],
            completed_at= data.get("completed_at")
        )

        db.session.add(task)
        db.session.commit()

        return task