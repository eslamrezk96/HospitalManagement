# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Appointment'
    _order = 'appointment_date desc'

    name = fields.Char(string='0', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient", required=True, )
    appointment_lines_ids = fields.One2many(comodel_name="hospital.appointment.lines", inverse_name="appointment_id",
                                            string="Appointment Lines")
    patient_age = fields.Integer(string="Age", related='patient_id.patient_age')
    notes = fields.Text(string="Notes")
    doctor_note = fields.Text(string="Notes")
    pharmacy_note = fields.Text(string="Notes")
    appointment_date = fields.Date(string="Date", required=True, )
    state = fields.Selection(string="Status",
                             selection=[
                                 ('draft', 'Draft'), ('confirm', 'Confirm'),
                                 ('done', 'Done'), ('cancel', 'Cancelled'), ], readonly=True, default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    @api.multi
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    @api.multi
    def action_done(self):
        for rec in self:
            rec.state = 'done'


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Hospital Appointment Lines'

    product_id = fields.Many2one('res.partner', string="Medicine")
    quantity = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one(comodel_name="hospital.appointment", string="Appointment ID")
