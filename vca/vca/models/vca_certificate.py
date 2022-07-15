from datetime import datetime

from odoo import models, fields, api


class VcaCertificate(models.Model):
    _name = "vca.certificate"
    _description = "Vehicle Certificate"
    _rec_name = "partner_id"

    serial_number = fields.Char(default=lambda self: self.env['ir.sequence'].next_by_code('vca.certificate.code'),
                                readonly="True")
    vehicle_type = fields.Selection([
        ("car", "Car"),
        ("bus", "Bus"),
        ("minibus", "Minibus"),
        ("Microbus", "microbus")
    ])
    certificate_type_id = fields.Many2one("vca.certificate_type")
    traffic_department_id = fields.Many2one("vca.traffic_department")
    partner_id = fields.Many2one("res.partner", "related_certificate_ids")
    partner_name = fields.Char(related="partner_id.name")
    motor_number = fields.Char()
    chassis_number = fields.Char()
    _this_year = datetime.now().year
    car_model = fields.Selection(list((str(i), str(i)) for i in range(_this_year, _this_year - 21, -1)))
    brand_id = fields.Many2one("vca.vehicle_brand")
    price = fields.Integer()
    log_history_ids = fields.One2many("vca.log_history", "certificate_id")
    printable = fields.Boolean(default=True)

    # @api.onchange('vehicle_type')
    # def show_menu(self):
    #     self.env.ref('vca.vca_certificate_card').write({'binding_model_id': None})

    def print_report_user(self):
        self.sudo().printable = False
        return self.print_report()

    def print_report(self, supervisor=False):
        # self.env.ref('vca.vca_certificate_card').write({'binding_model_id': None})
        # print(self.env['ir.actions.report'].search([("id", "=", 211)]))
        # self.env['ir.actions.report'].search([("id", "=", 211)]).write({'binding_model_id': None})

        if self.id:
            self.env["vca.log_history"].create({
                'certificate_id': self.id})
        return self.env.ref('vca.vca_certificate_card').report_action(self)

    def enable_print(self):
        self.printable = True

    @api.model
    def disable_print(self):
        print("Disabling print...")
        self.printable_var = False
        self.env.ref('vca.vca_certificate_card').write({'binding_model_id': None})
        


class CertificateType(models.Model):
    _name = "vca.certificate_type"
    _description = "Vehicle certificate type"

    name = fields.Char()
    certificate_ids = fields.One2many("vca.certificate", "certificate_type_id")


class TrafficDepartment(models.Model):
    _name = "vca.traffic_department"
    _description = "Traffic department"

    name = fields.Char()
    certificate_ids = fields.One2many("vca.certificate", "traffic_department_id")


class VehicleBrand(models.Model):
    _name = "vca.vehicle_brand"
    _description = "Vehicle brand"

    name = fields.Char()
    certificate_ids = fields.One2many("vca.certificate", "brand_id")


class LogHistory(models.Model):
    _name = "vca.log_history"
    _description = "Certificate print log history"

    certificate_id = fields.Many2one("vca.certificate")
