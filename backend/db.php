<?php
declare(strict_types=1);

class DB
{
    private $connection = null;

    public function __construct()
    {
        $databaseHost = 'localhost';
        $databaseUsername = 'ordayna_main';
        $databasePassword = '';
        $databaseName = '';

        $this->connection = mysqli_connect($databaseHost, $databaseUsername, $databasePassword, $databaseName);
    }

    function getAllUsers(int $intezmeny_id): mysqli_result|bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    SELECT display_name, email, phone_number FROM intezmeny_ids
                    LEFT JOIN intezmeny_ids_users ON intezmeny_ids_id = intezmeny_ids.id
                    LEFT JOIN users ON users_id = users.id

                    WHERE intezmeny_ids.intezmeny_id = ?
                    ;
                ',
                array($intezmeny_id),
            );
        } catch (Exception $e) {
            return false;
        }
    }

    function getUserIdViaEmail(string $email): int|bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    SELECT id FROM users WHERE email = ?;
                ',
                array($email),
            )->fetch_all()[0][0];
        } catch (Exception $e) {
            return false;
        }
    }

    function getUserPassViaEmail(string $email): string|bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    SELECT password_hash FROM users WHERE email = ?;
                ',
                array($email),
            )->fetch_all()[0][0];
        } catch (Exception $e) {
            return false;
        }
    }

    function userExistsEmail(string $email): bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    SELECT EXISTS(SELECT * FROM users WHERE email = ?)
                ',
                array($email)
            )->fetch_all()[0][0] === 1;
        } catch (Exception $e) {
            return false;
        }
    }

    function userExistsViaId(int $uid): bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    SELECT EXISTS(SELECT * FROM users WHERE id = ?)
                ',
                array($uid)
            )->fetch_all()[0][0] === 1;
        } catch (Exception $e) {
            return false;
        }
    }

    /**
     * Assumes the user doesn't exist
     * Returns true on success and false on error
     * phone_number is either a string or null
     */
    function createUser(string $display_name, string $email, mixed $phone_number, string $password_hash): bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    INSERT INTO ordayna_main_db.users (display_name, email, phone_number, password_hash) VALUE (?,?,?,?);
                ',
                array($display_name, $email, $phone_number, $password_hash)
            );
        } catch (Exception $e) {
            return false;
        }
    }

    /**
     * Assumes the user exists
     * Returns true on success and false on error
     */
    function deleteUserViaId(int $uid): bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    DELETE FROM users WHERE id = ?;
                ',
                array($uid),
            );
        } catch (Exception $e) {
            return false;
        }
    }

    /**
     * Assumes the user exists
     * Returns true on success and false on error
     */
    function changeDisplayNameViaId(int $uid, string $new_disp_name): bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    UPDATE users SET display_name = ? WHERE id = ?;
                ',
                array($new_disp_name, $uid),
            );
        } catch (Exception $e) {
            return false;
        }
    }

    /**
     * Assumes the user exists
     * Returns true on success and false on error
     */
    function changePhoneNumberViaId(int $uid, string $new_phone_number): bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    UPDATE users SET phone_number = ? WHERE id = ?;
                ',
                array($new_phone_number, $uid),
            );
        } catch (Exception $e) {
            return false;
        }
    }

    /**
     * Assumes the user exists
     * Returns true on success and false on error
     */
    function changePasswordHashViaId(int $uid, string $new_pass_hash): bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    UPDATE users SET password_hash = ? WHERE id = ?;
                ',
                array($new_pass_hash, $uid),
            );
        } catch (Exception $e) {
            return false;
        }
    }

    function getRevokedRefreshTokens(): array|bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            $res = $this->connection->execute_query(
                '
                    SELECT uuid FROM revoked_refresh_tokens;
                '
            )->fetch_all();

            $ret_arr = array();
            for ($i = 0; $i < count($res); $i++) {
                array_push($ret_arr, $res[$i][0]);
            }

            return $ret_arr;
        } catch (Exception $e) {
            return false;
        }
    }

    /**
     * Returns true on success and false on error
     */
    function newInvalidRefreshToken(string $uuid, string $expires_after): bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    INSERT INTO revoked_refresh_tokens (uuid, duration) VALUE (?, ?);
                ',
                array($uuid, $expires_after)
            );
        } catch (Exception $e) {
            return false;
        }
    }

    function partOfIntezmeny(int $uid, int $intezmeny_id): bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            return $this->connection->execute_query(
                '
                    SELECT EXISTS(
                        SELECT * FROM users
                        INNER JOIN intezmeny_users ON intezmeny_users.users_id = users.id
                        INNER JOIN intezmeny ON intezmeny_users.intezmeny_id = intezmeny.id
                        WHERE users.id = ? AND intezmeny.id = ?
                    );
                ',
                array($uid, $intezmeny_id)
            )->fetch_all()[0][0] === 1;
        } catch (Exception $e) {
            return false;
        }
    }

    function getIntezmenys(int $uid): mysqli_result|bool
    {
        try {
            $ret = $this->connection->query('USE ordayna_main_db');
            if ($ret === false) return false;
            // return $this->connection->query("SELECT name FROM lesson;");
            return $this->connection->execute_query(
                '
                    SELECT intezmeny.id, intezmeny.name FROM users
                    INNER JOIN intezmeny_users ON intezmeny_users.users_id = users.id
                    INNER JOIN intezmeny ON intezmeny_users.intezmeny_id = intezmeny.id
                    WHERE users.id = ?;
                ',
                array($uid)
            );
        } catch (Exception $e) {
            return false;
        }
    }

    function getClasses(int $intezmeny_id): mysqli_result|bool
    {
        try {
            $ret = $this->connection->query('USE ordayna_intezmeny_' . $intezmeny_id);
            if ($ret === false) return false;
            return $this->connection->query("SELECT name FROM lesson;");
        } catch (Exception $e) {
            return false;
        }
    }

    function createIntezmeny(string $intezmeny_name, int $admin_uid): bool
    {
        try {
            $ret = $this->connection->query('USE ordayna_main_db;');
            if ($ret === false) return false;
            $intezmeny_id = $this->connection->query('SELECT IFNULL(MAX(id)+1, 0) FROM intezmeny;')->fetch_all()[0][0];
            $ret = $this->connection->execute_query(
                '
                    SET @intezmeny_name = ?;
                ',
                array($intezmeny_name)
            );
            if ($ret === false) return false;
            $ret = $this->connection->multi_query(
                '
                    SET @admin_uid = ' . $admin_uid . ';
                    SET @intezmeny_id = (SELECT IFNULL(MAX(id)+1, 0) FROM intezmeny);
                    
                	-- This allows us to replace the database without encountering foreign key errors
                	SET FOREIGN_KEY_CHECKS = 0;
                	CREATE OR REPLACE DATABASE ordayna_intezmeny_' . $intezmeny_id . ' CHARACTER SET = "utf8mb4" COLLATE = "utf8mb4_uca1400_ai_ci";
                	SET FOREIGN_KEY_CHECKS = 1;

                	INSERT INTO intezmeny (id, name) VALUE (@intezmeny_id, @intezmeny_name);
                	INSERT INTO intezmeny_users (intezmeny_id, users_id) VALUE (@intezmeny_id, @admin_uid);
                    
                	USE ordayna_intezmeny_' . $intezmeny_id . ';
                	
                	CREATE OR REPLACE TABLE class ( 
                		id                   INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                		name                 VARCHAR(200) UNIQUE NOT NULL,
                		headcount            SMALLINT UNSIGNED NOT NULL
                	 ) ENGINE=InnoDB;
                	
                	CREATE OR REPLACE TABLE group_ ( 
                		id                   INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                		name                 VARCHAR(200) UNIQUE NOT NULL,
                		headcount            SMALLINT UNSIGNED NOT NULL,
                		class_id             INT UNSIGNED,
                		CONSTRAINT fk_group_class FOREIGN KEY ( class_id ) REFERENCES class( id ) ON DELETE SET NULL ON UPDATE NO ACTION
                	 ) ENGINE=InnoDB;
                	
                	CREATE OR REPLACE INDEX fk_group_class ON group_ ( class_id );
                	
                	CREATE OR REPLACE TABLE lesson ( 
                		id                   INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                		name                 VARCHAR(200) UNIQUE NOT NULL   
                	 ) ENGINE=InnoDB;
                	
                	CREATE OR REPLACE TABLE room ( 
                		id                   INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                		name                 VARCHAR(200) UNIQUE NOT NULL,
                		room_type            VARCHAR(200),
                		space                INT UNSIGNED NOT NULL
                	 ) ENGINE=InnoDB;
                	
                	-- TODO: connect teacher with lesson via a connecting table
                	
                	CREATE OR REPLACE TABLE teacher ( 
                		id                   INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                		name                 VARCHAR(200) UNIQUE NOT NULL,
                		job                  VARCHAR(200) NOT NULL,
                		email                VARCHAR(254),
                		phone_number         VARCHAR(15)       
                	 ) ENGINE=InnoDB;
                	
                	CREATE OR REPLACE TABLE teacher_lesson (
                	  teacher_id INT UNSIGNED NOT NULL,
                	  lesson_id INT UNSIGNED NOT NULL,
                	  CONSTRAINT fk_lesson_teacher FOREIGN KEY (lesson_id) REFERENCES lesson (id) ON DELETE CASCADE ON UPDATE NO ACTION,
                	  CONSTRAINT fk_teacher_lesson FOREIGN KEY (teacher_id) REFERENCES teacher (id) ON DELETE CASCADE ON UPDATE NO ACTION
                	) ENGINE=InnoDB;
                	
                	ALTER TABLE teacher MODIFY email VARCHAR(254) COMMENT \'The max length of a valid email address is technically 320 but you can\'\'t really use that due to the limit of the mailbox being 256 bytes (254 due to it always including a < and > bracket).
                	https://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address\';
                	
                	ALTER TABLE teacher MODIFY phone_number VARCHAR(15) COMMENT \'The max length of a phone number is 15 digits (not including the "+" sign and any spaces):
                	https://en.wikipedia.org/wiki/E.164\';
                	
                	CREATE OR REPLACE TABLE teacher_availability ( 
                		id                   INT UNSIGNED     NOT NULL AUTO_INCREMENT PRIMARY KEY,
                		teacher_id           INT UNSIGNED     NOT NULL,
                		available_from_day   TINYINT UNSIGNED NOT NULL,
                		available_from_time  TIME             NOT NULL,
                		available_until_day  TINYINT UNSIGNED NOT NULL,
                		available_until_time TIME             NOT NULL,
                		CONSTRAINT fk_teacher_availability FOREIGN KEY ( teacher_id ) REFERENCES teacher( id ) ON DELETE CASCADE ON UPDATE NO ACTION
                	 ) ENGINE=InnoDB;
                	
                	CREATE OR REPLACE INDEX fk_teacher_availability ON teacher_availability ( teacher_id );
                	
                	ALTER TABLE teacher_availability MODIFY available_from_day TINYINT UNSIGNED NOT NULL COMMENT \'0 = monday, ... , 6 = sunday\';
                	
                	ALTER TABLE teacher_availability MODIFY available_until_day TINYINT UNSIGNED NOT NULL COMMENT \'0 = monday, ... , 6 = sunday\';
                	
                	CREATE OR REPLACE TABLE timetable ( 
                		id                   INT UNSIGNED  NOT NULL AUTO_INCREMENT PRIMARY KEY,
                		duration             TIME          NOT NULL,
                		group_id             INT UNSIGNED,
                		lesson_id            INT UNSIGNED,
                		teacher_id           INT UNSIGNED,
                		room_id              INT UNSIGNED,
                		CONSTRAINT fk_timetable_group_ FOREIGN KEY ( group_id ) REFERENCES group_( id ) ON DELETE SET NULL ON UPDATE NO ACTION,
                		CONSTRAINT fk_timetable_class FOREIGN KEY ( room_id ) REFERENCES room( id ) ON DELETE SET NULL ON UPDATE NO ACTION,
                		CONSTRAINT fk_timetable_lesson FOREIGN KEY ( lesson_id ) REFERENCES lesson( id ) ON DELETE SET NULL ON UPDATE NO ACTION,
                		CONSTRAINT fk_timetable_teacher FOREIGN KEY ( teacher_id ) REFERENCES teacher( id ) ON DELETE SET NULL ON UPDATE NO ACTION
                	 ) ENGINE=InnoDB;
                	
                	CREATE OR REPLACE INDEX fk_timetable_group ON timetable ( group_id );
                	
                	CREATE OR REPLACE INDEX fk_timetable_class ON timetable ( room_id );
                	
                	CREATE OR REPLACE INDEX fk_timetable_lesson ON timetable ( lesson_id );
                	
                	CREATE OR REPlACE INDEX fk_timetable_teacher ON timetable ( teacher_id );
                	
                	CREATE OR REPLACE TABLE homework (
                		id            INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                		published     DATETIME     NOT NULL DEFAULT NOW(),
                		due           DATETIME,
                		lesson_id     INT UNSIGNED,
                		teacher_id    INT UNSIGNED,
                		CONSTRAINT fk_homework_lesson FOREIGN KEY ( lesson_id ) REFERENCES lesson( id ) ON DELETE SET NULL ON UPDATE NO ACTION,
                		CONSTRAINT fk_homework_teacher FOREIGN KEY ( teacher_id ) REFERENCES teacher( id ) ON DELETE SET NULL ON UPDATE NO ACTION
                	);
                	
                	CREATE OR REPLACE TABLE attachments (
                		id        INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                		file_name VARCHAR(255) NOT NULL
                	);
                	
                	CREATE OR REPLACE TABLE homework_attachments (
                		id             INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                		homework_id    INT UNSIGNED NOT NULL,
                		attachments_id INT UNSIGNED NOT NULL,
                		
                		CONSTRAINT fk_join_homework FOREIGN KEY ( homework_id ) REFERENCES homework( id ) ON DELETE CASCADE ON UPDATE NO ACTION,
                		CONSTRAINT fk_join_attachment FOREIGN KEY ( attachments_id ) REFERENCES attachments( id ) ON DELETE CASCADE ON UPDATE NO ACTION
                	);
                ',
            );
            while ($this->connection->more_results()) {
                $this->connection->next_result();
                if (!$this->connection->store_result() and $this->connection->errno != 0) {
                    echo $this->connection->error;
                    return false;
                };
            }
            return true;
        } catch (Exception $e) {
            echo $this->connection->error;
            return false;
        }
    }

    function deleteIntezmeny(int $intezmeny_id): bool
    {
        try {
            $ret = $this->connection->query("USE ordayna_main_db;");
            if ($ret === false) return false;
            $ret = $this->connection->execute_query(
                '
                    DELETE FROM intezmeny WHERE id = ?;
                ',
                array($intezmeny_id)
            );
            if ($ret == false) return false;
            return $this->connection->query("DROP DATABASE ordayna_intezmeny_".$intezmeny_id);
        } catch (Exception $e) {
            return false;
        }
    }
}
