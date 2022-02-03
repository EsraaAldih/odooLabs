from odoo import models, fields

class History(models.Model):
        _name = 'patient.history'
        # _rec_name = 'create_uid'

        description = fields.Char()

        patient_id = fields.Many2one('hms.patient')



