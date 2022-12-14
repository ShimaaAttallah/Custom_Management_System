from odoo import fields, models

class InheritHrEmployee(models.Model):
    _inherit = 'hr.employee'

    other_phone = fields.Char("Other Phone")