from odoo import models, fields, api


class VcaResPartnerInherit(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    related_certificate_ids = fields.Many2one("vca.certificate")
