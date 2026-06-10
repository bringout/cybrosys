# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Amaya Aravind (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    """ class for inherited model purchase order line. Contains a field for line
        numbers and a function for computing line numbers.
    """

    _inherit = 'purchase.order.line'

    sequence_number = fields.Integer(string='#', compute='_compute_sequence_number', help='Line Numbers')

    @api.depends('sequence', 'order_id', 'order_id.order_line')
    def _compute_sequence_number(self):
        """Function to compute line numbers"""
        # v19 requires every record in self to be assigned; a line with no
        # order_id would be left untouched -> "failed to assign". Default first.
        self.sequence_number = 0
        for order in self.mapped('order_id'):
            sequence_number = 1
            for lines in order.order_line:
                if lines.display_type:
                    lines.sequence_number = sequence_number
                    sequence_number += 0
                else:
                    lines.sequence_number = sequence_number
                    sequence_number += 1
