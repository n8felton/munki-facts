#!/usr/local/munki/munki-python
"""Check if `hubcli` from VMware Workspace ONE Intelligent Hub.app is installed."""
import os


def fact():
    hubcli_path = "/usr/local/bin/hubcli"
    hubcli_installed = os.path.isfile(hubcli_path) and os.access(hubcli_path, os.X_OK)
    return {"ws1_hubcli_installed": hubcli_installed}


if __name__ == "__main__":
    print(fact())
