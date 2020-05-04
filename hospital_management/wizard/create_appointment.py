from odoo import api, fields, models


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient")
    appointment_date = fields.Date(string="Appointment Date")

    def create_appointment(self):
        vals = {
            'patient_id':self.patient_id.id,
            'appointment_date':self.appointment_date,
            'notes':'Created From Wizard',
        }
        self.env['hospital.appointment'].create(vals)