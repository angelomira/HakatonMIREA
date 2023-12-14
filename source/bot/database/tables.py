table_auth = ("""CREATE TABLE IF NOT EXISTS auth (
                 user_id BIGINT NOT NULL,
                 code_hash CHAR(64) NOT NULL,
                 email TEXT NOT NULL,
                 expiration BIGINT NOT NULL,
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
