# Copyright (C) 2018 - TODAY, Open Source Integrators
# Copyright (C) 2021 Serpent Consulting Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"
    warranty_exp_date = fields.Date(string="Warranty Expiration Date", compute='_compute_warranty_exp_date')

    def _compute_warranty_exp_date(self):
        for record in self:
            if (
                record.product_id
                and record.product_id.product_tmpl_id.warranty_type
                and record.product_id.product_tmpl_id.warranty
            ):
                warranty_type = record.product_id.product_tmpl_id.warranty_type
                time = False
                if warranty_type == "day":
                    time = (
                        datetime.now()
                        + timedelta(days=record.product_id.product_tmpl_id.warranty)
                    ).strftime(DEFAULT_SERVER_DATE_FORMAT)
                elif warranty_type == "week":
                    time = (
                        datetime.now()
                        + timedelta(weeks=record.product_id.product_tmpl_id.warranty)
                    ).strftime(DEFAULT_SERVER_DATE_FORMAT)
                elif warranty_type == "month":
                    time = (
                        datetime.now()
                        + relativedelta(months=+record.product_id.product_tmpl_id.warranty)
                    ).strftime(DEFAULT_SERVER_DATE_FORMAT)
                elif warranty_type == "year":
                    time = (
                        datetime.now()
                        + relativedelta(years=+record.product_id.product_tmpl_id.warranty)
                    ).strftime(DEFAULT_SERVER_DATE_FORMAT)
                record.warranty_exp_date = time
