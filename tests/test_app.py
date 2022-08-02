from app import *


def test_insert_persons():
    name = 'Sara'
    number = 345
    insert = f"""
    INSERT INTO phonebook.phonebook (name, number)
    VALUES ('{name.strip().lower()}', '{number}');
    """
    result = cursor.execute(insert)
    assert result == insert


def test_find_persons():
    keyword = 'Bill'
    query = f"""
        SELECT * FROM phonebook.phonebook WHERE name like '%{keyword.strip().lower()}%';
        """
    result = cursor.fetchall()
    persons = [{'id': row[0], 'name': row[1].strip().title(), 'number': row[2]} for row in result]
    assert persons == query


def test_find_get_post():
    keyword = request.form['username']
    persons_app = find_persons(keyword)
    response = render_template('index.html', persons_html=persons_app, keyword=keyword)
    assert persons_app == response
