from odoo import models, fields


class VcaCustomer(models.Model):
    _name = "vca.customer"
    _description = "Vehicle certificate customer"

    name = fields.Char()
    certificate_ids = fields.One2many("vca.certificate", "customer_id")
    partner_id = fields.One2many("res.partner", "related_customer_id")
