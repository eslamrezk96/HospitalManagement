from odoo import api, fields, models


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(string="Name", required=True)
    gender = fields.Selection(string="Gender",
                              selection=[('male', 'Male'), ('female', 'Female'), ])
    res_users_id = fields.Many2one(comodel_name="res.users", string="Related User")


