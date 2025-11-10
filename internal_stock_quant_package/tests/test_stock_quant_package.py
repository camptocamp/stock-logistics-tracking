# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from .common import TestStockPickingInternal


class TestStockQuantPackage(TestStockPickingInternal):
    def test_is_internal(self):
        self.assertTrue(self.internal_package.is_internal)
        self.assertFalse(self.external_package.is_internal)
        # test change by changing package type carrier type
        self.internal_package.package_type_id.write({"package_carrier_type": "dhl"})
        self.external_package.package_type_id.write({"package_carrier_type": "none"})
        self.internal_package._compute_is_internal()
        self.external_package._compute_is_internal()
        self.assertFalse(self.internal_package.is_internal)
        self.assertTrue(self.external_package.is_internal)
