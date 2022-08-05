from app import *


def test_insert_persons():
    name = 'Coco'
    number = 654
    insert = f"""
    INSERT INTO phonebook.phonebook (name, number)
    VALUES ('{name.strip().lower()}', '{number}');
    """
    result = insert_person(name, number)

    assert result == 'Person with name Coco already exits.'

