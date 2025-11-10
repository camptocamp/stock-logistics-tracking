# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    is_internal = fields.Boolean(
        computed="_compute_is_internal", store=True, string="Internal use?"
    )

    @api.depends("package_type_id", "package_type_id.package_carrier_type")
    def _compute_is_internal(self):
        for record in self:
            record.is_internal = (
                not record.package_type_id.package_carrier_type
                or record.package_type_id.package_carrier_type == "none"
            )
