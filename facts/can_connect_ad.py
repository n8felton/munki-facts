"""Returns a fact to indicate if this machine can talk to main.ad.rit.edu"""

import socket

s = socket.socket(2, 1)
s.settimeout(2)


def can_connect():
    """Returns True if it can connect to main.ad.rit.edu on port 445, False otherwise"""
    try:
        s.connect(("main.ad.rit.edu", 445))
        return True
    except:
        return False


def fact():
    """Return our can_connect_ad fact"""
    return {"can_connect_ad": can_connect()}


if __name__ == "__main__":
    print(fact())
