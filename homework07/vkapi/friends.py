import dataclasses
import math
import time
import typing as tp

from vk_api.exceptions import ApiError  # type: ignore

from vkapi import config, session

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    c = config.VK_CONFIG
    if fields:
        query = f"/friends.get?access_token={c['access_token']}&user_id={user_id}&count={count}&offset={offset}&fields={','.join(fields)}&v={c['version']}"
    else:
        query = f"/friends.get?access_token={c['access_token']}&user_id={user_id}&count={count}&offset={offset}&v={c['version']}"
    try:
        response = session.get(url=str(query)).json()["response"]
        res=[]
        for friend in response["items"]:
            res.append(friend)
        return FriendsResponse(count=response["count"], items=res)
    except KeyError:
        pass


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    c = config.VK_CONFIG
    query = f"/friends.getMutual?access_token={c['access_token']}"
    if target_uid:
        if source_uid:
            query += f"&source_uid={source_uid}"
        query += f"&target_uid={target_uid}&order={order}"
        if count:
            query += f"&count={count}"
        query += f"&offset={offset}&v={c['version']}"
        response = session.get(url=str(query)).json()
        if response:
            return response["response"]
        return None  # type: ignore

    if target_uids and len(target_uids) > 100:
        chunks = [target_uids[i : i + 100] for i in range(0, len(target_uids), 100)]
        if len(target_uids) % 100 != 0:
            chunks.append(target_uids[100 * (len(target_uids)) // 100 :])
        results = []  # type: ignore
        offset_ = offset
        for chunk in chunks:
            result = get_mutual(source_uid=source_uid, target_uids=chunk, order=order, offset=offset_)
            offset_ += 100
            time.sleep(0.34)
            results.extend(result)
        return results

    if not target_uids:
        target_uids = get_friends(source_uid).items  # type: ignore
    mock = ",".join([str(i) for i in target_uids])  # type: ignore

    if source_uid:
        query += f"&source_uid={source_uid}"
    query += f"&target_uids={mock}&order={order}"
    if count:
        query += f"&count={count}"
    query += f"&offset={offset}&v={c['version']}"

    response = session.get(url=str(query)).json()
    if response:
        try:
            return response["response"]
        except KeyError:
            return None  # type: ignore
    return None  # type: ignore


# print(get_friends(user_id=431493170))
# print(get_mutual(target_uids = [1, 2, 3, 4, 5], count=3))
