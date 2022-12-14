from odoo import models, fields


class ItiTrack(models.Model):
    _name = 'iti.track'
    # _rec_name = 'capacity'

    name = fields.Char()
    duration = fields.Integer()
    start_date = fields.Date()
    end_date = fields.Date()
    address = fields.Char()
    capacity = fields.Integer(string='Number of Students')
    is_open = fields.Boolean()


    student_ids = fields.One2many('iti.student', 'track_id')
    course_ids = fields.One2many('track.course.line', 'track_id')


