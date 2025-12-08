<?php

include "main_db.php";

class UserController
{
    /**
     * Returns null on failure and users in json format on success
     */
    public function getAllUsers(): mixed
    {
        if (!isset($_GET["intezmeny_id"]) or intval($_GET["intezmeny_id"]) === 0) {
            return null;
        }

        $intezmeny_id = intval($_GET["intezmeny_id"]);

        $main_db = new MainDb();
        $res = $main_db->getAllUsers($intezmeny_id);

        return json_encode($res->fetch_all());
    }
    public function createUser(): CreateUserRet
    {
        $data = json_decode(file_get_contents("php://input"));

        if (
            !isset($data->disp_name) or !is_string($data->disp_name) or !isset($data->email) or !is_string($data->email) or
            !isset($data->pass_hash) or !is_string($data->pass_hash) or strlen($data->pass_hash) != 60
        ) {
            return CreateUserRet::bad_request;
        }

        $phone_number = null;
        if (isset($data->phone_number)) {
            if (strlen($data->phone_number) > 15) {
                return CreateUserRet::bad_request;
            }
            $phone_number = intval($data->phone_number);
            if ($phone_number === 0) {
                return CreateUserRet::bad_request;
            }
        }

        $main_db = new MainDb();

        if ($main_db->userExistsEmail($data->email)) {
            return CreateUserRet::user_already_exists;
        }

        if (!$main_db->createUser($data->disp_name, $data->email, $phone_number, $data->pass_hash)) {
            return CreateUserRet::unexpected_error;
        }

        return CreateUserRet::success;
    }

    public function deleteUser(): DeleteUserRet
    {
        $data = json_decode(file_get_contents("php://input"));

        $main_db = new MainDb();

        if (!isset($data->email) or !isset($data->pass_hash) or !is_string($data->email) or !is_string($data->pass_hash) or strlen($data->pass_hash) != 60) {
            return DeleteUserRet::bad_request;
        }

        if (!$main_db->userExistsEmail($data->email)) {
            return DeleteUserRet::user_does_not_exist;
        }

        $user_pass = $main_db->getUserPassViaEmail($data->email)->fetch_all()[0][0];

        if (!$user_pass or $user_pass !== $data->pass_hash) {
            return DeleteUserRet::unauthorised;
        }

        if (!$main_db->deleteUserViaEmail($data->email)) {
            return DeleteUserRet::unexpected_error;
        }

        return DeleteUserRet::success;
    }
}

enum CreateUserRet
{
    case success;
    case bad_request;
    case user_already_exists;
    case unexpected_error;
}

enum DeleteUserRet
{
    case success;
    case bad_request;
    case user_does_not_exist;
    case unauthorised;
    case unexpected_error;
}
