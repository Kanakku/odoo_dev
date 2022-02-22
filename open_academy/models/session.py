from odoo import models, fields, api
from odoo.exceptions import ValidationError

class open_academy(models.Model):
    _name = 'open_academy.session'
    _description = 'session'

    name = fields.Char(string='Name')
    start_date = fields.Date(String='Start Date', default=fields.Date.today)
    duration = fields.Char(string='Duration')
    seats = fields.Integer(string='Number of seats')
    active = fields.Boolean(default=True)

    instructor_id = fields.Many2one('res.partner', string="Instructor", domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('open_academy.course', ondelete='cascade', string="Course", required=True)
    
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(string="% Of Taken seats", compute='_taken_seats')

    # Sacar un porcentaje de asientos ocupados, depende del id de participantes y numero de asientos
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats = 0.0
            else:
                record.taken_seats = 100.0 * len(record.attendee_ids) / record.seats
    
    # Evitar un numero negativo de asientos o mas participantes que asientos
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Valor de 'seats' incorrecto",
                    'message': "El valor no puede ser negativo",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Demasiados asistentes",
                    'message': "Incremente el numero de asientos o reduzca los asistentes",
                },
            }
    
    # Un instructor no puede estar a cargo de una seccion y ser un aistente en la misma
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_attendees(self):
        if self.instructor_id and self.instructor_id in self.attendee_ids:
            raise ValidationError("Un instructor de seccion no puede ser asistente")
