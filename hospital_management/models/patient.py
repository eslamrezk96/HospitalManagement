# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_name'
    _description = 'Patient Record'

    name = fields.Char(string="Test")
    patient_name = fields.Char(string='Name', required=True)
    gender = fields.Selection(string="Gender",
                              selection=[('male', 'Male'), ('female', 'Female'), ])
    age_group = fields.Selection(string="Age Group",
                                 selection=[('major', 'Major'), ('minor', 'Minor'), ],
                                 compute='set_age_group')
    patient_age = fields.Integer(string="Age", track_visibility='always')
    notes = fields.Text(string="Notes")
    image = fields.Binary(string="Image", attachment=True)
    name_seq = fields.Char(string='Patient Sequence', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: _('New'))
    appointment_ct = fields.Integer(string='Appointment Count', compute='appointment_count')
    active = fields.Boolean(string="Active", default=True)
    hospital_doctor_id = fields.Many2one(comodel_name="hospital.doctor", string="Doctor")
    doctor_gender = fields.Selection(string="Doctor Gender", selection=[('major', 'Major'), ('minor', 'Minor'), ], )
   
    @api.onchange('hospital_doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.hospital_doctor_id:
                rec.doctor_gender = rec.hospital_doctor_id.gender

    @api.constrains('patient_age')
    def chech_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_('The age must be greater than 5. '))

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result

    @api.onchange('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age < 15:
                rec.age_group = 'minor'
            else:
                rec.age_group = 'major'

    ## smart button (type object)
    ## Start
    @api.multi
    def open_patient_appointment(self):
        return {
            'name': _('Appointment'),
            'view_type': 'form',
            'domain': [('patient_id', '=', self.id)],
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_ct = count

    ## End

    @api.model
    def test_cron_job(self):
        print('Eslam')