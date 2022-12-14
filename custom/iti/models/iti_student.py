from odoo.exceptions import ValidationError, UserError
from odoo import models, fields, api


class ItiStudent(models.Model):
    _name = 'iti.student'
    _rec_name = 'first_name'

    first_name = fields.Char(size=20, string='First Name', required=False)
    second_name = fields.Char(string='Second Name')
    birth_date = fields.Date(string='Birth_Date')
    age = fields.Integer(compute="_get_age", store=True)
    address = fields.Char()
    phone = fields.Char()
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ])

    history = fields.Text()
    cv = fields.Html()
    image = fields.Image()
    state = fields.Selection([
        ('first_interview', 'First Interview'),
        ('second_interview', 'Second Interview'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='first_interview')

    salary = fields.Float(default=100)
    tax = fields.Float()
    email = fields.Char(string="Email")
    accepted = fields.Boolean()

    track_id = fields.Many2one('iti.track')
    track_capacity = fields.Integer(string="Track_Capacity", related="track_id.capacity", store=False)
    track_name = fields.Char(related='track_id.name', readonly=False, store=True)
    skill_ids = fields.Many2many('student.skills')


    @api.onchange('track_id', 'accepted')
    def change_salary(self):
        domain = []
        if self.track_id and self.accepted:
            self.salary = 1000
            return {
                'domain': {'track_id': domain},
                'warning': {
                    'title': 'Student Accepted',
                    'message': 'Student is Accepted and change salary to 1000'
                }
            }
        else:
            print('On Change')

    def action_second_interview(self):
        if self.track_id:
            self.state = 'second_interview'
        else:
            raise ValidationError('Must be track on student')

    def action_accepted(self):
        self.state = 'accepted'

    def action_rejected(self):
        self.state = 'rejected'

    def action_first_interview(self):
        self.state = 'first_interview'

    @api.model
    def create(self, vals):
        student = super().create(vals)
        if student.first_name and student.second_name:
            email = f'{student.first_name}.{student.second_name[0]}@gmail.com'
            student.email = email
        return student

    def write(self, vals):
        res = super().write(vals)
        # logic
        if vals.get('first_name'):
            email = f'{vals.get("first_name")}'
        else:
            email = f'{self.first_name}'
        if vals.get('second_name'):
            email += f'.{vals.get("second_name")[0]}@mycompany.com'
        else:
            email += f'.{self.second_name[0]}@mycompany.com'
        if vals.get('first_name') or vals.get('second_name'):
            self.email = email

        return res

    def unlink(self):
        print("record ", self)
        for student in self:
            if student.track_id:
                raise UserError(f"Not Allow to delete student linked with track {student.track_id.name}")
        return super().unlink()

    _sql_constraints = [
        ('email_unique', 'UNIQUE(email)', 'This email exists')
    ]

    @api.depends('birth_date')
    def _get_age(self):
        print("records  ", self)
        for student in self:
            if student.birth_date:
                today = fields.Date.today()
                delta = (today - student.birth_date).days
                student.age = delta // 365
            else:
                student.age = 0


class StudentSkills(models.Model):
    _name = 'student.skills'

    name = fields.Char()
    level = fields.Selection([
        ('good', 'Good'),
        ('very_good', 'Very Good'),
    ])
