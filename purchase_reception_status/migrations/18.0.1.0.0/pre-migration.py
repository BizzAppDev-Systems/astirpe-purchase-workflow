import logging

from openupgradelib import openupgrade

from odoo.tools.sql import column_exists

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    _logger.info(
        "Starting migration: checking for 'reception_status' column in 'purchase_order'"
    )
    if column_exists(env.cr, "purchase_order", "reception_status"):
        _logger.info("'reception_status' column found. Applying data migration")
        mapping_status = {"no": "pending", "partial": "partial", "received": "full"}
        for old_val, new_val in mapping_status.items():
            openupgrade.logged_query(
                env.cr,
                """
                UPDATE purchase_order
                SET receipt_status = %s
                WHERE reception_status = %s
                """,
                (new_val, old_val),
            )
        _logger.info("Migration completed: 'reception_status' values updated.")
    else:
        _logger.info("No 'reception_status' column found. Skipping migration.")
