# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import date, datetime, time
from odoo.tools import date_utils

class EstateProperty(models.Model):
  _name = "estate.property"
  _description = "Estate Property"

  today = fields.Datetime.now()
  name = fields.Char("Title",required=True)
  description = fields.Text()
  postcode = fields.Char()
  date_availability = fields.Date(copy=False, default=date_utils.add(today, months=3))
  expected_price = fields.Float(required=True)
  selling_price = fields.Float(readonly=True,copy=False)
  bedrooms = fields.Integer(default=2)
  living_area = fields.Integer()
  facades = fields.Integer()
  garage = fields.Boolean()
  garden = fields.Boolean()
  garden_area = fields.Integer()
  garden_orientation = fields.Selection(
    string='Type',
    selection=[('north', 'North'), ('south','South'), ('east', 'East'), ('west','West')]
  )
  active = fields.Boolean('Active', default=False)
  status = fields.Selection(
    string='Status',
    selection=[
      ('new', 'New'), 
      ('offer received', 'Offer Received'), 
      ('offer accepted', 'Offered Accepted'),
      ('sold', 'Sold'),
      ('cancelled', 'Cancelled')
    ],
    default='new'
  )
  property_type_id = fields.Char("Property Type", required=True)
  salesperson = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
  buyer = fields.Many2one('res.partner', string="Buyer", index=True, tracking=10, copy=False, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
  tag_ids = fields.Many2many('estate.property.tag', string="Tags")
  offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
  total_area = fields.Float(compute="_compute_total")
  best_price = fields.Float("Best Offer", compute="_compute_max_offer")

  @api.depends('living_area', 'garden_area')
  def _compute_total(self):
    for record in self:
      record.total_area = record.living_area * record.garden_area

  @api.depends('offer_ids.price')
  def _compute_max_offer(self):
    for record in self:
      if record.offer_ids:
        record.best_price = max(record.offer_ids.mapped('price'))
      else:
        record.best_price = 0.0
