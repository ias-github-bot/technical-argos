from odoo import fields, models


class HostelAmenities(models.Model):
    _name = "hostel.amenities"
    _description = "Hostel Amenities"

    name = fields.Char("Name", help="Provided Hostel Amenity")
    active = fields.Boolean("Active",
        help="Activate/Deactivate whether the amenity should be given or not")
    hostel_room_ids = fields.Many2many("hostel.room",
        "hostel_room_amenities_rel", "amenitiy_id", "room_id",
        string="Amenities",
        help="Select hostel room amenities")
