admins_table = """CREATE TABLE IF NOT EXISTS admin
            (
                user_id SERIAL PRIMARY KEY, 
                name VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL UNIQUE,
                phone VARCHAR(50) NOT NULL,
                password VARCHAR (300) NOT NULL,
                registered TIMESTAMP DEFAULT NOW(),
                isadmin BOOLEAN DEFAULT FALSE
        )"""

queries = [admins_table]