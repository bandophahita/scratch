from __future__ import annotations

from typing import Union

from screenpy import Actor
from screenpy.protocols import Forgettable
from selenium.webdriver import Chrome, Firefox, Safari
from selenium.webdriver.remote.webdriver import WebDriver


class ManageBrowserLocalStorage(Forgettable):
    """
    The ability to manage the browser.  This includes featuers that are
    outside normal web browsing like clearing cache, or accessing devtools.

    Examples::

        Perry = AnActor.named("Perry").who_can(ManageTheBrowser.using_firefox())

        Perry = AnActor.named("Perry").who_can(ManageTheBrowser.using(driver))
    """

    def forget(self):
        self.driver.quit()

    @staticmethod
    def using(driver: WebDriver) -> ManageBrowserLocalStorage:
        """Provide an already-set-up |WebDriver| to use manage the browser"""
        return ManageBrowserLocalStorage(driver)

    @staticmethod
    def using_chrome() -> ManageBrowserLocalStorage:
        """Create and use a default Chrome Selenium webdriver instance."""
        return ManageBrowserLocalStorage.using(Chrome())

    @staticmethod
    def using_firefox() -> ManageBrowserLocalStorage:
        """Create and use a default Firefox Selenium webdriver instance."""
        return ManageBrowserLocalStorage.using(Firefox())

    @staticmethod
    def using_safari() -> ManageBrowserLocalStorage:
        """Create and use a default Safari Selenium webdriver instance."""
        return ManageBrowserLocalStorage.using(Safari())

    def clear_all_cache(self):
        self.localstorage.clear()

    clear_cache = to_clear_cache = to_clear_all_cache = clear_all_cache

    def get_item(self, key: str):
        return self.localstorage.get(key)

    to_get_item = get_item

    def remove_item(self, key: str):
        self.localstorage.remove(key)

    to_remove_item = remove_item

    def get_all_items(self):
        return self.localstorage.items()

    to_get_all_items = get_all_items

    def get_all_keys(self):
        return self.localstorage.keys()

    to_get_all_keys = get_all_keys

    @staticmethod
    def as_(actor: Actor):
        return actor.ability_to(ManageBrowserLocalStorage)

    def __repr__(self) -> str:
        return "manage browser LocalStorage"

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.localstorage = LocalStorage(driver)


################################################################################
class LocalStorage:
    # https://stackoverflow.com/questions/46361494/how-to-get-the-localstorage-with-python-and-selenium-webdriver
    # python API doesn't provide a way to access the local storage.
    # But selenium does.

    def __init__(self, driver: Union[WebDriver]):
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self):
        if self.__on_data():
            return
        return self.driver.execute_script(
            "var ls = window.localStorage, items = {}; "
            "for (var i = 0, k; i < ls.length; ++i) "
            "  items[k = ls.key(i)] = ls.getItem(k); "
            "return items; "
        )

    def keys(self):
        if self.__on_data():
            return
        return self.driver.execute_script(
            "var ls = window.localStorage, keys = []; "
            "for (var i = 0; i < ls.length; ++i) "
            "  keys[i] = ls.key(i); "
            "return keys; "
        )

    def get(self, key):
        if self.__on_data():
            return
        return self.driver.execute_script(
            "return window.localStorage.getItem(arguments[0]);", key
        )

    def set(self, key, value):
        if self.__on_data():
            return
        self.driver.execute_script(
            "window.localStorage.setItem(arguments[0], arguments[1]);", key, value
        )

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        if self.__on_data():
            return
        self.driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        if self.__on_data():
            return
        self.driver.execute_script("window.localStorage.clear();")

    def __on_data(self):
        return self.driver.current_url == "data:,"

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()
