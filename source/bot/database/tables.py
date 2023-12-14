table_auth = ("""CREATE TABLE IF NOT EXISTS auth (
                 user_id BIGINT NOT NULL,
                 code_hash CHAR(64) NOT NULL,
                 email TEXT NOT NULL,
                 expiration BIGINT NOT NULL,
                 attempts INTEGER NOT NULL,
                 PRIMARY KEY (user_id, code_hash)
              );
              """)

table_logged = ("""CREATE TABLE IF NOT EXISTS logged (
                   user_id BIGINT PRIMARY KEY NOT NULL,
                   email TEXT NOT NULL,
                   role TEXT NOT NULL,
                   logged_in BOOL NOT NULL,
                   expiration BIGINT NOT NULL
                );
                """)

table_tempblocked = ("""CREATE TABLE IF NOT EXISTS tempblocked (
                        user_id BIGINT PRIMARY KEY NOT NULL,
                        expiration BIGINT NOT NULL
                     );
                     """)

table_occupied_rooms = ("""CREATE TABLE IF NOT EXISTS occupied_rooms (
                        user_id BIGINT NOT NULL,
                        building INTEGER NOT NULL,
                        storey INTEGER NOT NULL,
                        room INTEGER NOT NULL,
                        check_in_date BIGINT NOT NULL,
                        PRIMARY KEY (user_id, building, storey, room)
                     );
                     """)

table_student_card = ("""CREATE TABLE IF NOT EXISTS student_card (
                          id SERIAL NOT NULL,
                          user_id BIGINT NOT NULL,
                          first_name TEXT NOT NULL,
                          middle_name TEXT NOT NULL,
                          last_name TEXT NOT NULL,
                          birth_date TEXT NOT NULL,
                          dormitory_prov_order INTEGER NOT NULL,
                          enrollment_order INTEGER NOT NULL,
                          birth_place TEXT NOT NULL,
                          residential_address TEXT NOT NULL,
                          PRIMARY KEY (id, user_id)
                       );
                       """)

