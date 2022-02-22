from odoo import models, fields, api

class open_academy(models.Model):
    _name = 'open_academy.session'
    _description = 'session'

    name = fields.Char(string='Name')
    start_date = fields.Date(String='Start Date')
    duration = fields.Char(string='Duration')
    seats = fields.Integer(string='Number of seats')

    instructor_id = fields.Many2one('res.partner', string="Instructor", domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('open_academy.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")