"""
This file contains the transaction support for pymongo methods,
with optional mongoengine integration.
"""

from functools import wraps
from time import sleep
from typing import Callable, Optional

from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.errors import OperationFailure

try:
    # Try to import from mongoengine
    from mongoengine.connection import get_db

    _USING_MONGOENGINE = True
except ImportError:
    get_db = None
    _USING_MONGOENGINE = False


if _USING_MONGOENGINE:

    class atomic:
        """
        A utility class for managing transactions in PyMongo.

        The `atomic` class can be used to ensure operations are executed within a
        transaction. It supports retries for transient errors when used as a decorator.

        Attributes:
            max_retries (int): The maximum number of retries for transient errors.
            retry_delay (int): The delay (in seconds) between retries.

        Note:
            - When used as a context manager, retry functionality is disabled, and
            only a single transaction attempt is made.
        """

        def __init__(self, max_retries=0, retry_delay=1):
            """
            Initialize the atomic transaction utility.

            Args:
                max_retries (int): The maximum number of retries for transient errors.
                retry_delay (int): The delay (in seconds) between retries.
            """
            self.session = None
            self.max_retries = max_retries
            self.retry_delay = retry_delay

        def __enter__(self):
            """
            Start a transaction session.
            """
            self.session = get_db().client.start_session()
            self.session.start_transaction()
            return self.session

        def __exit__(self, exc_type, exc_value, traceback):
            """
            Handle the transaction commit or abort based on exceptions.
            """
            if not exc_type:
                self.session.commit_transaction()
            else:
                self.session.abort_transaction()
            self.session.end_session()

        def __call__(self, func):
            """
            Decorator to execute a function within a transaction.

            Args:
                func (Callable): The function to execute within the transaction.
            """

            @wraps(func)
            def wrapper(*args, session: Optional[ClientSession] = None, **kwargs):
                def execute_with_retries(exec_func):
                    """Executes the given function with retries."""
                    for retry_attempt in range(self.max_retries + 1):
                        try:
                            return exec_func()
                        except OperationFailure as err:
                            if retry_attempt == self.max_retries:
                                raise err
                            sleep(self.retry_delay * retry_attempt)

                if session:
                    # Use the provided session for execution
                    return func(*args, session=session, **kwargs)
                else:
                    # Create a new session and execute within a transaction
                    with get_db().client.start_session() as new_session:
                        return execute_with_retries(
                            lambda: new_session.with_transaction(
                                lambda s: func(*args, session=s, **kwargs)
                            )
                        )

            return wrapper

else:

    class atomic:
        """
        Generic transaction support using PyMongo (no mongoengine).
        """

        def __init__(
            self, client: MongoClient, max_retries: int = 0, retry_delay: int = 1
        ):
            self.client = client
            self.session = None
            self.max_retries = max_retries
            self.retry_delay = retry_delay

        def __enter__(self) -> ClientSession:
            self.session = self.client.start_session()
            self.session.start_transaction()
            return self.session

        def __exit__(self, exc_type, exc_value, traceback):
            if not exc_type:
                self.session.commit_transaction()
            else:
                self.session.abort_transaction()
            self.session.end_session()

        def __call__(self, func: Callable):
            @wraps(func)
            def wrapper(*args, session: Optional[ClientSession] = None, **kwargs):
                def execute_with_retries(exec_func):
                    for retry_attempt in range(self.max_retries + 1):
                        try:
                            return exec_func()
                        except OperationFailure as err:
                            if retry_attempt == self.max_retries:
                                raise err
                            sleep(self.retry_delay * retry_attempt)

                if session:
                    return func(*args, session=session, **kwargs)
                else:
                    with self.client.start_session() as new_session:
                        return execute_with_retries(
                            lambda: new_session.with_transaction(
                                lambda s: func(*args, session=s, **kwargs)
                            )
                        )

            return wrapper
