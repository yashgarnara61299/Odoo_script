import connection
old_script = connection.getSourceConnection()
new_script = connection.getDestinationConnection()

def userOldId():
    oldIdName = 'x_old_id'
    object_id = new_script.execute('ir.model', 'search', [('model','=','hr.expense')])
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

    old_ids = old_script.execute('hr.expense', 'search',[])
    for i, old_id in enumerate(sorted(old_ids)):
        print ('\n\nStart:[%s]: %s' % (i, old_id))

        import_setdata_id = new_script.execute('hr.expense', 'search',
                                            [('x_old_id','=',old_id)])

        if len(import_setdata_id) > 0:
            print('Exist:', import_setdata_id)
            continue

        old_v15 = old_script.execute('hr.expense', 'read', old_id,[])[0]
        print("old_v15", old_v15)

        old_product_id = old_v15['product_id'] and old_v15['product_id'][1] or ''
        new_product_id = new_script.execute('product.product','search',[('name','=',old_product_id)])

        old_employee_id = old_v15['employee_id'] and old_v15['employee_id'][1] or ''
        new_employee_id = new_script.execute('hr.employee','search',[('name','=',old_employee_id)])

        old_currency_id = old_v15['currency_id'] and old_v15['currency_id'][1] or ''
        new_currency_id = new_script.execute('res.currency','search',[('name','=',old_currency_id)])

        old_product_uom_id = old_v15['product_uom_id'] and old_v15['product_uom_id'][1] or ''
        new_product_uom_id = new_script.execute('uom.uom','search',[('name','=',old_product_uom_id)])

        department = new_script.execute(
            'hr.expense', 'create',
            {   
                'name':old_v15['name'],
                'product_id':new_product_id and new_product_id[0]or False,
                'total_amount':old_v15['total_amount'],
                'currency_id': new_currency_id and new_currency_id[0]or False,
                'unit_amount':old_v15['unit_amount'],
                'quantity':old_v15['quantity'],
                'product_uom_id': new_product_uom_id and new_product_uom_id[0]or False,
                'amount_residual':old_v15['amount_residual'],
                'payment_mode':old_v15['payment_mode'],
                'date':old_v15['date'],
                'employee_id': new_employee_id and new_employee_id[0]or False,
                'label_total_amount_company':old_v15['label_total_amount_company'],
                'description':old_v15['description'],
                'state':old_v15['state'],
                'x_old_id':old_id,
            }
        )
        # Button Code...
        # if old_v15.get('state') == 'submit':
        #     new_script.execute('hr.expense.sheet','write',department,{'state':'submit'})

        # elif old_v15.get('state') == 'approve':
        #     new_script.execute('hr.expense.sheet','write',department,{'state':'approve'})

        # elif old_v15.get('state') == 'post':
        #     new_script.execute('hr.expense.sheet','write',department,{'state':'post'})

        # elif old_v15.get('state') == 'done':
        #     new_script.execute('hr.expense.sheet','write',department,{'state':'done'})

        # print("Creation of record Successfullyyyyyyyyyy...\n End:[%s]: Created. Old(%s) New(%s)."
        #       % (i, old_id, department))

userOldId()
Migration()
print("Yayyyyyyyyyyy..!!! Script run successfullyyyyy...!!!!",Migration())