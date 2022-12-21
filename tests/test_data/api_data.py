class APIData:
    add_user_data = [
        {
            "case":
                (
                    "Correct New User Data - 201 expected",
                    "https://www.notion.so/4c244e11a01f4b83a30f51de333db957",
                    {"name": "Dmitry", "surname": "Surname", "middle_name": "Middle",
                     "username": "CorrectUser", "password": "Dmitry", "email": "dmitry@mail.ru"},
                    "application/json",
                    201
                )
        },
        {
            "case":
                (
                    "Bad Request (Wrong content-type) - 400 expected",
                    "https://www.notion.so/content-type-ab1611ff444b4195aefa125970b9c217",
                    {"name": "Dmitry", "surname": "Surname", "middle_name": "Middle",
                     "username": "TextContent", "password": "123456", "email": "content@mail.ru"},
                    "text/html; charset=utf-8",
                    400
                )
        },
        {
            "case":
                (
                    "Bad Request (Missing email field) - 400 expected",
                    "https://www.notion.so/email-cc1cda8e9fa9429a81626b4b2d57c408",
                    {"name": "Dmitry", "surname": "Surname", "middle_name": "Middle",
                     "username": "NoEmailUser", "password": "123456"},
                    "application/json",
                    400
                )
        },
        {
            "case":
                (
                    "Bad Request (Incorrect Email) - 400 expected",
                    "https://www.notion.so/email-2c08f1965f994131bc7e4d61b3b60d1a",
                    {"name": "Dmitry", "surname": "Surname", "middle_name": "Middle",
                     "username": "WrongEmailUser", "password": "123456", "email": "email"},
                    "application/json",
                    400
                )
        },
        {
            "case":
                (
                    "Bad Request (Empty Values) - 400 expected",
                    "https://www.notion.so/838c6b4dbfb34bd4b4b2296a1edbf6e9",
                    {"name": "", "surname": "", "middle_name": "",
                     "username": "", "password": "", "email": ""},
                    "application/json",
                    400
                )
        },
        {
            "case":
                (
                    "Bad Request (Spec Symbols) - 400 expected",
                    "https://www.notion.so/fc6a5a7131be44d999ed8c21bc86086c",
                    {"name": "######", "surname": "######", "middle_name": "######",
                     "username": "######", "password": "######", "email": "######"},
                    "application/json",
                    400
                )
        },
        {
            "case":
                (
                    "Bad Request (Long Values) - 400 expected",
                    "https://www.notion.so/d011324cd91e4dc5ba8e28e734f4643d",
                    {"name": "D"*256, "surname": "Surname", "middle_name": "Middle",
                     "username": "LongValuesUser", "password": "123456",
                     "email": "email@mail.ru"},
                    "application/json",
                    400
                )
        },
    ]

    delete_user_data = [
        {
            "case": (
                "DELETE existing user - 204 expected",
                "https://www.notion.so/3ec21e1910d64cdd8d3df75b66219e29",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "ToDelete",
                    "password": "ABC123456",
                    "email": "todelete@mail.ru",
                    "add_to_db": True
                },
                "DELETE",
                204
            )
        },
        {
            "case": (
                "DELETE non-existing user - 404 expected",
                "https://www.notion.so/d061612c2cf6438d821b5f3e635fc629",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "NonExistingUser",
                    "password": "ABC123456",
                    "email": "nonexistinguser@mail.ru",
                    "add_to_db": False
                },
                "DELETE",
                404
            )
        },
        {
            "case": (
                "GET existing user - 405 expected",
                "https://www.notion.so/3ec21e1910d64cdd8d3df75b66219e29",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "ExistingUser",
                    "password": "ABC123456",
                    "email": "existinguser@mail.ru",
                    "add_to_db": True
                },
                "GET",
                405
            )
        },
        {
            "case": (
                "DELETE with no user specified - 400 expected",
                "https://www.notion.so/22f01f8bc26a44d1991c9badc7b4dd99",
                {
                    "username": "",
                    "add_to_db": False
                },
                "DELETE",
                400
            )
        }
    ]

    block_user_data = [
        {
            "case": (
                "Block existing user - 200 expected",
                "https://www.notion.so/82c955eb75f64620aed971288442d583",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "ToBlock",
                    "password": "ABC123456",
                    "email": "toblock@mail.ru",
                    "add_to_db": True
                },
                "POST",
                200
            )
        },
        {
            "case": (
                "Block non-existing user - 200 expected",
                "https://www.notion.so/68a6252b8c2e47f098232c82d2bf30e3",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "NonExistingBlock",
                    "password": "ABC123456",
                    "email": "toblock-non-existing@mail.ru",
                    "add_to_db": False
                },
                "POST",
                404
            )
        },
        {
            "case": (
                "Wrong method can't be used to block user - 405 expected",
                "https://www.notion.so/POST-27f7d753f3ab447b9aa1196f3e0a1194",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "ToBlockGetMethod",
                    "password": "ABC123456",
                    "email": "toblock-get-method@mail.ru",
                    "add_to_db": True
                },
                "GET",
                405
            )
        },
        {
            "case": (
                "User cant be blocked twice - 400 expected",
                "https://www.notion.so/01b8c8009d6e4827bb5423c202884db7",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "TwiceBlocked",
                    "password": "ABC123456",
                    "email": "twice-blocked-user@mail.ru",
                    "add_to_db": True,
                    "repeat": 2
                },
                "POST",
                400
            )
        },
    ]

    unblock_user_data = [
        {
            "case": (
                "Unblock existing user - 200 expected",
                "https://www.notion.so/d11e7b24380c41bea212600baecddfcf",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "ToUnblock",
                    "password": "ABC123456",
                    "email": "to-unblock@mail.ru",
                    "add_to_db": True
                },
                "POST",
                200
            )
        },
        {
            "case": (
                "Unblock non-existing user - 200 expected",
                "https://www.notion.so/65a5b75c70a1483cada83e6587a3f6e1",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "NonExistUnblock",
                    "password": "ABC123456",
                    "email": "tounblock-non-exist@mail.ru",
                    "add_to_db": False
                },
                "POST",
                404
            )
        },
        {
            "case": (
                "Wrong method can't be used to unblock user - 405 expected",
                "https://www.notion.so/POST-491734b9329e4a92b4f845eeee88fa90",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "UnlockGetMethod",
                    "password": "ABC123456",
                    "email": "tounblock-get-method@mail.ru",
                    "add_to_db": True
                },
                "GET",
                405
            )
        },
        {
            "case": (
                "User cant be unblocked twice - 400 expected",
                "https://www.notion.so/f687309c3a81451590a3e31d095d71e7",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "TwiceUnlocked",
                    "password": "ABC123456",
                    "email": "twice-unblocked-user@mail.ru",
                    "add_to_db": True,
                    "repeat": 2
                },
                "POST",
                400
            )
        },
    ]

    change_password_data = [
        {
            "case": (
                "Change password of existing user - 200 expected",
                "https://www.notion.so/8269b27d0b674afc934ca4d76c49630d",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "ChangePass",
                    "password": "OLD_PASSWORD",
                    "new_password": "NEW_PASSWORD",
                    "email": "change-pass@mail.ru",
                    "add_to_db": True
                },
                "PUT",
                "application/json",
                200
            )
        },
        {
            "case": (
                "Change password of non-existing user - 404 expected",
                "https://www.notion.so/b77dfa2eef864c5c8ed5ec1f8c98c3bd",
                {
                    "username": "NonExistingUser",
                    "password": "OLD_PASS_NON_EXISTING",
                    "new_password": "NEW_PASSWORD_NON_EXISTING",
                    "add_to_db": False
                },
                "PUT",
                "application/json",
                404
            )
        },
        {
            "case": (
                "Old password cant be used as new password - 400 expected",
                "https://www.notion.so/fe4e8a66579a4f7db1afe10450338618",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "OldPassAsNewPass",
                    "password": "OLD_PASSWORD",
                    "new_password": "OLD_PASSWORD",
                    "email": "old-pass-as-new-pass@mail.ru",
                    "add_to_db": True
                },
                "PUT",
                "application/json",
                400
            )
        },
        {
            "case": (
                "Wrong Content-Type cant be used - 400 expected",
                "https://www.notion.so/content-type-81e50c12bbbb4e1d9384ae48b93b130e",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "WrongContentPass",
                    "password": "OLD_PASSWORD",
                    "new_password": "NEW_PASSWORD",
                    "email": "wrong-content-pass@mail.ru",
                    "add_to_db": True
                },
                "PUT",
                "text/html; charset=utf-8",
                400
            )
        },
        {
            "case": (
                "Wrong Method cant be used - 400 expected",
                "https://www.notion.so/PUT-e1938f9c6a6c4aad91a6db2b7456aaee",
                {
                    "name": "Dmitry",
                    "surname": "Surname",
                    "middle_name": "Middle",
                    "username": "WrongMethodPass",
                    "password": "OLD_PASSWORD",
                    "new_password": "NEW_PASSWORD",
                    "email": "wrong-method-pass@mail.ru",
                    "add_to_db": True
                },
                "POST",
                "application/json",
                400
            )
        },
    ]

    get_status_data = [
        {
            "case": (
                "GET app status - 200 expected",
                "https://www.notion.so/GET-d011324cd91e4dc5ba8e28e734f4643d",
                "GET",
                200
            )
        },
        {
            "case": (
                "POST app status - 400 expected",
                "https://www.notion.so/GET-a475ab1e2bf6474e97671eb10d26aacb",
                "POST",
                400
            )
        }
    ]
