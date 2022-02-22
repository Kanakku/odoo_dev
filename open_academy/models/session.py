from odoo import models, fields, api

class open_academy(models.Model):
    _name = 'open_academy.session'
    _description = 'session'

    name = fields.Char(string='Name')
    start_date = fields.Date(String='Start Date')
    duration = fields.Char(string='Duration')
    seats = fields.Integer(string='Number of seats')