from odoo import models, fields

class Doctors(models.Model):
        _name = 'hms.doctor'
        _rec_name = 'first_name'

        first_name = fields.Char()
        last_name = fields.Char()
        Image = fields.Image()


