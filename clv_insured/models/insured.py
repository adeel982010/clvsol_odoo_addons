# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from datetime import datetime
from dateutil.relativedelta import relativedelta

from lxml import etree

from odoo import api, fields, models
from odoo.fields import Date as fDate
from odoo.exceptions import UserError


ADDRESS_FORMAT_CLASSES = {
    '%(city)s %(state_code)s\n%(zip)s': 'o_city_state',
    '%(zip)s %(city)s': 'o_zip_city'
}


class FormatAddress(object):

    @api.model
    def fields_view_get_address(self, arch):
        address_format = self.env.user.company_id.country_id.address_format or ''
        for format_pattern, format_class in ADDRESS_FORMAT_CLASSES.iteritems():
            if format_pattern in address_format:
                doc = etree.fromstring(arch)
                for address_node in doc.xpath("//div[@class='o_address_format']"):
                    # add address format class to address block
                    address_node.attrib['class'] += ' ' + format_class
                    if format_class.startswith('o_zip'):
                        zip_fields = address_node.xpath("//field[@name='zip']")
                        city_fields = address_node.xpath("//field[@name='city']")
                        if zip_fields and city_fields:
                            # move zip field before city field
                            city_fields[0].addprevious(zip_fields[0])
                arch = etree.tostring(doc)
                break
        return arch


class Insured(models.Model, FormatAddress):
    _description = 'Insured'
    _name = 'clv.insured'
    _order = 'name'

    @api.multi
    @api.depends('name', 'code', 'age')
    def name_get(self):
        result = []
        for record in self:
            result.append(
                (record.id,
                 u'%s [%s] (%s)' % (record.name, record.code, record.age)
                 ))
        return result

    name = fields.Char(string='Name', required=True)
    alias = fields.Char(string='Alias', help='Common name that the Insured is referred')

    code = fields.Char(string='Insured Code', required=False)

    notes = fields.Text(string='Notes')

    date_inclusion = fields.Datetime(
        string="Inclusion Date", required=False, readonly=False,
        default=lambda *a: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    nationality = fields.Many2one(comodel_name='res.country', string='Nationality')
    birthday = fields.Date(string="Date of Birth")
    age = fields.Char(
        string='Age',
        compute='_compute_age',
        store=True
    )
    estimated_age = fields.Char(string='Estimated Age', required=False)
    date_reference = fields.Date(string="Reference Date")
    age_reference = fields.Char(
        string='Reference Age',
        compute='_compute_age_reference',
        store=True
    )

    identification_id = fields.Char(string='Insured ID')
    otherid = fields.Char(string='Other ID')
    gender = fields.Selection(
        [('M', 'Male'),
         ('F', 'Female'),
         ('O', 'Other'),
         ], 'Gender'
    )
    marital = fields.Selection(
        [('single', 'Single'),
         ('married', 'Married'),
         ('widower', 'Widower'),
         ('divorced', 'Divorced'),
         ], string='Marital Status'
    )

    active = fields.Boolean(string='Active', default=1)

    _sql_constraints = [
        ('code_uniq',
         'UNIQUE(code)',
         u'Error! The Insured Code must be unique!'
         )
    ]

    @api.multi
    @api.constrains('birthday')
    def _check_birthday(self):
        for insured in self:
            if insured.birthday > fields.Date.today():
                raise UserError(u'Date of Birth must be in the past!')

    @api.one
    @api.depends('birthday')
    def _compute_age(self):
        now = datetime.now()
        if self.birthday:
            dob = datetime.strptime(self.birthday, '%Y-%m-%d')
            delta = relativedelta(now, dob)
            # self.age = str(delta.years) + "y " + str(delta.months) + "m " + str(delta.days) + "d"
            self.age = str(delta.years)
        else:
            self.age = "No Date of Birth!"

    @api.one
    @api.depends('date_reference', 'birthday')
    def _compute_age_reference(self):
        if self.date_reference:
            if self.birthday:
                dob = datetime.strptime(self.birthday, '%Y-%m-%d')
                now = datetime.strptime(self.date_reference, '%Y-%m-%d')
                delta = relativedelta(now, dob)
                # self.age_reference = str(delta.years) + "y " + str(delta.months) + "m " + str(delta.days) + "d"
                self.age_reference = str(delta.years)
            else:
                self.age_reference = "No Date of Birth!"
        else:
            self.age_reference = "No Reference Date!"

    @api.multi
    @api.depends('birthday')
    def _compute_age_days(self):
        today = fDate.from_string(fDate.today())
        for insured in self.filtered('birthday'):
            delta = (today - fDate.from_string(insured.birthday))
            insured.age_days = delta.days

    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    zip = fields.Char(string='ZIP code', change_default=True)
    city = fields.Char(string='City')
    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string='State',
        ondelete='restrict',
        domain="[('country_id','=',country_id)]"
    )
    country_id = fields.Many2one(comodel_name='res.country', string='Country', ondelete='restrict')

    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    fax = fields.Char(string='Fax')
    email = fields.Char(string='Email')

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        if (not view_id) and (view_type == 'form') and self._context.get('force_email'):
            view_id = self.env.ref('base.view_partner_simple_form').id
        res = super(Insured, self).fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu
        )
        if view_type == 'form':
            res['arch'] = self.fields_view_get_address(res['arch'])
        return res

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            return {'domain': {'state_id': [('country_id', '=', self.country_id.id)]}}
        else:
            return {'domain': {'state_id': []}}


class Insured2(models.Model):
    _inherit = 'clv.insured'

    main_insured_id = fields.Many2one(
        comodel_name='clv.insured',
        string='Main Insured',
        ondelete='restrict'
    )
    dependent_insured_ids = fields.One2many(
        comodel_name='clv.insured',
        inverse_name='main_insured_id',
        string='Dependent Insureds'
    )
    count_dependent_insureds = fields.Integer(
        string='Number of Dependent Insureds',
        compute='_compute_count_dependent_insureds',
        store=True
    )

    @api.depends('dependent_insured_ids')
    def _compute_count_dependent_insureds(self):
        for r in self:
            r.count_dependent_insureds = len(r.dependent_insured_ids)
