from odoo import models, fields, api
import base64

class FrontdeskVisitor(models.Model):
    _inherit = 'frontdesk.visitor'
    
    image = fields.Binary(string='Photo', attachment=True)
    host_id = fields.Many2one('res.partner', string="Host")

class VisitorRegistration(models.Model):
    _name = 'visitor.registration'
    _description = 'Visitor Registration'
    _rec_name = 'name'
    _order = 'create_date desc'
    
    name = fields.Char(string='Visitor Name', required=True)
    purpose = fields.Text(string='Purpose of Visit', required=True)
    contact_person_id = fields.Many2one('res.partner', string='Person to Meet', required=True)
    image = fields.Binary(string='Photo', attachment=True)
    registration_date = fields.Datetime(string='Registration Date', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    station_id = fields.Many2one('frontdesk.frontdesk', string='Frontdesk Station', required=True)
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    frontdesk_visitor_id = fields.Many2one('frontdesk.visitor', string='Frontdesk Visitor Reference')
    
    @api.model
    def create_visitor_registration(self, vals):
        if vals.get('image_data'):
            # Remove the header part (data:image/png;base64,)
            if ',' in vals.get('image_data', ''):
                image_data = vals.get('image_data').split(',')[1]
                vals['image'] = image_data
            
            # Remove image_data as it's not a field in the model
            if 'image_data' in vals:
                del vals['image_data']
        
        visitor = self.create(vals)
        
        # Create a corresponding record in frontdesk.visitor
        frontdesk_visitor = self.env['frontdesk.visitor'].sudo().create({
            'name': visitor.name,
            'phone': visitor.phone,
            'email': visitor.email,
            'host_id': visitor.contact_person_id.id,
            'station_id': visitor.station_id.id,
            'message': visitor.purpose,
            'image': visitor.image,
        })
        
        # Link the frontdesk.visitor to the visitor.registration
        visitor.write({
            'frontdesk_visitor_id': frontdesk_visitor.id
        })
        
        return visitor.id