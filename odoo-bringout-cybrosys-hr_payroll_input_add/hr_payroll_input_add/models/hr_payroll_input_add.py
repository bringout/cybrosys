# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class HrPayrollInputAdd(models.Model):
    _name = 'hr.payroll.input.add'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Payroll Add Request"

    @api.model
    def default_get(self, field_list):
        result = super(HrPayrollInputAdd, self).default_get(field_list)
        if result.get('user_id'):
            ts_user_id = result['user_id']
        else:
            ts_user_id = self.env.context.get('user_id', self.env.user.id)
        result['employee_id'] = self.env['hr.employee'].search([('user_id', '=', ts_user_id)], limit=1).id

        return result

    @api.onchange('employee_id')
    def onchange_employee(self):
        if not self.employee_id:
            return

        employee = self.employee_id
        self.company_id = self.env['res.company'].search([('id', '=', employee.company_id.id)], limit=1)

    

    name = fields.Char(string="Payroll Add Name", readonly=True, help="Name of the payroll add")
    date = fields.Date(string="Date", default=fields.Date.today(), readonly=True, help="Date")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, help="Employee")
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True,
                                    string="Department", help="Employee")
    payment_date = fields.Date(string="Payment Start Date", required=True, default=fields.Date.today(), help="Date of "
                                                                                                             "the "
                                                                                                             "paymemt")
    # v19: Field.states removed; editability in draft is handled in the view
    # (readonly="state != 'draft'").
    company_id = fields.Many2one('res.company', 'Company', readonly=True, help="Company",
                                 default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, help="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)
    job_position = fields.Many2one('hr.job', related="employee_id.job_id", readonly=True, string="Job Position",
                                   help="Job position")
    add_amount = fields.Float(string="Add amount", required=True, help="Payroll add amount")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval_1', 'Submitted'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('cancel', 'Canceled'),
    ], string="State", default='draft', tracking=True, copy=False, )

    payslip_id = fields.Many2one('hr.payslip', string="Payslip Ref.", help="Payslip")

    # v19: ORM expects batch create (model_create_multi); single @api.model
    # create is rejected. ir.sequence.get() was removed long ago -> next_by_code.
    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            values['name'] = self.env['ir.sequence'].next_by_code('hr.payroll.input.add.seq') or ' '
        return super(HrPayrollInputAdd, self).create(vals_list)

 
    def action_move_to_status_draft(self):
        for input_add_id in self._context['active_ids']:
            input_add = self.env['hr.payroll.input.add'].browse(input_add_id)
            input_add.write({'state': 'draft'})

    def action_refuse(self):
        return self.write({'state': 'refuse'})

    def action_submit(self):
        self.write({'state': 'waiting_approval_1'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_approve(self):
        for data in self:
            #if not data.loan_lines:
            #    raise ValidationError(_("Please Compute installment"))
            #else:
            self.write({'state': 'approve'})

    def unlink(self):
        for add in self:
            if add.state not in ('draft', 'cancel'):
                raise UserError(
                    'You cannot delete a pyroll add which is not in draft or cancelled state')
        return super(HrPayrollInputAdd, self).unlink()



class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def _compute_employee_payroll_adds(self):
        """This compute total payroll adds count of an employee.
            """
        # Must loop: self.id raises "Expected singleton" on a multi-record read
        # (v19 reads a computed field for the whole recordset at once).
        Add = self.env['hr.payroll.input.add']
        for employee in self:
            employee.payroll_add_count = Add.search_count([('employee_id', '=', employee.id)])

    payroll_add_count = fields.Integer(string="Payroll adds", compute='_compute_employee_payroll_adds')
