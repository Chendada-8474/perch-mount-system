from alembic import op


TABLES_STATUS = (
    ("unreviewed_media_contents", "UNREVIEWED"),
    ("unchecked_media_contents", "UNCHECKED"),
    ("reviewed_media_contents", "REVIEWED"),
    ("accidental_media_contents", "ACCIDENTAL"),
)


ENUMS = (
    "positions",
    "mountlayers",
    "mediatypes",
    "mediastatus",
    "habitats",
    "conservationstatus",
    "preystatus",
)


def create_extensions():
    op.execute("CREATE EXTENSION IF NOT EXISTS citext;")
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_cron;")


def upgrade_ext():

    op.execute(
        """
        CREATE OR REPLACE PROCEDURE refresh_section_counts()
        LANGUAGE plpgsql
        AS $$
        BEGIN
            UPDATE sections s
            SET 
                undetected_count = COALESCE(m.undetected_count, 0),
                unchecked_count = COALESCE(m.unchecked_count, 0),
                unreviewed_count = COALESCE(m.unreviewed_count, 0),
                reviewed_count = COALESCE(m.reviewed_count, 0),
                accidental_count = COALESCE(m.accidental_count, 0)
            FROM (
                SELECT 
                    section_id,
                    COUNT(*) FILTER (WHERE status = 'UNDETECTED') AS undetected_count,
                    COUNT(*) FILTER (WHERE status = 'UNCHECKED') AS unchecked_count,
                    COUNT(*) FILTER (WHERE status = 'UNREVIEWED') AS unreviewed_count,
                    COUNT(*) FILTER (WHERE status = 'REVIEWED') AS reviewed_count,
                    COUNT(*) FILTER (WHERE status = 'ACCIDENTAL') AS accidental_count
                FROM media
                GROUP BY section_id
            ) AS m
            WHERE s.id = m.section_id;
        END;
        $$;
        """
    )

    op.execute(
        """
        SELECT cron.schedule(
            'refresh_section_counts_job',
            '* */1 * * *',
            $$CALL refresh_section_counts();$$
        );
        """
    )

    # update media status
    for table_name, status in TABLES_STATUS:
        op.execute(
            f"""
            CREATE OR REPLACE FUNCTION update_media_status_as_{status.lower()}()
            RETURNS TRIGGER AS $$
            BEGIN
                UPDATE media SET status = '{status.upper()}' WHERE media.id = NEW.medium_id;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER trigger_update_media_status_as_{status.lower()}
            AFTER INSERT ON {table_name}
            FOR EACH ROW
            EXECUTE FUNCTION update_media_status_as_{status.lower()}();
            """
        )

    # update prey_status of individual as has or no prey
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_prey_status_as_no_prey_or_unidentified()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.has_prey = false THEN
                UPDATE individuals
                SET prey_status = 'NO_PREY'
                WHERE id = NEW.individual_id;
            ELSIF NEW.has_prey = true THEN
                UPDATE individuals
                SET prey_status = 'UNIDENTIFIED'
                WHERE id = NEW.individual_id;
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trigger_update_prey_status_as_no_prey_or_unidentified
        AFTER INSERT ON marked_prey_individuals_contents
        FOR EACH ROW
        EXECUTE FUNCTION update_prey_status_as_no_prey_or_unidentified();
        """
    )

    # update prey_status of individual after prey identified
    op.execute(
        f"""
        CREATE OR REPLACE FUNCTION update_prey_status_as_identified()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE individuals SET prey_status = 'IDENTIFIED'
            WHERE individuals.id = NEW.individual_id;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trigger_update_prey_status_as_identified
        AFTER INSERT OR UPDATE ON identified_prey_individuals_contents
        FOR EACH ROW
        EXECUTE FUNCTION update_prey_status_as_identified();
        """
    )


def downgrade_ext():
    for table_name, status in TABLES_STATUS:
        op.execute(
            f"""
            DROP TRIGGER IF EXISTS trigger_update_prey_status_as_{status.lower()} ON {table_name};
            DROP FUNCTION IF EXISTS update_prey_status_as_{status.lower()} CASCADE;
            """
        )

    op.execute(
        """
        DROP TRIGGER IF EXISTS trigger_update_prey_status_as_no_prey_or_unidentified
        ON marked_prey_individuals_contents;
        DROP FUNCTION IF EXISTS update_prey_status_as_no_prey_or_unidentified CASCADE;
        """
    )

    op.execute(
        """
        DROP TRIGGER IF EXISTS trigger_update_prey_status_as_identified
        ON marked_prey_individuals_contents;
        DROP FUNCTION IF EXISTS update_prey_status_as_identified CASCADE;
        """
    )

    for name in ENUMS:
        op.execute(f"DROP TYPE IF EXISTS {name} CASCADE;")

    op.execute("DROP PROCEDURE IF EXISTS refresh_section_counts CASCADE;")
    op.execute("SELECT cron.unschedule('refresh_section_counts_job');")
