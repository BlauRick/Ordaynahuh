import requests

def handleApiError(response: requests.Response, expected_res_code, expected_res_body: str):
    global tests_passed
    passed = True
    if (response.status_code != expected_res_code or response.text != expected_res_body):
        text = "\n        ".join(response.text.split("\n"))
        expected_text = "\n        ".join(expected_res_body.split("\n"))
        if (text.__len__() == 0): text = "[No Content]"
        print(f"❌\n        Test failed with status code: {response.status_code}\n        Received body: {text}\n        Expected body: {expected_text}")
        passed = False
    else:
        print("✔")

    if (response.cookies.__len__() != 0 and response.status_code >= 400):
        print("        Endpoint returned cookies!!!")
        passed = False

    if (passed): tests_passed += 1

def testEndpoint(message: str, method: str, endpoint_path: str, cookies, payload: dict(), expected_res_code, expected_res_body):
    global test_count
    test_count += 1
    print(f"{test_count:>4} {message}: ", end="")

    response = requests.request(method, URL + endpoint_path, json=payload, cookies=cookies)
    handleApiError(response, expected_res_code, expected_res_body)
    return response

def testEndpointNoErrorHandling(message: str, method: str, endpoint_path: str, cookies, payload: dict()):
    global test_count
    test_count += 1
    print(f"{test_count:>4} {message}: ", end="")

    return requests.request(method, URL + endpoint_path, json=payload, cookies=cookies)

test_count = 0
tests_passed = 0
refresh_jar = dict()
access_jar = dict()
wrong_access_jar = dict()
wrong_refresh_jar = dict()
reuse_refresh_jar = dict()
intezmeny_id = 0
URL = "http://127.0.0.1:8000"

def main():
    global test_count
    global tests_passed

    createUser()
    tokens()
    changeUserData()
    createIntezmeny()
    intezmenyCreateEndpoints()
    intezmenyGetEndpoints()
    deleteIntezmeny()
    deleteUser()

    print("\n" + "-"*30+"Cleanup"+"-"*30 + "\n")
    cleanup()

    print(f"\nTests passed: {tests_passed}/{test_count}")


def createUser():
    testEndpoint("Create user, no display name", "POST", "/user/create_user", "",
                 {"email": "tester@test.com", "phone_number": "123456789012345", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, display name empty", "POST", "/user/create_user", "",
                 {"disp_name": "", "email": "tester@test.com", "phone_number": "123456789012345", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, display name length longer than 200", "POST", "/user/create_user", "",
                 {"disp_name": "tester" * 40, "email": "tester@test.com", "phone_number": "123456789012345", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, display name not string", "POST", "/user/create_user", "",
                 {"disp_name": ["tester"], "email": "tester@test.com", "phone_number": "123456789012345", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, no email", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "phone_number": "123456789012345", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, email empty", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "", "phone_number": "123456789012345", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, email not string", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": ["tester@test.com"], "phone_number": "123456789012345", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, email length longer than 254", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester@test.com" * 30, "phone_number": "123456789012345", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, email with no @", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "testertest.com", "phone_number": "123456789012345", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, no password", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester@test.com", "phone_number": "123456789012345"},
                 400, "Bad request")
    testEndpoint("Create user, password not string", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester@test.com", "phone_number": "123456789012345", "pass": ["tester_pass"]},
                 400, "Bad request")
    testEndpoint("Create user, password length not at least 8", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester@test.com", "phone_number": "123456789012345", "pass": "tester_"},
                 400, "Bad request")
    testEndpoint("Create user, no phone number", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester_no_phone@test.com", "pass": "tester_pass"},
                 201, "")
    testEndpoint("Create user, phone number empty", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester@test.com", "phone_number": "", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, phone number not string", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester@test.com", "phone_number": ["123456789012345"], "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, phone number is not numeric", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester@test.com", "phone_number": "12345678901234a", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, phone number length longer than 15", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester@test.com", "phone_number": "1234567890123456", "pass": "tester_pass"},
                 400, "Bad request")
    testEndpoint("Create user, method is not POST", "PATCH", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester@test.com", "phone_number": "123456789012345", "pass": "tester_pass"},
                 405, "")
    testEndpoint("Create user", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester@test.com", "phone_number": "123456789012345", "pass": "tester_pass"},
                 201, "")
    testEndpoint("Create user, user already exists", "POST", "/user/create_user", "",
                 {"disp_name": "tester", "email": "tester@test.com", "phone_number": "123456789012345", "pass": "tester_pass"},
                 400, "User already exists")


def tokens():
    global refresh_jar
    global access_jar
    global wrong_access_jar
    global wrong_refresh_jar
    global reuse_refresh_jar

    refresh_jar = testEndpoint("Get refresh token", "POST", "/token/get_refresh_token", "",
                 {"email": "tester@test.com", "pass": "tester_pass"}, 200, "").cookies
    testEndpoint("Get refresh token, no email", "POST", "/token/get_refresh_token", "",
                 {"pass": "tester_pass"}, 400, "Bad request")
    testEndpoint("Get refresh token, email empty", "POST", "/token/get_refresh_token", "",
                 {"email": "", "pass": "tester_pass"}, 400, "Bad request")
    testEndpoint("Get refresh token, email not string", "POST", "/token/get_refresh_token", "",
                 {"email": ["tester@test.com"], "pass": "tester_pass"}, 400, "Bad request")
    testEndpoint("Get refresh token, email with no @", "POST", "/token/get_refresh_token", "",
                 {"email": "testertest.com", "pass": "tester_pass"}, 400, "Bad request")
    testEndpoint("Get refresh token, no password", "POST", "/token/get_refresh_token", "",
                 {"email": "tester@test.com"}, 400, "Bad request")
    testEndpoint("Get refresh token, password empty", "POST", "/token/get_refresh_token", "",
                 {"email": "tester@test.com", "pass": ""}, 400, "Bad request")
    testEndpoint("Get refresh token, password not string", "POST", "/token/get_refresh_token", "",
                 {"email": "tester@test.com", "pass": ["tester_pass"]}, 400, "Bad request")
    testEndpoint("Get refresh token, password incorrect", "POST", "/token/get_refresh_token", "",
                 {"email": "tester@test.com", "pass": "tester_pass_incorrect"}, 403, "Unauthorised")
    testEndpoint("Get refresh token, method is not POST", "PATCH", "/token/get_refresh_token", "",
                 {"email": "tester@test.com", "pass": "tester_pass"}, 405, "")

    reuse_refresh_jar = refresh_jar.copy()
    refresh_jar = testEndpoint("Refresh refresh token", "POST", "/token/refresh_refresh_token", refresh_jar,
                 {}, 200, "").cookies
    wrong_access_jar = refresh_jar.copy()
    for cookie in wrong_access_jar:
        if cookie.name == 'RefreshToken':
            cookie.name = "AccessToken"
            cookie.path = "/"
            break

    access_jar = testEndpoint("Get access token", "POST", "/token/get_access_token", refresh_jar,
                 {}, 200, "").cookies
    wrong_refresh_jar = access_jar.copy()
    for cookie in wrong_refresh_jar:
        if cookie.name == 'AccessToken':
            cookie.name = "RefreshToken"
            cookie.path = "/"
            break

    testEndpoint("Refresh refresh token, reused refresh token", "POST", "/token/refresh_refresh_token", reuse_refresh_jar,
                 {}, 403, "Unauthorised")
    testEndpoint("Refresh refresh token, wrong refresh token", "POST", "/token/refresh_refresh_token", wrong_refresh_jar,
                 {}, 403, "Unauthorised")
    testEndpoint("Get access token, reused refresh token", "POST", "/token/get_access_token", reuse_refresh_jar,
                 {}, 403, "Unauthorised")
    testEndpoint("Get access token, wrong refresh token", "POST", "/token/get_access_token", wrong_refresh_jar,
                 {}, 403, "Unauthorised")


def changeUserData():
    global access_jar
    global wrong_access_jar

    testEndpoint("Change display name", "POST", "/user/change_disp_name", access_jar,
                 {"new_disp_name": "testerer"}, 204, "")
    testEndpoint("Change display name, no new display name", "POST", "/user/change_disp_name", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Change display name, new display name empty", "POST", "/user/change_disp_name", access_jar,
                 {"new_disp_name": ""}, 400, "Bad request")
    testEndpoint("Change display name, new display name not string", "POST", "/user/change_disp_name", access_jar,
                 {"new_disp_name": ["testerer"]}, 400, "Bad request")
    testEndpoint("Change display name, new display name length longer than 200", "POST", "/user/change_disp_name", access_jar,
                 {"new_disp_name": "testerer" * 25 + "+"}, 400, "Bad request")
    testEndpoint("Change display name, wrong token", "POST", "/user/change_disp_name", wrong_access_jar,
                 {"new_disp_name": "testerer"}, 403, "Unauthorised")
    testEndpoint("Change display name, no token", "POST", "/user/change_disp_name", "",
                 {"new_disp_name": "testerer"}, 400, "Bad request")
    testEndpoint("Change display name, method is not POST", "PATCH", "/user/change_disp_name", access_jar,
                 {"new_disp_name": "testerer"}, 405, "")

    testEndpoint("Change phone number", "POST", "/user/change_phone_number", access_jar,
                 {"new_phone_number": "12345"}, 204, "")
    testEndpoint("Change phone number, no new phone number", "POST", "/user/change_phone_number", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Change phone number, new phone number empty", "POST", "/user/change_phone_number", access_jar,
                 {"new_phone_number": ""}, 400, "Bad request")
    testEndpoint("Change phone number, new phone number not string", "POST", "/user/change_phone_number", access_jar,
                 {"new_phone_number": ["12345"]}, 400, "Bad request")
    testEndpoint("Change phone number, new phone number not numeric", "POST", "/user/change_phone_number", access_jar,
                 {"new_phone_number": "12345a"}, 400, "Bad request")
    testEndpoint("Change phone number, new phone number length longer than 15", "POST", "/user/change_phone_number", access_jar,
                 {"new_phone_number": "12345" * 3 + "+"}, 400, "Bad request")
    testEndpoint("Change phone number, wrong token", "POST", "/user/change_phone_number", wrong_access_jar,
                 {"new_phone_number": "12345"}, 403, "Unauthorised")
    testEndpoint("Change phone number, no token", "POST", "/user/change_phone_number", "",
                 {"new_phone_number": "12345"}, 400, "Bad request")
    testEndpoint("Change phone number, method is not POST", "PATCH", "/user/change_phone_number", access_jar,
                 {"new_phone_number": "12345"}, 405, "")

    testEndpoint("Change password", "POST", "/user/change_pass", access_jar,
                 {"new_pass": "tmp_tester_pass"}, 204, "")
    testEndpoint("Change password back", "POST", "/user/change_pass", access_jar,
                 {"new_pass": "tester_pass"}, 204, "")
    testEndpoint("Change password, no new password", "POST", "/user/change_pass", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Change password, new password not string", "POST", "/user/change_pass", access_jar,
                 {"new_pass": ["tester_pass"]}, 400, "Bad request")
    testEndpoint("Change password, new password length no at least 8", "POST", "/user/change_pass", access_jar,
                 {"new_pass": "tester_"}, 400, "Bad request")
    testEndpoint("Change password", "POST", "/user/change_pass", wrong_access_jar,
                 {"new_pass": "tester_pass"}, 403, "Unauthorised")
    testEndpoint("Change password, no token", "POST", "/user/change_pass", "",
                 {"new_pass": "tester_pass"}, 400, "Bad request")
    testEndpoint("Change password, method is not POST", "PATCH", "/user/change_pass", access_jar,
                 {"new_pass": "tester_pass"}, 405, "")


def createIntezmeny():
    global access_jar
    global wrong_access_jar
    global intezmeny_id

    testEndpoint("Create intezmeny", "POST", "/create_intezmeny", access_jar,
                 {"intezmeny_name": "tester_intezmeny"}, 201, "")
    testEndpoint("Create intezmeny, intezmeny_name not string", "POST", "/create_intezmeny", access_jar,
                 {"intezmeny_name": ["tester_intezmeny"]}, 400, "Bad request")
    testEndpoint("Create intezmeny, no intezmeny_name", "POST", "/create_intezmeny", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Create intezmeny, intezmeny_name empty", "POST", "/create_intezmeny", access_jar,
                 {"intezmeny_name": ""}, 400, "Bad request")
    testEndpoint("Create intezmeny, intezmeny_name length longer than 200", "POST", "/create_intezmeny", access_jar,
                 {"intezmeny_name": "tester_intezmeny"*16}, 400, "Bad request")
    testEndpoint("Create intezmeny, wrong token", "POST", "/create_intezmeny", wrong_access_jar,
                 {"intezmeny_name": "tester_intezmeny"}, 403, "Unauthorised")
    testEndpoint("Create intezmeny, no token", "POST", "/create_intezmeny", "",
                 {"intezmeny_name": "tester_intezmeny"}, 400, "Bad request")
    testEndpoint("Create intezmeny, method is not POST", "PATCH", "/create_intezmeny", access_jar,
                 {"intezmeny_name": "tester_intezmeny"}, 405, "")

    response = testEndpointNoErrorHandling("Get intezmenys", "GET", "/get_intezmenys", access_jar, {})
    intezmeny_id = response.json()[0][0]
    handleApiError(response, 200, f"[[{intezmeny_id},\"tester_intezmeny\"]]")
    testEndpoint("Get intezmenys, wrong token", "GET", "/get_intezmenys", wrong_access_jar,
                 {}, 403, "Unauthorised")
    testEndpoint("Get intezmenys, no token", "GET", "/get_intezmenys", "",
                 {}, 400, "Bad request")
    testEndpoint("Get intezmenys, method is not GET", "PATCH", "/get_intezmenys", access_jar,
                 {}, 405, "")


def intezmenyCreateEndpoints():
    global access_jar
    global wrong_access_jar
    global intezmeny_id

    testEndpoint("Create class, intezmeny does not exist", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": "347653267853", "name": "test_class", "headcount": "30"}, 403, "Unauthorised")
    testEndpoint("Create class, intezmeny id out of representable range of int", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": "347653267853" * 25, "name": "test_class", "headcount": "30"}, 400, "Bad request")
    testEndpoint("Create class, no intezmeny id", "POST", "/intezmeny/create/class", access_jar,
                 {"name": "test_class", "headcount": "30"}, 400, "Bad request")
    testEndpoint("Create class, intezmeny id empty", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": "", "name": "test_class", "headcount": "30"}, 400, "Bad request")
    testEndpoint("Create class, intezmeny id is not string", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"], "name": "test_class", "headcount": "30"}, 400, "Bad request")
    testEndpoint("Create class, intezmeny id is not numeric", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a", "name": "test_class", "headcount": "30"}, 400, "Bad request")
    testEndpoint("Create class, no name", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "headcount": "30"}, 400, "Bad request")
    testEndpoint("Create class, name empty", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "", "headcount": "30"}, 400, "Bad request")
    testEndpoint("Create class, name is not string", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": ["test_class"], "headcount": "30"}, 400, "Bad request")
    testEndpoint("Create class, name too long", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_class" * 30, "headcount": "30"}, 400, "Bad request")
    testEndpoint("Create class, headcount out of representable range of int", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_class", "headcount": "30" * 100}, 400, "Bad request")
    testEndpoint("Create class, headcount out of representable range of smallint", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_class", "headcount": "300000"}, 400, "Bad request")
    testEndpoint("Create class, no headcount", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_class"}, 400, "Bad request")
    testEndpoint("Create class, headcount empty", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_class", "headcount": ""}, 400, "Bad request")
    testEndpoint("Create class, headcount is not string", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_class", "headcount": ["30"]}, 400, "Bad request")
    testEndpoint("Create class, wrong token", "POST", "/intezmeny/create/class", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_class", "headcount": "30"}, 403, "Unauthorised")
    testEndpoint("Create class, headcount is not numeric", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a", "name": "test_class", "headcount": "30a"}, 400, "Bad request")
    testEndpoint("Create class, no token", "POST", "/intezmeny/create/class", "",
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_class", "headcount": "30"}, 400, "Bad request")
    testEndpoint("Create class, method not POST", "PATCH", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_class", "headcount": "30"}, 405, "")
    testEndpoint("Create class", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_class", "headcount": "30"}, 201, "")
    testEndpoint("Create class, already exists", "POST", "/intezmeny/create/class", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_class", "headcount": "30"}, 400, "Bad request")

    testEndpoint("Create lesson, intezmeny does not exist", "POST", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": "347653267853", "name": "test_lesson"}, 403, "Unauthorised")
    testEndpoint("Create lesson, intezmeny id out of representable range of int", "POST", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": "347653267853" * 25, "name": "test_lesson"}, 400, "Bad request")
    testEndpoint("Create lesson, no intezmeny id", "POST", "/intezmeny/create/lesson", access_jar,
                 {"name": "test_lesson"}, 400, "Bad request")
    testEndpoint("Create lesson, intezmeny id empty", "POST", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": "", "name": "test_lesson"}, 400, "Bad request")
    testEndpoint("Create lesson, intezmeny id is not string", "POST", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"], "name": "test_lesson"}, 400, "Bad request")
    testEndpoint("Create lesson, intezmeny id is not numeric", "POST", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a", "name": "test_lesson"}, 400, "Bad request")
    testEndpoint("Create lesson, no name", "POST", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 400, "Bad request")
    testEndpoint("Create lesson, name empty", "POST", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": ""}, 400, "Bad request")
    testEndpoint("Create lesson, name is not string", "POST", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": ["test_lesson"]}, 400, "Bad request")
    testEndpoint("Create lesson, name too long", "POST", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_lesson" * 20}, 400, "Bad request")
    testEndpoint("Create lesson, wrong token", "POST", "/intezmeny/create/lesson", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_lesson"}, 403, "Unauthorised")
    testEndpoint("Create lesson, no token", "POST", "/intezmeny/create/lesson", "",
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_lesson"}, 400, "Bad request")
    testEndpoint("Create lesson, method not POST", "PATCH", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_lesson"}, 405, "")
    testEndpoint("Create lesson", "POST", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_lesson"}, 201, "")
    testEndpoint("Create lesson, already exists", "POST", "/intezmeny/create/lesson", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_lesson"}, 400, "Bad request")

    testEndpoint("Create group, intezmeny does not exist", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": "347653267853", "name": "test_group", "headcount": "30", "class_id": "1"}, 403, "Unauthorised")
    testEndpoint("Create group, intezmeny id out of representable range of int", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": "347653267853" * 25, "name": "test_group", "headcount": "30", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, no intezmeny id", "POST", "/intezmeny/create/group", access_jar,
                 {"name": "test_group", "headcount": "30", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, intezmeny id empty", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": "", "name": "test_group", "headcount": "30", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, intezmeny id is not string", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"], "name": "test_group", "headcount": "30", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, intezmeny id is not numeric", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a", "name": "test_group", "headcount": "30", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, no name", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "headcount": "30", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, name empty", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "", "headcount": "30", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, name is not string", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": ["test_group"], "headcount": "30", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, name too long", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group" * 30, "headcount": "30", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, headcount out of representable range of int", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "30" * 100, "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, headcount out of representable range of smallint", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "300000", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, no headcount", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, headcount empty", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, headcount is not string", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": ["30"], "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, class does not exist", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "30", "class_id": "0"}, 400, "Bad request")
    testEndpoint("Create group, class id out of representable range of int", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "30", "class_id": "112434" * 25}, 400, "Bad request")
    testEndpoint("Create group, no class id", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group_no_class_id", "headcount": "30"}, 201, "")
    testEndpoint("Create group, class id empty", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "30", "class_id": ""}, 400, "Bad request")
    testEndpoint("Create group, class id is not string", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "30", "class_id": ["1"]}, 400, "Bad request")
    testEndpoint("Create group, class id is not numeric", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "30", "class_id": "1a"}, 400, "Bad request")
    testEndpoint("Create group, wrong token", "POST", "/intezmeny/create/group", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "30", "class_id": "1"}, 403, "Unauthorised")
    testEndpoint("Create group, no token", "POST", "/intezmeny/create/group", "",
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "30", "class_id": "1"}, 400, "Bad request")
    testEndpoint("Create group, method not POST", "PATCH", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "30", "class_id": "1"}, 405, "")
    testEndpoint("Create group", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "30", "class_id": "1"}, 201, "")
    testEndpoint("Create group, group already exists", "POST", "/intezmeny/create/group", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_group", "headcount": "30", "class_id": "1"}, 400, "Bad request")

    testEndpoint("Create room, intezmeny does not exist", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": "347653267853", "type": "test", "name": "test_room", "space": "30"}, 403, "Unauthorised")
    testEndpoint("Create room, intezmeny id out of representable range of int", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": "347653267853" * 25, "type": "test", "name": "test_room", "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, no intezmeny id", "POST", "/intezmeny/create/room", access_jar,
                 {"name": "test_room", "type": "test", "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, intezmeny id empty", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": "", "name": "test_room", "type": "test", "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, intezmeny id is not string", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"], "name": "test_room", "type": "test", "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, intezmeny id is not numeric", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a", "name": "test_room", "type": "test", "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, no name", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, name empty", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "", "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, name is not string", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": ["test_room"], "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, name too long", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room" * 30, "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, no type", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room_no_type", "space": "30"}, 201, "")
    testEndpoint("Create room, type empty", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "", "name": "test_room", "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, type is not string", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": ["test"], "name": "test_room", "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, type too long", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test" * 60, "name": "test_room", "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, space out of representable range of int", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room", "space": "30" * 100}, 400, "Bad request")
    testEndpoint("Create room, space out of representable range of smallint", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room", "space": "300000"}, 400, "Bad request")
    testEndpoint("Create room, no space", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room"}, 400, "Bad request")
    testEndpoint("Create room, space empty", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room", "space": ""}, 400, "Bad request")
    testEndpoint("Create room, space is not string", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room", "space": ["30"]}, 400, "Bad request")
    testEndpoint("Create room, wrong token", "POST", "/intezmeny/create/room", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room", "space": "30"}, 403, "Unauthorised")
    testEndpoint("Create room, no token", "POST", "/intezmeny/create/room", "",
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room", "space": "30"}, 400, "Bad request")
    testEndpoint("Create room, method not POST", "PATCH", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room", "space": "30"}, 405, "")
    testEndpoint("Create room", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room", "space": "30"}, 201, "")
    testEndpoint("Create room, room already exists", "POST", "/intezmeny/create/room", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "type": "test", "name": "test_room", "space": "30"}, 400, "Bad request")

    testEndpoint("Create teacher, intezmeny does not exist", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": "636345653", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 403, "Unauthorised")
    testEndpoint("Create teacher, intezmeny id out of representable range of int", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": "2633246356" * 25, "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, no intezmeny id", "POST", "/intezmeny/create/teacher", access_jar,
                 {"name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, intezmeny id empty", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": "", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, intezmeny id is not string", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"], "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, intezmeny id is not numeric", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, no name", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, name empty", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, name is not string", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": ["test_teacher"], "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, name too long", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher" * 30, "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, no job", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, job empty", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, job is not string", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": ["test"], "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, job too long", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test" * 60, "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, no email", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher_no_email", "job": "test", "phone_number": "12345"},
                 201, "")
    testEndpoint("Create teacher, email empty", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, email with no @", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "testertest.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, email not string", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": ["tester@test.com"], "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, email too long", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "tester@test.com" * 50, "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, no phone number", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher_no_phone", "job": "test", "email": "tester@test.com"},
                 201, "")
    testEndpoint("Create teacher, phone number empty", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": ""},
                 400, "Bad request")
    testEndpoint("Create teacher, phone number not string", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": ["12345"]},
                 400, "Bad request")
    testEndpoint("Create teacher, phone number too long", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345" * 4},
                 400, "Bad request")
    testEndpoint("Create teacher, phone number is not numeric", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345a"},
                 400, "Bad request")
    testEndpoint("Create teacher, wrong token", "POST", "/intezmeny/create/teacher", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 403, "Unauthorised")
    testEndpoint("Create teacher, no token", "POST", "/intezmeny/create/teacher", "",
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 400, "Bad request")
    testEndpoint("Create teacher, method not POST", "PATCH", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 405, "")
    testEndpoint("Create teacher", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 201, "")
    testEndpoint("Create teacher, teacher already exists", "POST", "/intezmeny/create/teacher", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "name": "test_teacher", "job": "test", "email": "tester@test.com", "phone_number": "12345"},
                 201, "")


    testEndpoint("Create timetable element, intezmeny does not exist", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": "636345653", "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 403, "Unauthorised")
    testEndpoint("Create timetable element, intezmeny id out of representable range of int", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": "2633246356" * 25, "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, no intezmeny id", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, intezmeny id empty", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": "", "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, intezmeny id is not string", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"], "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, intezmeny id is not numeric", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a", "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, no duration", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, invalid duration", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:2:02", "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, null byte in duration", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "\x0002:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, duration not string", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": ["02:02:02"], "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, duration overflow", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:99:02", "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, no day", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, day not string", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": ["4"], "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, not numeric", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4a", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, day larger than 6", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "7", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, day smaller than 0", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "-1", "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, day out of range of int", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4" * 4000, "from": "2020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, no from", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, invalid from", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": "2020-12-24a", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, null byte in from", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": "\x002020-12-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, from not string", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": ["2020-12-24"], "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, from overflow", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": "2020-13-24", "until": "2020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, no until", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": "2020-12-24"},
                 400, "Bad request")
    testEndpoint("Create timetable element, invalid until", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-25a"},
                 400, "Bad request")
    testEndpoint("Create timetable element, null byte in until", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "\x002020-12-25"},
                 400, "Bad request")
    testEndpoint("Create timetable element, until not string", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": ["2020-12-25"]},
                 400, "Bad request")
    testEndpoint("Create timetable element, until overflow", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-32"},
                 400, "Bad request")
    testEndpoint("Create timetable element, until is before from", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-23"},
                 400, "Bad request")
    testEndpoint("Create timetable element, until is the same day as from", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-24"},
                 201, "")
    testEndpoint("Create timetable element", "POST", "/intezmeny/create/timetable_element", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "duration": "02:02:02", "day": "4", "from": "2020-12-24", "until": "2020-12-25"},
                 201, "")

    testEndpoint("Create homework", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "1"},
                 201, "")
    testEndpoint("Create homework, already exists", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "1"},
                 201, "")
    testEndpoint("Create homework, intezmeny does not exist", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": "636345653", "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "1"},
                 403, "Unauthorised")
    testEndpoint("Create homework, intezmeny id out of representable range of int", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": "2633246356" * 25, "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, no intezmeny id", "POST", "/intezmeny/create/homework", access_jar,
                 {"due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, intezmeny id empty", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": "", "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, intezmeny id is not string", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"], "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, intezmeny id is not numeric", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a", "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, no due", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "lesson_id": "1", "teacher_id": "1"},
                 201, "")
    testEndpoint("Create homework, invalid due", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:2:02", "lesson_id": "1", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, null byte in due", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "\x002020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, due not string", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": ["2020-12-24 02:02:02"], "lesson_id": "1", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, due overflow", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:99:02", "lesson_id": "1", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, lesson does not exist", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "0", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, lesson id out of representable range of int", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "1" * 1000, "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, no lesson id", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "teacher_id": "1"},
                 201, "")
    testEndpoint("Create homework, lesson id empty", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, lesson id is not string", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": ["1"], "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, lesson id is not numeric", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "1a", "teacher_id": "1"},
                 400, "Bad request")
    testEndpoint("Create homework, teacher does not exist", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "0"},
                 400, "Bad request")
    testEndpoint("Create homework, teacher id out of representable range of int", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "1" * 1000},
                 400, "Bad request")
    testEndpoint("Create homework, no teacher id", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "1"},
                 201, "")
    testEndpoint("Create homework, teacher id empty", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "0"},
                 400, "Bad request")
    testEndpoint("Create homework, teacher id is not string", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": ["1"]},
                 400, "Bad request")
    testEndpoint("Create homework, teacher id is not numeric", "POST", "/intezmeny/create/homework", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "due": "2020-12-24 02:02:02", "lesson_id": "1", "teacher_id": "1a"},
                 400, "Bad request")
    
    testEndpoint("Create attachment, intezmeny does not exist", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": "636345653", "homework_id": "1", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 403, "Unauthorised")
    testEndpoint("Create attachment, intezmeny id out of representable range of int", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": "2633246356" * 25, "homework_id": "1", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, no intezmeny id", "POST", "/intezmeny/create/attachment", access_jar,
                 {"homework_id": "1", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, intezmeny id empty", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": "", "homework_id": "1", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, intezmeny id is not string", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"], "homework_id": "1", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, intezmeny id is not numeric", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a", "homework_id": "1", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, homework does not exist", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "0", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, homework id out of representable range of int", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1" * 1000, "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, no homework id", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, homework id empty", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, homework id is not string", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": ["1"], "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, homework id is not numeric", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1a", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, no file name", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, file name empty", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1", "file_name": "", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, file name is not string", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1", "file_name": ["test_file"], "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, file name too long", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1", "file_name": "test_file" * 50, "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment, file name with illegal character", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1", "file_name": "test_file\x00", "file_contents": "test_text test_text\ntest_text"},
                 400, "Bad request")
    testEndpoint("Create attachment", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text"},
                 201, "")
    testEndpoint("Create attachment, no file contents", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1", "file_name": "test_file"},
                 400, "Bad request")
    testEndpoint("Create attachment, file contents empty", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1", "file_name": "test_file", "file_contents": ""},
                 201, "")
    testEndpoint("Create attachment, file contents is not string", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1", "file_name": "test_file", "file_contents": ["test_text test_text\ntest_text"]},
                 400, "Bad request")
    testEndpoint("Create attachment, file contents too long", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1", "file_name": "test_file", "file_contents": "t" * 1024 * 1024 * 20 + "+"},
                 400, "Bad request")
    testEndpoint("Create attachment, file contents with null character", "POST", "/intezmeny/create/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "homework_id": "1", "file_name": "test_file", "file_contents": "test_text test_text\ntest_text\x00"},
                 201, "")


def intezmenyGetEndpoints():
    global access_jar
    global wrong_access_jar
    global intezmeny_id

    testEndpoint("Get classes", "POST", "/intezmeny/get/classes", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 200, '[["1","test_class","30"]]')
    testEndpoint("Get classes, intezmeny does not exist", "POST", "/intezmeny/get/classes", access_jar,
                 {"intezmeny_id": "347653267853"}, 403, "Unauthorised")
    testEndpoint("Get classes, intezmeny id out of representable range of int", "POST", "/intezmeny/get/classes", access_jar,
                 {"intezmeny_id": "3476532678537834698573463247856326578324685268734578635734278298673426324568325634256"}, 400, "Bad request")
    testEndpoint("Get classes, no intezmeny id", "POST", "/intezmeny/get/classes", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Get classes, intezmeny id empty", "POST", "/intezmeny/get/classes", access_jar,
                 {"intezmeny_id": ""}, 400, "Bad request")
    testEndpoint("Get classes, intezmeny id is not string", "POST", "/intezmeny/get/classes", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"]}, 400, "Bad request")
    testEndpoint("Get classes, intezmeny id is not numeric", "POST", "/intezmeny/get/classes", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a"}, 400, "Bad request")
    testEndpoint("Get classes, wrong token", "POST", "/intezmeny/get/classes", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 403, "Unauthorised")
    testEndpoint("Get classes, no token", "POST", "/intezmeny/get/classes", "",
                 {"intezmeny_id": f"{intezmeny_id}"}, 400, "Bad request")
    testEndpoint("Get classes, method not POST", "PATCH", "/intezmeny/get/classes", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 405, "")

    testEndpoint("Get lessons", "POST", "/intezmeny/get/lessons", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 200, '[["1","test_lesson"]]')
    testEndpoint("Get lessons, intezmeny does not exist", "POST", "/intezmeny/get/lessons", access_jar,
                 {"intezmeny_id": "347653267853"}, 403, "Unauthorised")
    testEndpoint("Get lessons, intezmeny id out of representable range of int", "POST", "/intezmeny/get/lessons", access_jar,
                 {"intezmeny_id": "3476532678537834698573463247856326578324685268734578635734278298673426324568325634256"}, 400, "Bad request")
    testEndpoint("Get lessons, no intezmeny id", "POST", "/intezmeny/get/lessons", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Get lessons, intezmeny id empty", "POST", "/intezmeny/get/lessons", access_jar,
                 {"intezmeny_id": ""}, 400, "Bad request")
    testEndpoint("Get lessons, intezmeny id is not string", "POST", "/intezmeny/get/lessons", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"]}, 400, "Bad request")
    testEndpoint("Get lessons, intezmeny id is not numeric", "POST", "/intezmeny/get/lessons", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a"}, 400, "Bad request")
    testEndpoint("Get lessons, wrong token", "POST", "/intezmeny/get/lessons", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 403, "Unauthorised")
    testEndpoint("Get lessons, no token", "POST", "/intezmeny/get/lessons", "",
                 {"intezmeny_id": f"{intezmeny_id}"}, 400, "Bad request")
    testEndpoint("Get lessons, method not POST", "PATCH", "/intezmeny/get/lessons", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 405, "")

    testEndpoint("Get groups", "POST", "/intezmeny/get/groups", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 200, '[["1","test_group_no_class_id","30",null,null,null],["2","test_group","30","1","test_class","30"]]')
    testEndpoint("Get groups, intezmeny does not exist", "POST", "/intezmeny/get/groups", access_jar,
                 {"intezmeny_id": "347653267853"}, 403, "Unauthorised")
    testEndpoint("Get groups, intezmeny id out of representable range of int", "POST", "/intezmeny/get/groups", access_jar,
                 {"intezmeny_id": "3476532678537834698573463247856326578324685268734578635734278298673426324568325634256"}, 400, "Bad request")
    testEndpoint("Get groups, no intezmeny id", "POST", "/intezmeny/get/groups", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Get groups, intezmeny id empty", "POST", "/intezmeny/get/groups", access_jar,
                 {"intezmeny_id": ""}, 400, "Bad request")
    testEndpoint("Get groups, intezmeny id is not string", "POST", "/intezmeny/get/groups", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"]}, 400, "Bad request")
    testEndpoint("Get groups, intezmeny id is not numeric", "POST", "/intezmeny/get/groups", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a"}, 400, "Bad request")
    testEndpoint("Get groups, wrong token", "POST", "/intezmeny/get/groups", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 403, "Unauthorised")
    testEndpoint("Get groups, no token", "POST", "/intezmeny/get/groups", "",
                 {"intezmeny_id": f"{intezmeny_id}"}, 400, "Bad request")
    testEndpoint("Get groups, method not POST", "PATCH", "/intezmeny/get/groups", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 405, "")

    testEndpoint("Get rooms", "POST", "/intezmeny/get/rooms", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 200, '[["1","test_room_no_type","test","30"],["2","test_room","test","30"]]')
    testEndpoint("Get rooms, intezmeny does not exist", "POST", "/intezmeny/get/rooms", access_jar,
                 {"intezmeny_id": "347653267853"}, 403, "Unauthorised")
    testEndpoint("Get rooms, intezmeny id out of representable range of int", "POST", "/intezmeny/get/rooms", access_jar,
                 {"intezmeny_id": "3476532678537834698573463247856326578324685268734578635734278298673426324568325634256"}, 400, "Bad request")
    testEndpoint("Get rooms, no intezmeny id", "POST", "/intezmeny/get/rooms", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Get rooms, intezmeny id empty", "POST", "/intezmeny/get/rooms", access_jar,
                 {"intezmeny_id": ""}, 400, "Bad request")
    testEndpoint("Get rooms, intezmeny id is not string", "POST", "/intezmeny/get/rooms", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"]}, 400, "Bad request")
    testEndpoint("Get rooms, intezmeny id is not numeric", "POST", "/intezmeny/get/rooms", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a"}, 400, "Bad request")
    testEndpoint("Get rooms, wrong token", "POST", "/intezmeny/get/rooms", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 403, "Unauthorised")
    testEndpoint("Get rooms, no token", "POST", "/intezmeny/get/rooms", "",
                 {"intezmeny_id": f"{intezmeny_id}"}, 400, "Bad request")
    testEndpoint("Get rooms, method not POST", "PATCH", "/intezmeny/get/rooms", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 405, "")

    testEndpoint("Get teachers", "POST", "/intezmeny/get/teachers", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 200, '[["1","test_teacher_no_email","test",null,"12345",[],[]],["2","test_teacher_no_phone","test","tester@test.com",null,[],[]],["3","test_teacher","test","tester@test.com","12345",[],[]],["4","test_teacher","test","tester@test.com","12345",[],[]]]')
    testEndpoint("Get teachers, intezmeny does not exist", "POST", "/intezmeny/get/teachers", access_jar,
                 {"intezmeny_id": "347653267853"}, 403, "Unauthorised")
    testEndpoint("Get teachers, intezmeny id out of representable range of int", "POST", "/intezmeny/get/teachers", access_jar,
                 {"intezmeny_id": "3476532678537834698573463247856326578324685268734578635734278298673426324568325634256"}, 400, "Bad request")
    testEndpoint("Get teachers, no intezmeny id", "POST", "/intezmeny/get/teachers", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Get teachers, intezmeny id empty", "POST", "/intezmeny/get/teachers", access_jar,
                 {"intezmeny_id": ""}, 400, "Bad request")
    testEndpoint("Get teachers, intezmeny id is not string", "POST", "/intezmeny/get/teachers", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"]}, 400, "Bad request")
    testEndpoint("Get teachers, intezmeny id is not numeric", "POST", "/intezmeny/get/teachers", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a"}, 400, "Bad request")
    testEndpoint("Get teachers, wrong token", "POST", "/intezmeny/get/teachers", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 403, "Unauthorised")
    testEndpoint("Get teachers, no token", "POST", "/intezmeny/get/teachers", "",
                 {"intezmeny_id": f"{intezmeny_id}"}, 400, "Bad request")
    testEndpoint("Get teachers, method not POST", "PATCH", "/intezmeny/get/teachers", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 405, "")

    testEndpoint("Get timetable", "POST", "/intezmeny/get/timetable", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 200,
                 '[["1","02:02:02","4","2020-12-24","2020-12-24",null,null,null,null],["2","02:02:02","4","2020-12-24","2020-12-25",null,null,null,null]]')
    testEndpoint("Get timetable, intezmeny does not exist", "POST", "/intezmeny/get/timetable", access_jar,
                 {"intezmeny_id": "347653267853"}, 403, "Unauthorised")
    testEndpoint("Get timetable, intezmeny id out of representable range of int", "POST", "/intezmeny/get/timetable", access_jar,
                 {"intezmeny_id": "3476532678537834698573463247856326578324685268734578635734278298673426324568325634256"}, 400, "Bad request")
    testEndpoint("Get timetable, no intezmeny id", "POST", "/intezmeny/get/timetable", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Get timetable, intezmeny id empty", "POST", "/intezmeny/get/timetable", access_jar,
                 {"intezmeny_id": ""}, 400, "Bad request")
    testEndpoint("Get timetable, intezmeny id is not string", "POST", "/intezmeny/get/timetable", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"]}, 400, "Bad request")
    testEndpoint("Get timetable, intezmeny id is not numeric", "POST", "/intezmeny/get/timetable", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a"}, 400, "Bad request")
    testEndpoint("Get timetable, wrong token", "POST", "/intezmeny/get/timetable", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 403, "Unauthorised")
    testEndpoint("Get timetable, no token", "POST", "/intezmeny/get/timetable", "",
                 {"intezmeny_id": f"{intezmeny_id}"}, 400, "Bad request")
    testEndpoint("Get timetable, method not POST", "PATCH", "/intezmeny/get/timetable", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 405, "")

    response = testEndpointNoErrorHandling("Get homeworks", "POST", "/intezmeny/get/homeworks", access_jar, {"intezmeny_id": f"{intezmeny_id}"})
    handleApiError(response, 200, '[["1","' + f"{response.json()[0][1]}" + '","2020-12-24 02:02:02","test_lesson","test_teacher_no_email",[[1,"test_file"],[2,"test_file"],[3,"test_file"]]],["2","' + f"{response.json()[1][1]}" + '","2020-12-24 02:02:02","test_lesson","test_teacher_no_email",[]],["3","' + f"{response.json()[2][1]}" + '",null,"test_lesson","test_teacher_no_email",[]],["4","' + f"{response.json()[3][1]}" + '","2020-12-24 02:02:02",null,"test_teacher_no_email",[]],["5","' + f"{response.json()[4][1]}" + '","2020-12-24 02:02:02","test_lesson",null,[]]]')
    testEndpoint("Get homeworks, intezmeny does not exist", "POST", "/intezmeny/get/homeworks", access_jar,
                 {"intezmeny_id": "347653267853"}, 403, "Unauthorised")
    testEndpoint("Get homeworks, intezmeny id out of representable range of int", "POST", "/intezmeny/get/homeworks", access_jar,
                 {"intezmeny_id": "3476532678537834698573463247856326578324685268734578635734278298673426324568325634256"}, 400, "Bad request")
    testEndpoint("Get homeworks, no intezmeny id", "POST", "/intezmeny/get/homeworks", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Get homeworks, intezmeny id empty", "POST", "/intezmeny/get/homeworks", access_jar,
                 {"intezmeny_id": ""}, 400, "Bad request")
    testEndpoint("Get homeworks, intezmeny id is not string", "POST", "/intezmeny/get/homeworks", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"]}, 400, "Bad request")
    testEndpoint("Get homeworks, intezmeny id is not numeric", "POST", "/intezmeny/get/homeworks", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a"}, 400, "Bad request")
    testEndpoint("Get homeworks, wrong token", "POST", "/intezmeny/get/homeworks", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 403, "Unauthorised")
    testEndpoint("Get homeworks, no token", "POST", "/intezmeny/get/homeworks", "",
                 {"intezmeny_id": f"{intezmeny_id}"}, 400, "Bad request")
    testEndpoint("Get homeworks, method not POST", "PATCH", "/intezmeny/get/homeworks", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 405, "")

    testEndpoint("Get attachment", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "attachment_id": "1"}, 200, "test_text test_text\ntest_text")
    testEndpoint("Get attachment, intezmeny does not exist", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": "347653267853", "attachment_id": "0"}, 403, "Unauthorised")
    testEndpoint("Get attachment, intezmeny id out of representable range of int", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": "34765326785" * 25, "attachment_id": "0"}, 400, "Bad request")
    testEndpoint("Get attachment, no intezmeny id", "POST", "/intezmeny/get/attachment", access_jar,
                 {"attachment_id": "0"}, 400, "Bad request")
    testEndpoint("Get attachment, intezmeny id empty", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": "", "attachment_id": "0"}, 400, "Bad request")
    testEndpoint("Get attachment, intezmeny id is not numeric", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a", "attachment_id": "0"}, 400, "Bad request")
    testEndpoint("Get attachment, intezmeny id is not string", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"], "attachment_id": "0"}, 400, "Bad request")
    testEndpoint("Get attachment, attachment does not exist", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "attachment_id": "25327823"}, 400, "Bad request")
    testEndpoint("Get attachment, attachment id out of representable range of int", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "attachment_id": "7259345518397" * 25}, 400, "Bad request")
    testEndpoint("Get attachment, no attachment id", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 400, "Bad request")
    testEndpoint("Get attachment, attachment id empty", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "attachment_id": ""}, 400, "Bad request")
    testEndpoint("Get attachment, intezmeny id is not string", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "attachment_id": ["0"]}, 400, "Bad request")
    testEndpoint("Get attachment, intezmeny id is not numeric", "POST", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "attachment_id": "0a"}, 400, "Bad request")
    testEndpoint("Get attachment, wrong token", "POST", "/intezmeny/get/attachment", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "attachment_id": "0"}, 403, "Unauthorised")
    testEndpoint("Get attachment, no token", "POST", "/intezmeny/get/attachment", "",
                 {"intezmeny_id": f"{intezmeny_id}", "attachment_id": "0"}, 400, "Bad request")
    testEndpoint("Get attachment, method not POST", "PATCH", "/intezmeny/get/attachment", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}", "attachment_id": "0"}, 405, "")


def deleteIntezmeny():            
    global access_jar
    global wrong_access_jar
    global intezmeny_id

    testEndpoint("Delete intezmeny", "DELETE", "/delete_intezmeny", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 204, "")
    testEndpoint("Delete intezmeny, intezmeny does not exist", "DELETE", "/delete_intezmeny", access_jar,
                 {"intezmeny_id": "7832678563"}, 403, "Unauthorised")
    testEndpoint("Delete intezmeny, intezmeny id out of range of int", "DELETE", "/delete_intezmeny", access_jar,
                 {"intezmeny_id": "7832678563" * 10}, 400, "Bad request")
    testEndpoint("Delete intezmeny, no intezmeny id", "DELETE", "/delete_intezmeny", access_jar,
                 {}, 400, "Bad request")
    testEndpoint("Delete intezmeny, intezmeny id empty", "DELETE", "/delete_intezmeny", access_jar,
                 {"intezmeny_id": ""}, 400, "Bad request")
    testEndpoint("Delete intezmeny, intezmeny id is not string", "DELETE", "/delete_intezmeny", access_jar,
                 {"intezmeny_id": [f"{intezmeny_id}"]}, 400, "Bad request")
    testEndpoint("Delete intezmeny, intezmeny id is not numeric", "DELETE", "/delete_intezmeny", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}a"}, 400, "Bad request")
    testEndpoint("Delete intezmeny, wrong token", "DELETE", "/delete_intezmeny", wrong_access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 403, "Unauthorised")
    testEndpoint("Delete intezmeny, no token", "DELETE", "/delete_intezmeny", "",
                 {"intezmeny_id": f"{intezmeny_id}"}, 400, "Bad request")
    testEndpoint("Delete intezmeny, method is not DELETE", "PATCH", "/delete_intezmeny", access_jar,
                 {"intezmeny_id": f"{intezmeny_id}"}, 405, "")


def deleteUser():
    global access_jar
    global wrong_access_jar

    testEndpoint("Delete user, wrong token", "DELETE", "/user/delete_user", wrong_access_jar, {}, 403, "Unauthorised")
    testEndpoint("Delete user, no token", "DELETE", "/user/delete_user", "", {}, 400, "Bad request")
    testEndpoint("Delete user, method is not DELETE", "PATCH", "/user/delete_user", access_jar, {}, 405, "")
    testEndpoint("Delete user", "DELETE", "/user/delete_user", access_jar, {}, 204, "")
    testEndpoint("Delete user, user does not exist", "DELETE", "/user/delete_user", access_jar, {}, 400, "User does not exist")


def cleanup():
    no_phone_refresh_jar = dict()
    no_phone_access_jar = dict()
    
    no_phone_refresh_jar = testEndpoint("Get refresh token for no phone user", "POST", "/token/get_refresh_token", "",
                 {"email": "tester_no_phone@test.com", "pass": "tester_pass"}, 200, "").cookies
    no_phone_access_jar = testEndpoint("Get access token for no phone user", "POST", "/token/get_access_token", no_phone_refresh_jar, {}, 200, "").cookies
    testEndpoint("Delete no phone number user", "DELETE", "/user/delete_user", no_phone_access_jar, {}, 204, "")


main()
    
