"""
Collin typed activation integration.

Voice wake and typed wake both activate the same runtime state.
"""

from teaching.session import TeachingSessionManager
from wake.typed_listener import TypedWakeListener


class TypedActivation:
    def __init__(self, runtime=None):
        self.runtime = runtime
        self.teaching = TeachingSessionManager()

        self.listener = TypedWakeListener(
            on_wake=self.wake,
            on_learn=self.learn,
            on_write_here=self.write_here,
        )

    def wake(self):
        if self.runtime and not self.runtime.running:
            self.runtime.start()

        self.teaching.indicator("awake")

    def learn(self):
        self.teaching.start()

    def write_here(self):
        self.teaching.write_here()

    def start(self):
        self.listener.start()

    def stop(self):
        self.listener.stop()
