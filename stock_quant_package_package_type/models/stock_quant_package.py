# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    def auto_assign_packaging(self):
        res = super().auto_assign_packaging()
        for package in self:
            if not package.package_type_id:
                # if no package type could be set by auto assign,
                # fallback on the default product's package type (if any)
                package._sync_package_type_from_single_product()
        return res

    @api.model_create_multi
    def create(self, vals):
        records = super().create(vals)
        records._sync_package_type_from_packaging()
        return records

    def write(self, vals):
        result = super().write(vals)
        if vals.get("product_packaging_id"):
            self._sync_package_type_from_packaging()
        return result

    def _sync_package_type_from_packaging(self):
        for package in self:
            if package.package_type_id:
                # Do not set package type for delivery packages
                # to not trigger constraint like height requirement
                # (we are delivering them, not storing them)
                continue
            package_type = package.product_packaging_id.package_type_id
            if not package_type:
                continue
            package.package_type_id = package_type

    def _sync_package_type_from_single_product(self):
        for package in self:
            if package.package_type_id:
                # Do not set package type for delivery packages
                # to not trigger constraint like height requirement
                # (we are delivering them, not storing them)
                continue
            package_type = package.single_product_id.package_type_id
            best_packaging = package.single_product_id._find_best_packaging(
                package.single_product_qty
            )
            if best_packaging.package_type_id:
                package_type = best_packaging.package_type_id
            package.package_type_id = package_type
