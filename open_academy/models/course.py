from pyparsing import one_of
from odoo import models, fields, api


class open_academy(models.Model):
    _name = 'open_academy.course'
    _description = 'course'

    name = fields.Char(string='Course')
    title = fields.Char(string='Title')
    description = fields.Text(string='Description')

    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many('open_academy.session', 'course_id', string="Sessions")

    #Verificar que el nombre del curso y su descripcion sean diferentes, agregar nombre como unico
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "El titulo del curso y la descripcion deben ser diferentes"),

        ('name_unique',
         'UNIQUE(name)',
         "El titulo del curso debe ser diferente"),
    ]

    #Opcion de duplicado
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(open_academy, self).copy(default)
