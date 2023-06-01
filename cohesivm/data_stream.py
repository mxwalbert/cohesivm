"""Module containing the classes which handle the data stream from measurement methods."""


class FakeQueue:
    """Mimics the queue.Queue class to be used as default value for methods which implement an optional data stream.
    Simplifies the methods because they do not have to care if the queue is actually present and also prevents
    unnecessary data accumulation."""
    @staticmethod
    def put(data):
        pass
