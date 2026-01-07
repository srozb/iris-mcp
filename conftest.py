import os
import sys
import types
from unittest.mock import MagicMock

# Add vendor directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor/iris-client"))

# Mock dfir_iris_client modules
sys.modules["dfir_iris_client"] = MagicMock()
sys.modules["dfir_iris_client.session"] = MagicMock()
sys.modules["dfir_iris_client.case"] = MagicMock()
sys.modules["dfir_iris_client.alert"] = MagicMock()
sys.modules["dfir_iris_client.customer"] = MagicMock()
sys.modules["dfir_iris_client.admin"] = MagicMock()


# Mock fastmcp
class DummyFastMCP:
    def __init__(self, *_args, **_kwargs):
        self.registered = []

    def tool(self):
        def decorator(fn):
            self.registered.append(fn.__name__)
            return fn

        return decorator

    def run(self, **_kwargs):
        return None


sys.modules["fastmcp"] = types.SimpleNamespace(FastMCP=DummyFastMCP)
