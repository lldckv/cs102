import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    items = get_friends(user_id=user_id, fields=["bdate"]).items
    today = dt.date.today()
    ages = []
    for item in items:
        try:
            bdate = item["bdate"].split(".")  # type: ignore
            if len(bdate) > 2:
                b = dt.date(int(bdate[2]), int(bdate[1]), int(bdate[0]))
                ages.append(int((today - b).days / 365.2425))
        except KeyError:
            pass
    if ages:
        return statistics.median(ages)
    return None


# age_predict(431493170)
