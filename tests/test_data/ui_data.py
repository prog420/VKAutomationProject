class UITestData:
    # User with correct credentials
    correct_user = {
        "name": "Dmitry",
        "surname": "Surname",
        "middle_name": "Middle",
        "username": "UIUser",
        "password": "123456AQA",
        "email": "uiuser@mail.ru",
        "active": "1",
    }
    # User with invalid username (spec symbols in username)
    invalid_username_user = {
        "name": "Dmitry",
        "surname": "Surname",
        "middle_name": "Middle",
        "username": "$$$$$$",
        "password": "123456AQA",
        "email": "invalidusername@mail.ru",
        "active": "1",
    }
