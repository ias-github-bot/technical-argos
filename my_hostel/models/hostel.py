from odoo import api, fields, models


class Hostel(models.Model):
    _name = 'hostel.hostel'
    _description = "Information about hostel"
    _order = "id desc, name"
    _rec_name = 'hostel_code'

    name = fields.Char(string="hostel Name", required=True)
    hostel_code = fields.Char(string="Code", required=True)
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    phone = fields.Char('Phone',required=True)
    mobile = fields.Char('Mobile',required=True)
    email = fields.Char('Email')
    hostel_floors = fields.Integer(string="Total Floors")
    image = fields.Binary('Hostel Image')
    active = fields.Boolean("Active", default=True,
        help="Activate/Deactivate hostel record")
    type = fields.Selection([("male", "Boys"), ("female", "Girls"),
        ("common", "Common")], "Type", help="Type of Hostel",
        required=True, default="common")
    other_info = fields.Text("Other Information",
        help="Enter more information")
    description = fields.Html('Description')
    hostel_rating = fields.Float('Hostel Average Rating',
                                # digits=(14, 4) # Method 1: Optional precision (total, decimals),
                                 digits='Rating Value' # Method 2
                                 )
    category_id = fields.Many2one('hostel.category')
    rector = fields.Many2one("res.partner", "Rector",
        help="Select hostel rector")
    room_ids = fields.One2many('hostel.room', 'hostel_id', string='Rooms')
    room_count = fields.Integer('Number of rooms', compute='_compute_room_by_hostel')
    room_amount_total = fields.Integer('Total amount per room rented', compute='_compute_room_by_hostel')
    room_available = fields.Integer('Number of rooms available', compute='_compute_room_by_hostel')
    room_partial_av = fields.Integer('Number of rooms partially available', compute='_compute_room_by_hostel')

    @api.depends('hostel_code')
    def _compute_display_name(self):
        for record in self:
            name = record.name
            if record.hostel_code:
                name = f'{name} ({record.hostel_code})'
            record.display_name = name

    @api.depends('room_ids', 'room_ids.student_per_room',
                 'room_ids.rent_amount', 'room_ids.student_ids')
    def _compute_room_by_hostel(self):
        # self == [recordset('hostel.hostel', 1), recordset('hostel.hostel', 2)]
        # self.room_ids == [recordset('hostel.room', 1), recordset('hostel.room', 2)]
        # record.room_ids == [recordset('hostel.room', 1), recordset('hostel.room', 2)]
        for record in self:
            count_room = len(record.room_ids)
            room_available = len(record.room_ids.filtered(lambda r: not r.student_ids))
            room_part_available = len(record.room_ids.filtered(
                lambda r: r.student_ids and len(r.student_ids) < r.student_per_room))
            amount_total = sum(record.room_ids.filtered('student_ids').mapped('rent_amount'))
            """
            amunt_total = 0
            for room in record.room_ids:
                if room.student_ids:
                    amount_total += room.rent_amount
            """

            record.room_count = count_room
            record.room_amount_total = amount_total
            record.room_available = room_available
            record.room_partial_av = room_part_available
