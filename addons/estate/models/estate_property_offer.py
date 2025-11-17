from odoo import api, fields, models
from datetime import datetime, date

class EstatePropertyOffer(models.Model):
  _name = "estate.property.offer"

  price = fields.Float(default=0, string="Price")
  status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False)
  partner_id = fields.Many2one("res.partner", string="Partner", required=True)
  property_id = fields.Many2one("estate.property", string="Offers", required=True)
  validity = fields.Integer(default=7 )
  
  # create_date = fields.Date("estate.property", "")
  # date_deadline = fields.Date(string="Deadline", compute="_compute_validity_date", inverse="_inverse_validity_date")

