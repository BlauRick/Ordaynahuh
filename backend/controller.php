<?php

declare(strict_types=1);
// TODO: Rewrite getAllUsers

static $is_test_server = php_sapi_name() === "cli-server";

use Lcobucci\JWT\Token\RegisteredClaims;
use Lcobucci\JWT\UnencryptedToken;

include "db.php";
include "jwt.php";

class UserController
{
    private $jwt;

    function __construct()
    {
        $this->jwt = new JWT();
    }

    /**
     * Returns null on failure and users in json format on success
     */
    public function getAllUsers(): mixed
    {
        if (!isset($_GET["intezmeny_id"]) or intval($_GET["intezmeny_id"]) === 0) {
            return null;
        }

        $intezmeny_id = intval($_GET["intezmeny_id"]);

        $db = new DB();
        $res = $db->getAllUsers($intezmeny_id);

        header('Content-Type: application/json');
        return json_encode($res->fetch_all());
    }

    public function getRefreshToken(): ControllerRet
    {
        global $is_test_server;

        $data = json_decode(file_get_contents("php://input"));
        $email = $this->validateEmail(@$data->email);
        if ($email === null) return ControllerRet::bad_request;
        $pass = $this->validateString(@$data->pass, min_chars: 8);
        if ($pass === null) return ControllerRet::bad_request;

        $db = new DB();

        if (!$db->userExistsEmail($email)) return ControllerRet::user_does_not_exist;

        $user_pass = $db->getUserPassViaEmail($email);
        if (!$user_pass or !password_verify($pass, $user_pass)) return ControllerRet::unauthorised;

        $user_id = $db->getUserIdViaEmail($email);
        $refresh_token = $this->jwt->createRefreshToken($user_id);

        $arr_cookie_options = array(
            'expires' => time() + 60 * 60 * 24 * 15,
            'path' => '/token/',
            'domain' => '',
            'secure' => !$is_test_server,
            'httponly' => true,
            'samesite' => 'Strict'
        );
        setcookie('RefreshToken', $refresh_token->toString(), $arr_cookie_options);

        return ControllerRet::success;
    }

    public function refreshRefreshToken(): ControllerRet
    {
        global $is_test_server;
        $db = new DB();

        $token = $this->validateRefreshToken($db);
        if (is_a($token, "ControllerRet")) return $token;
        $new_token = $this->jwt->createRefreshToken($token->claims()->get("uid"));

        // Expires after 15 days
        $db->newInvalidRefreshToken($token->claims()->get(RegisteredClaims::ID), '15 0:0:0');

        $arr_cookie_options = array(
            // 15 days
            'expires' => time() + 60 * 60 * 24 * 15,
            'path' => '/token/',
            'domain' => '',
            'secure' => !$is_test_server,
            'httponly' => true,
            'samesite' => 'Strict'
        );
        setcookie('RefreshToken', $new_token->toString(), $arr_cookie_options);

        return ControllerRet::success;
    }

    public function getAccessToken(): ControllerRet
    {
        global $is_test_server;
        $db = new DB();

        $token = $this->validateRefreshToken($db);
        if (is_a($token, "ControllerRet")) return $token;
        $new_access_token = $this->jwt->createAccessToken($token->claims()->get("uid"));

        $arr_cookie_options = array(
            // 10 minutes
            'expires' => time() + 60 * 10,
            'path' => '/',
            'domain' => '',
            'secure' => !$is_test_server,
            'httponly' => true,
            'samesite' => 'Strict'
        );
        setcookie('AccessToken', $new_access_token->toString(), $arr_cookie_options);

        return ControllerRet::success;
    }

    public function createUser(): ControllerRet
    {
        $data = json_decode(file_get_contents("php://input"));
        $disp_name = $this->validateString(@$data->disp_name, max_chars: 200);
        if ($disp_name === null) return ControllerRet::bad_request;
        $email = $this->validateEmail(@$data->email);
        if ($email === null) return ControllerRet::bad_request;
        $pass = $this->validateString(@$data->pass, min_chars: 8);
        if ($pass === null) return ControllerRet::bad_request;

        $phone_number = null;
        if (isset($data->phone_number)) {
            $phone_number = $this->validateInteger(@$data->phone_number, 15);
            if ($phone_number === null) return ControllerRet::bad_request;
        }

        $db = new DB();

        if ($db->userExistsEmail($email)) return ControllerRet::user_already_exists;

        $pass_hash = password_hash($pass, PASSWORD_BCRYPT);
        if (!$db->createUser($disp_name, $email, $phone_number, $pass_hash)) return ControllerRet::unexpected_error;

        return ControllerRet::success_created;
    }

    public function deleteUser(): ControllerRet
    {
        $token = $this->validateAccessToken();
        if (is_a($token, "ControllerRet")) return $token;

        $db = new DB();

        if (!$db->userExistsViaId($token->claims()->get("uid"))) return ControllerRet::user_does_not_exist;

        // TODO: delete intezmeny's whose sole owner is this user
        if (!$db->deleteUserViaId($token->claims()->get("uid"))) return ControllerRet::unexpected_error;

        // Unset token cookies
        setcookie('RefreshToken', "", 0);
        setcookie('AccessToken', "", 0);

        return ControllerRet::success_no_content;
    }

    public function changeDisplayName(): ControllerRet
    {
        $data = json_decode(file_get_contents("php://input"));
        $new_disp_name = $this->validateString(@$data->new_disp_name, max_chars: 200);
        if ($new_disp_name === null) return ControllerRet::bad_request;

        $token = $this->validateAccessToken();
        if (is_a($token, "ControllerRet")) return $token;

        $db = new DB();

        if (!$db->userExistsViaId($token->claims()->get("uid"))) return ControllerRet::user_does_not_exist;

        if (!$db->changeDisplayNameViaId($token->claims()->get("uid"), $new_disp_name)) return ControllerRet::unexpected_error;

        return ControllerRet::success_no_content;
    }

    public function changePhoneNumber(): ControllerRet
    {
        $data = json_decode(file_get_contents("php://input"));
        $new_phone_number = $this->validateInteger(@$data->new_phone_number, 15);
        if ($new_phone_number === null) return ControllerRet::bad_request;

        $token = $this->validateAccessToken();
        if (is_a($token, "ControllerRet")) return $token;

        $db = new DB();

        if (!$db->userExistsViaId($token->claims()->get("uid"))) return ControllerRet::user_does_not_exist;

        if (!$db->changePhoneNumberViaId($token->claims()->get("uid"), $data->new_phone_number)) return ControllerRet::unexpected_error;

        return ControllerRet::success_no_content;
    }

    // TODO: Ask for the old password
    public function changePassword(): ControllerRet
    {
        $data = json_decode(file_get_contents("php://input"));
        $new_pass = $this->validateString(@$data->new_pass, min_chars: 8);
        if ($new_pass === null) return ControllerRet::bad_request;

        $token = $this->validateAccessToken();
        if (is_a($token, "ControllerRet")) return $token;

        $db = new DB();

        if (!$db->userExistsViaId($token->claims()->get("uid"))) return ControllerRet::user_does_not_exist;

        if (!$db->changePasswordHashViaId($token->claims()->get("uid"), password_hash($new_pass, PASSWORD_BCRYPT))) return ControllerRet::unexpected_error;

        return ControllerRet::success_no_content;
    }

    public function createIntezmeny(): ControllerRet
    {
        $data = json_decode(file_get_contents("php://input"));
        $intezmeny_name = $this->validateString(@$data->intezmeny_name, max_chars: 200);
        if ($intezmeny_name === null) return ControllerRet::bad_request;

        $token = $this->validateAccessToken();
        if (is_a($token, "ControllerRet")) return $token;

        $db = new DB();

        if (!$db->userExistsViaId($token->claims()->get("uid"))) return ControllerRet::user_does_not_exist;

        if (! $db->createIntezmeny($intezmeny_name, $token->claims()->get("uid"))) return ControllerRet::unexpected_error;

        return ControllerRet::success_created;
    }

    public function deleteIntezmeny(): ControllerRet
    {
        $data = json_decode(file_get_contents("php://input"));
        $intezmeny_id = $this->validateInteger(@$data->intezmeny_id);
        if ($intezmeny_id === null) return ControllerRet::bad_request;

        $token = $this->validateAccessToken();
        if (is_a($token, "ControllerRet")) return $token;

        $db = new DB();

        if (!$db->userExistsViaId($token->claims()->get("uid"))) return ControllerRet::user_does_not_exist;
        if (!$db->partOfIntezmeny($token->claims()->get("uid"), $intezmeny_id)) return ControllerRet::unauthorised;

        if (!$db->deleteIntezmeny($intezmeny_id)) return ControllerRet::unexpected_error;

        return ControllerRet::success_no_content;
    }

    public function getIntezmenys(): ControllerRet
    {
        $token = $this->validateAccessToken();
        if (is_a($token, "ControllerRet")) return $token;

        $db = new DB();

        if (!$db->userExistsViaId($token->claims()->get("uid"))) return ControllerRet::user_does_not_exist;

        $ret = $db->getIntezmenys($token->claims()->get("uid"));
        if (!$ret) return ControllerRet::unexpected_error;

        header('Content-Type: application/json');
        echo json_encode($ret->fetch_all());

        return ControllerRet::success;
    }

    public function getClasses(): ControllerRet
    {
        $data = json_decode(file_get_contents("php://input"));
        $intezmeny_id = $this->validateInteger(@$data->intezmeny_id);
        if ($intezmeny_id === null) return ControllerRet::bad_request;

        $token = $this->validateAccessToken();
        if (is_a($token, "ControllerRet")) return $token;

        $db = new DB();

        if (!$db->userExistsViaId($token->claims()->get("uid"))) {
            return ControllerRet::user_does_not_exist;
        }

        if (!$db->partOfIntezmeny($token->claims()->get("uid"), $intezmeny_id)) {
            return ControllerRet::unauthorised;
        }

        $ret = $db->getClasses($intezmeny_id);
        if (!$ret) {
            return ControllerRet::unexpected_error;
        }

        header('Content-Type: application/json');
        echo json_encode($ret->fetch_all());

        return ControllerRet::success;
    }

    function validateRefreshToken(DB $db): ControllerRet|UnencryptedToken
    {
        if (!isset($_COOKIE["RefreshToken"]) or !is_string($_COOKIE["RefreshToken"])) return ControllerRet::bad_request;

        $token = $this->jwt->parseToken($_COOKIE["RefreshToken"]);
        if ($token === null) return ControllerRet::bad_request;

        $invalid_ids = $db->getRevokedRefreshTokens();
        if (!$this->jwt->validateRefreshToken($token, $invalid_ids)) return ControllerRet::unauthorised;

        return $token;
    }

    function validateAccessToken(): ControllerRet|UnencryptedToken
    {
        if (!isset($_COOKIE["AccessToken"]) or !is_string($_COOKIE["AccessToken"])) return ControllerRet::bad_request;

        $token = $this->jwt->parseToken($_COOKIE["AccessToken"]);
        if ($token === null) return ControllerRet::bad_request;

        if (!$this->jwt->validateAccessToken($token)) return ControllerRet::unauthorised;

        return $token;
    }

    // This function handles the case where $number is undefined
    // It's expected that $number is passed in with the "@" stfu operator
    function validateInteger(mixed $number, int|null $max_digits = null): int|null
    {
        if (!isset($number) or !is_string($number) or !is_numeric($number)) return null;
        if ($max_digits !== null and strlen($number) > $max_digits) return null;
        $int = intval($number);
        if (($int >= PHP_INT_MAX and $number !== strval(PHP_INT_MAX)) or ($int === 0 and $number !== "0")) return null;
        return $int;
    }

    // This function handles the case where $string is undefined
    // It's expected that $string is passed in with the "@" stfu operator
    function validateString(mixed $string, int $min_chars = 1, int|null $max_chars = null): string|null
    {
        if (!isset($string) or !is_string($string) or strlen($string) < $min_chars or ($max_chars !== null and strlen($string) > $max_chars)) return null;
        return (string) $string;
    }

    // This function handles the case where $email is undefined
    // It's expected that $email is passed in with the "@" stfu operator
    function validateEmail(mixed $email): string|null
    {
        if (!isset($email) or !is_string($email) or !preg_match('/^[^@]+[@]+[^@]+$/', $email)) return null;
        return (string) $email;
    }
}

function handleReturn(ControllerRet $ret_val): void
{
    switch ($ret_val) {
        case ControllerRet::success:
            http_response_code(200);
            break;
        case ControllerRet::success_created:
            http_response_code(201);
            break;
        case ControllerRet::success_no_content:
            http_response_code(204);
            break;
        case ControllerRet::bad_request:
            http_response_code(400);
            echo "Bad request";
            break;
        case ControllerRet::user_does_not_exist:
            http_response_code(400);
            echo "User does not exist";
            break;
        case ControllerRet::user_already_exists:
            http_response_code(400);
            echo "User already exists";
            break;
        case ControllerRet::unauthorised:
            http_response_code(403);
            echo "Unauthorised";
            break;
        case ControllerRet::unexpected_error:
            http_response_code(500);
            echo "Unexpected error";
            break;
    }
}

enum ControllerRet
{
    case success;
    case success_created;
    case success_no_content;
    case bad_request;
    case unauthorised;
    case user_does_not_exist;
    case user_already_exists;
    case unexpected_error;
}
