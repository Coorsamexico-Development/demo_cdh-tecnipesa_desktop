
from features.database.migrations.migration import Migration, QueryMigration

class CreateTables(Migration):
    def __init__(self,):
        super().__init__()
        self.querys =self.create_tables()
   

    def create_tables(self):
         return [ 
             QueryMigration(
                """CREATE TABLE `tarimas`(
                    `id` INTEGER PRIMARY KEY,
                    `lpn` varchar(255) UNIQUE NOT NULL,
                    `token_tag` varchar(255) DEFAULT(NULL),
                    `switch` TINYINT(1) DEFAULT(0),
                    `created_at` TIMESTAMP,
                    `updated_at` TIMESTAMP
                    )
                    """,
                check_table_exist=True,
                table='tarimas'
            ),
            
         
        ]
        
        
