from database import session
from users import models as users_models
from messages import models
from messages import schemas


def create_message(message: schemas.Message, user: users_models.User) -> dict:
    message = models.Message(
        text=message.text,
        user_id=user.id
    )
    session.add(message)
    session.flush()
    message = message.to_dict()
    session.commit()

    return message


def get_user(user_id: int) -> users_models.User:
    return session.query(users_models.User).filter_by(id=user_id).first()


def get_chat_history(offset: int, limit: int) -> list[dict]:
    chat_history = session.query(models.Message).offset(offset).limit(limit).all()
    chat_history = [_.to_dict() for _ in chat_history]

    for _ in chat_history:
        _["user"] = get_user(_["user_id"]).to_dict()
        _.pop("user_id")

    return chat_history
