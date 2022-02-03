from odoo import models, fields, api
from datetime import date
import re
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = 'hms.patient'
    # _log_access = False
    _rec_name = 'first_name'


    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    email = fields.Char()
    history = fields.Char()
    cr_ratio = fields.Float()
    PCR = fields.Boolean()
    avatar = fields.Image()
    address = fields.Text()
    # age = fields.Integer()
    Blood_type = fields.Selection([
        ('o+', 'o+'),
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('AB+', 'AB+'),
        ('o-', 'o-'),
        ('A-', 'A-'),
        ('B-', 'B-'),
        ('AB-', 'AB-'),
    ])

    age = fields.Integer(compute='calc_age')

    @api.depends('birth_date')
    def calc_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = date.today().year - rec.birth_date.year
            else:
                rec.age = 0

    state = fields.Selection([
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('undetermined', 'Undetermined'),
        ('serious', 'Serious'),
    ],default='good')


    department_id = fields.Many2one('hms.department')  # many2one
    capacity = fields.Integer(related='department_id.capacity')
    doctor_ids = fields.Many2many('hms.doctor')
    patient_history_ids = fields.One2many('patient.history', 'patient_id')

    # @api.onchange('birth_date')
    # def _onchange_birth_date(self):
    #     if self.birth_date:
    #         self.age = date.today().year - self.birth_date.year



    def next_stage(self):
        if self.state == 'good':
            self.state = 'fair'
            self.create_log()

        elif self.state == 'fair':
            self.state = 'undetermined'
            self.create_log()

        else:
            self.state = 'serious'
            self.create_log()




    def create_log(self):
        # ORM -> object relational mapping
        patient = self.env['patient.history'].create({
            'description': self.state,
            'patient_id' : self.id,

        })



    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30:
            self.PCR = True
        else:
            self.PCR = False

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail')

    _sql_constraints = [
        # ('constraint name', 'constraint type', 'message ')
        ('email', 'UNIQUE(email)', 'email must be unique.'),
    ]

