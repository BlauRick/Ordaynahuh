<?php

declare(strict_types=1);

require 'vendor/autoload.php';

include "controller.php";
$user_controller = new UserController();

$req_uri = explode("/", explode("?", $_SERVER["REQUEST_URI"])[0]);

if (count($req_uri) <= 1) {
    if ($_SERVER["REQUEST_METHOD"] != "GET") {
        http_response_code(405);
        return;
    }
    include "../base/index.php";
    http_response_code(200);
    return;
}

switch ($req_uri[1]) {
    case "":
        if ($_SERVER["REQUEST_METHOD"] != "GET") {
            http_response_code(405);
            break;
        }
        include "../base/index.php";
        http_response_code(200);
        break;
    case "login":
        if ($_SERVER["REQUEST_METHOD"] != "GET") {
            http_response_code(405);
            break;
        }
        include "../base/login.php";
        http_response_code(200);
        break;
    case "signup":
        if ($_SERVER["REQUEST_METHOD"] != "GET") {
            http_response_code(405);
            break;
        }
        include "../base/signup.php";
        http_response_code(200);
        break;
    case "get_all_users":
        if ($_SERVER["REQUEST_METHOD"] != "GET") {
            http_response_code(405);
            break;
        }
        $res = $user_controller->getAllUsers();
        if ($res == null) {
            http_response_code(400);
            break;
        }
        echo $res;
        http_response_code(200);
        break;
    case "token":
        if (count($req_uri) <= 2) {
            http_response_code(404);
            break;
        }
        if ($_SERVER["REQUEST_METHOD"] != "POST") {
            http_response_code(405);
            break;
        }

        $res;
        switch ($req_uri[2]) {
            case "get_refresh_token":
                $res = $user_controller->getRefreshToken();
                break;
            case "refresh_refresh_token":
                $res = $user_controller->refreshRefreshToken();
                break;
            case "get_access_token":
                $res = $user_controller->getAccessToken();
                break;
            default:
                http_response_code(404);
                return;
        }
        handleReturn($res);
        break;
    case "user":
        if (count($req_uri) <= 2) {
            http_response_code(404);
            break;
        }

        $res;
        switch ($req_uri[2]) {
            case "create_user":
                if ($_SERVER["REQUEST_METHOD"] != "POST") {
                    http_response_code(405);
                    break;
                }
                $res = $user_controller->createUser();
                break;
            case "delete_user":
                if ($_SERVER["REQUEST_METHOD"] != "DELETE") {
                    http_response_code(405);
                    break;
                }
                $res = $user_controller->deleteUser();
                break;
            case "change_disp_name":
                if ($_SERVER["REQUEST_METHOD"] != "POST") {
                    http_response_code(405);
                    break;
                }
                $res = $user_controller->changeDisplayName();
                break;
            case "change_phone_number":
                if ($_SERVER["REQUEST_METHOD"] != "POST") {
                    http_response_code(405);
                    break;
                }
                $res = $user_controller->changePhoneNumber();
                break;
            case "change_pass":
                if ($_SERVER["REQUEST_METHOD"] != "POST") {
                    http_response_code(405);
                    break;
                }
                $res = $user_controller->changePassword();
                break;
            default:
                http_response_code(404);
                return;
        }
        handleReturn($res);
        break;
    case "create_intezmeny":
        if ($_SERVER["REQUEST_METHOD"] != "POST") {
            http_response_code(405);
            break;
        }
        handleReturn($user_controller->createIntezmeny());
        break;
    case "delete_intezmeny":
        if ($_SERVER["REQUEST_METHOD"] != "DELETE") {
            http_response_code(405);
            break;
        }
        handleReturn($user_controller->deleteIntezmeny());
        break;
    case "get_intezmenys":
        if ($_SERVER["REQUEST_METHOD"] != "GET") {
            http_response_code(405);
            break;
        }
        handleReturn($user_controller->getIntezmenys());
        break;
    case "intezmeny":
        if (count($req_uri) <= 2) {
            http_response_code(404);
            break;
        }
        if ($_SERVER["REQUEST_METHOD"] != "POST") {
            http_response_code(405);
            break;
        }

        $res;
        switch ($req_uri[2]) {
            case "get_classes":
                $res = $user_controller->getClasses();
                break;
            case "get_groups":
                $res = $user_controller->getGroups();
                break;
            case "get_lessons":
                $res = $user_controller->getLessons();
                break;
            case "get_rooms":
                $res = $user_controller->getRooms();
                break;
            case "get_teachers":
                $res = $user_controller->getTeachers();
                break;
            case "get_timetable":
                $res = $user_controller->getTimetable();
                break;
            case "get_homeworks":
                $res = $user_controller->getHomeworks();
                break;
            case "get_attachments":
                $res = $user_controller->getAttachments();
                break;
            default:
                http_response_code(404);
                return;
        }
        handleReturn($res);
        break;
    default:
        http_response_code(404);
        break;
}
