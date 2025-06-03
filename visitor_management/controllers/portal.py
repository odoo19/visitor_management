from odoo import http
from odoo.http import request
import base64

class VisitorRegistrationController(http.Controller):
    
    @http.route(['/visitor/registration'], type='http', auth="public", website=True)
    def visitor_registration_form(self, **kw):
        contacts = request.env['res.partner'].sudo().search([('is_company', '=', False)])
        values = {
            'contacts': contacts,
        }
        return request.render("visitor_management.visitor_registration_form", values)
    
    @http.route(['/visitor/registration/submit'], type='http', auth="public", website=True, methods=['POST'])
    def visitor_registration_submit(self, **post):
        frontdesk_visitor = request.env['frontdesk.visitor'].sudo()
        
        # Get the default frontdesk station (you might want to customize this)
        default_station = request.env['frontdesk.frontdesk'].sudo().search([], limit=1)
        
        # Prepare values for the frontdesk.visitor model
        vals = {
            'name': post.get('name'),
            'message': post.get('purpose'),
            'host_id': int(post.get('contact_person_id')) if post.get('contact_person_id') else False,
            'station_id': default_station.id if default_station else False,
            'phone': post.get('phone', ''),
            'email': post.get('email', ''),
        }
        
        # Process image data if provided
        if post.get('image_data') and post.get('image_data').strip():
            try:
                # Remove the header part (data:image/png;base64,)
                if ',' in post.get('image_data', ''):
                    image_data = post.get('image_data').split(',')[1]
                    vals['image'] = image_data
            except Exception as e:
                # Log error but continue with registration
                _logger.error(f"Error processing image: {e}")
        
        # Create the frontdesk.visitor record
        frontdesk_visitor.create(vals)
            
        return request.render("visitor_management.visitor_registration_thanks")

    # def _prepare_home_portal_values(self, counters):
    #     values = super()._prepare_home_portal_values(counters)
        
    #     if 'visit_count' in counters:
    #         partner = request.env.user.partner_id
    #         visit_count = request.env['visitor.registration'].sudo().search_count([
    #             ('email', '=', partner.email)
    #         ])
    #         values['visit_count'] = visit_count
        
    #     return values

    # @http.route(['/my/visits', '/my/visits/page/<int:page>'], type='http', auth="user", website=True)
    # def portal_my_visits(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
    #     # Prepare values
    #     values = self._prepare_portal_layout_values()
    #     partner = request.env.user.partner_id
        
    #     # Get visits linked to this user
    #     VisitorRegistration = request.env['visitor.registration'].sudo()
        
    #     domain = [('email', '=', partner.email)]
        
    #     # Count for pager
    #     visit_count = VisitorRegistration.search_count(domain)
        
    #     # Pager
    #     pager = portal_pager(
    #         url="/my/visits",
    #         url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
    #         total=visit_count,
    #         page=page,
    #         step=self._items_per_page
    #     )
        
    #     # Content according to pager and archive selected
    #     visits = VisitorRegistration.search(domain, limit=self._items_per_page, offset=pager['offset'])
        
    #     values.update({
    #         'visits': visits,
    #         'page_name': 'visit',
    #         'pager': pager,
    #         'default_url': '/my/visits',
    #         'visit_count': visit_count,
    #     })
        
    #     return request.render("visitor_registration.portal_my_visits", values)