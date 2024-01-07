from typing import Generic, TypeVar, Callable

T = TypeVar('T')


class Notifier(Generic[T]):
    """Notifies subscribers when value is changed"""
    _value: T | None = None

    def __init__(self):
        """create an empty observer list"""

        self._observers = []

    def notify(self, modifier=None):
        """Alert the observers"""

        for observer in self._observers:
            if modifier != observer:
                observer(self.value)

    def attach(self, observer: Callable[[T], None]):
        """If the observer is not in the list,
        append it into the list"""

        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Remove the observer from the observer list"""

        try:
            self._observers.remove(observer)
        except ValueError:
            print("error removing")
            pass

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T):
        self._value = value
        self.notify()
