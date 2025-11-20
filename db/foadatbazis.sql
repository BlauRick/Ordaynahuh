CREATE OR REPLACE SCHEMA foadatbazis_terv;

CREATE OR REPLACE TABLE foadatbazis_terv.intezmeny_ids ( 
	id                   INT UNSIGNED   NOT NULL AUTO_INCREMENT  PRIMARY KEY,
	intezmeny_id         INT UNSIGNED   NOT NULL   
 ) engine=InnoDB;

CREATE OR REPLACE TABLE foadatbazis_terv.users ( 
	id                   INT UNSIGNED   NOT NULL AUTO_INCREMENT  PRIMARY KEY,
	display_name         VARCHAR(200)    NOT NULL   ,
	email                VARCHAR(254)   UNIQUE NOT NULL   ,
	password_hash        CHAR(128)    NOT NULL   ,
	salt                 CHAR(80) NOT NULL,
	CONSTRAINT email UNIQUE ( email ) 
 ) engine=InnoDB;

CREATE OR REPLACE TABLE foadatbazis_terv.intezmeny_ids_users ( 
	intezmeny_ids_id     INT UNSIGNED   NOT NULL   ,
	users_id             INT UNSIGNED   NOT NULL   ,
	CONSTRAINT fk_intezmeny_ids_users FOREIGN KEY ( intezmeny_ids_id ) REFERENCES foadatbazis_terv.intezmeny_ids( id ) ON DELETE CASCADE ON UPDATE NO ACTION,
	CONSTRAINT fk_intezmeny_ids_users_users FOREIGN KEY ( users_id ) REFERENCES foadatbazis_terv.users( id ) ON DELETE CASCADE ON UPDATE NO ACTION
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

