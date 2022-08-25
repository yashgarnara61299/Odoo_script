import connection    
old_script = connection.getSourceConnection()
new_script = connection.getDestinationConnection()

def userOldId():
    oldIdName = 'x_old_id'
    object_id = new_script.execute('ir.model', 'search', [('model','=','hr.expense.sheet')])
    field = new_script.execute(
        'ir.model.fields', 'search',
        [('model_id', '=', object_id and object_id[0]),
         ('name', '=', oldIdName)]
    )
    if not field:
        field_id = new_script.execute(
            'ir.model.fields', 'create',
            {'name': oldIdName,
             'ttype': 'char',
             'field_description': 'Old_id',
             'model_id': object_id and object_id[0],
             'state': 'manual',
             'modules': 'base'})
        print ('Created - Old Id:', field_id)
    else:
        print ('Field: %s, already exist.' % oldIdName)

def Migration():

    old_ids = old_script.execute('hr.expense.sheet', 'search',[])
    for i, old_id in enumerate(sorted(old_ids)):
        print ('\n\nStart:[%s]: %s' % (i, old_id))

        import_setdata_id = new_script.execute('hr.expense.sheet', 'search',
                                            [('x_old_id','=',old_id)])

        if len(import_setdata_id) > 0:
            print('Exist:', import_setdata_id)
            continue

        old_v15 = old_script.execute('hr.expense.sheet', 'read', old_id,)[0]
        print("old_v15", old_v15)

        old_user_id = old_v15['user_id'] and old_v15['user_id'][1] or ''
        new_user_id = new_script.execute('res.users','search',[('name','=',old_user_id)])

        old_journal_id = old_v15['journal_id'] and old_v15['journal_id'][0] or ''
        new_journal_id = new_script.execute('account.journal','search',[('name','=',old_journal_id)])

        hr_expense_Sheet_list = []
        print("hr_expense_Sheet_list",hr_expense_Sheet_list)
        if old_v15['expense_line_ids']:
            for department in old_v15['expense_line_ids']:
                hr_expense_sheet_read = old_script.execute('hr.expense','read',department)[0]

                old_employee_id = old_v15['employee_id'] and old_v15['employee_id'][1] or ''
                new_employee_id = new_script.execute('hr.employee','search',[('name','=',old_employee_id)])

                # old_product_id = old_v15['product_id'] and old_v15['product_id'][1] or ''
                # new_product_id = new_script.execute('product.product','search',[('name','=',old_product_id)])

                data = {
                    'name':hr_expense_sheet_read['name'],
                    'employee_id': new_employee_id and new_employee_id[0] or False,
                    # 'product_id': new_product_id and new_product_id[0] or False,
                    'payment_mode': hr_expense_sheet_read['payment_mode'],
                    # 'sale_order_id': new_sale_order_id and new_sale_order_id[0] or False,
                    'reference':hr_expense_sheet_read['reference'], 
                    'date': hr_expense_sheet_read['date'],
                    # 'account_id': new_account_id and new_account_id[0] or False,
                    'total_amount': hr_expense_sheet_read['total_amount'],
                    'unit_amount': hr_expense_sheet_read['unit_amount'],
                    'currency_id': hr_expense_sheet_read['currency_id'],
                    'quantity': hr_expense_sheet_read['quantity'],
                    'total_amount_company': hr_expense_sheet_read['total_amount_company'],
                    'amount_residual':hr_expense_sheet_read['amount_residual'],
                    'state': hr_expense_sheet_read['state'],
                }
                hr_expense_Sheet_list.append((0, 0, data))

        department = new_script.execute(
            'hr.expense.sheet', 'create',
            {   
                'name':old_v15['name'],
                'employee_id': new_employee_id and new_employee_id[0] or False,
                'approval_date': old_v15['approval_date'],
                'user_id': new_user_id and new_user_id[0]or False,
                'journal_id': new_journal_id and new_journal_id[0]or False,  
                # 'accounting_date': old_v15['accounting_date'],
                'payment_mode': old_v15['payment_mode'],
                'payment_state': old_v15['payment_state'],
                'total_amount': old_v15['total_amount'],
                'state':'draft',
                'expense_line_ids':hr_expense_Sheet_list,
                'x_old_id':old_id,
            }
        )
        # Button Code...
        if old_v15.get('state') == 'submit':
            new_script.execute('hr.expense.sheet','write',department,{'state':'submit'})

        elif old_v15.get('state') == 'approve':
            new_script.execute('hr.expense.sheet','write',department,{'state':'approve'})

        elif old_v15.get('state') == 'post':
            new_script.execute('hr.expense.sheet','write',department,{'state':'post'})

        elif old_v15.get('state') == 'done':
            new_script.execute('hr.expense.sheet','write',department,{'state':'done'})

        print("Creation of record Successfullyyyyyyyyyy...\n End:[%s]: Created. Old(%s) New(%s)."
              % (i, old_id, department))

userOldId()
Migration()
print("Yayyyyyyyyyyy..!!! Script run successfullyyyyy...!!!!")
