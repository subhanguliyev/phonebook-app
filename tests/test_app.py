from app import *


def test_insert_persons():
    name = 'Coco'
    number = 654
    result = insert_person(name, number)
    assert result == 'Person with name Coco already exits.'


def test_find_persons_yes():
    keyword = 'Bill'
    person = find_persons(keyword)
    assert person == [{'id': 6, 'name': 'Bill', 'number': '987'}]


def test_find_persons_not():
    keyword = 'Obama'
    person = find_persons(keyword)
    assert person == [{'name': 'No Result', 'number': 'No Result'}]


def test_update_person():
    name = 'Marina'
    number = 222
    result = update_person(name, number)
    assert result == f'Person with name {name.strip().title()} does not exist.'


def test_delete_person():
    name = 'Sara'
    result = delete_person(name)
    assert result == f'Phone record of {name.strip().title()} is deleted from the phonebook successfully'

