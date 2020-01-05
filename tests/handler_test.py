import pytest
import src.handler


def test_is_table_backupable():
    table_description = {"TableStatus": "ACTIVE"}
    assert src.handler.is_table_backupable(table_description) == True

    table_description = {"TableStatus": "CREATING"}
    assert src.handler.is_table_backupable(table_description) == False


def test_handle_request():
    handler = src.handler.LambdaHandler()
    handler_input = {}
