import pytest
from tests.common.common_methods import unique_id
import random


def shorlink_creation_payload():
    """
    Payload for channels creation/editing
    :return: Payload.
    """
    return {"sl": "".join((random.choice("testautomation")) for x in range(5)),
            "des": "test automation using python requests",
            "url": "https://en.wikipedgia.org/wiki/Enigma_machine"}
