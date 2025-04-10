revision = "0000000006"
down_revision = "0000000005"

def upgrade(migration):
    # Create the "todo" table
    migration.create_table(
        "todo",
        """
            "entity_id" varchar(32) NOT NULL,
            "version" varchar(32) NOT NULL,
            "previous_version" varchar(32) DEFAULT '00000000000000000000000000000000',
            "active" boolean DEFAULT true,
            "changed_by_id" varchar(32) DEFAULT NULL,
            "changed_on" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            "person_id" varchar(32) NOT NULL,
            "title" text NOT NULL,
            "is_completed" boolean DEFAULT false,
            "created_on" timestamp DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY ("entity_id")
        """
    )
    migration.add_index("todo", "todo_person_id_ind", "person_id")
    migration.add_index("todo", "todo_is_completed_ind", "is_completed")

    # Create the "todo_audit" table
    migration.create_table(
        "todo_audit",
        """
            "entity_id" varchar(32) NOT NULL,
            "version" varchar(32) NOT NULL,
            "previous_version" varchar(32) DEFAULT '00000000000000000000000000000000',
            "active" boolean DEFAULT true,
            "changed_by_id" varchar(32) DEFAULT NULL,
            "changed_on" timestamp NULL DEFAULT CURRENT_TIMESTAMP,
            "person_id" varchar(32) NOT NULL,
            "title" text NOT NULL,
            "is_completed" boolean DEFAULT false,
            "created_on" timestamp DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY ("entity_id", "version")
        """
    )

    migration.update_version_table(version=revision)

def downgrade(migration):
    migration.drop_table(table_name="todo")
    migration.drop_table(table_name="todo_audit")
    migration.update_version_table(version=down_revision)
