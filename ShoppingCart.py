import redis
import uuid
from typing import Dict, List

r = redis.Redis(host='localhost', port=6379, db=0)  # conn redis server

class ShoppingCarts:
    _EXPIRED_TIME = 900  # 15 minute

    @classmethod
    def save_cart(cls, **kwargs) -> Dict[str, str]:
        """
        Method to save a cart. 

        If the cart with the given user_id and activity_id already exists, a message indicating that 
        the item is already in the cart is returned.

        Parameters:
        kwargs (dict): Key-value pairs representing cart details.

        Returns:
        result (Dict[str, str]): A dictionary representing the saved cart.
        """
        user_id = kwargs['user_id']
        # check if cart already exists
        for user_carts in r.scan_iter(f"carts:{user_id}:*"):
            data = {index.decode('utf-8'): value.decode('utf-8') for index, value in r.hgetall(user_carts).items()}
            if int(data['user_id']) == kwargs['user_id'] and int(data['activity_id']) == kwargs['activity_id']:
                return {'message': 'Item already in cart'}

        kwargs['rowId'] = uuid.uuid4().hex
        key = f"carts:{user_id}:{kwargs['rowId']}"
        # store cart to redis
        for index, value in kwargs.items():
            r.hset(key, index, value)
        # set expired shopping cart
        r.expire(key, cls._EXPIRED_TIME)
        result = {key.decode('utf-8'): value.decode('utf-8') for key, value in r.hgetall(key).items()}
        return result

    @classmethod
    def carts(cls, user_id: int) -> List[Dict[str, str]]:
        """
        Method to get all carts for a user.

        Parameters:
        user_id (int): The user ID.

        Returns:
        result (List[Dict[str, str]]): A list of dictionaries representing all the carts of the user.
        """
        result = []
        for user_carts in r.scan_iter(f"carts:{user_id}:*"):
            data = {index.decode('utf-8'): value.decode('utf-8') for index, value in r.hgetall(user_carts).items()}
            result.append(data)
        return result

    @classmethod
    def update_person(cls, user_id: int, rowid: str, person: int) -> None:
        """
        Method to update the 'person' field for a cart.

        Parameters:
        user_id (int): The user ID.
        rowid (str): The row ID.
        person (int): The new 'person' value.
        """
        key = f"carts:{user_id}:{rowid}"
        if r.exists(key):
            r.hset(key, 'person', person)
            # reset expired if user update data in redis
            r.expire(key, cls._EXPIRED_TIME)
        else:
            print("The specified cart does not exist.")

    @classmethod
    def delete_cart(cls, user_id: int, rowid: str) -> int:
        """
        Method to delete a cart.

        Parameters:
        user_id (int): The user ID.
        rowid (str): The row ID.

        Returns:
        int: 1 if the cart was deleted, and 0 if the cart does not exist.
        """
        # if return 1 is true and return 0 is false it's mean data doesn't exist.
        return r.delete(f"carts:{user_id}:{rowid}")

    @classmethod
    def delete_all_carts(cls, user_id: int) -> None:
        """
        Method to delete all carts for a user.

        Parameters:
        user_id (int): The user ID.
        """
        for x in r.scan_iter(f"carts:{user_id}:*"):
            r.delete(x)
