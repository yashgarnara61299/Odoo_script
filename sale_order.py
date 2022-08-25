import connection
# Is old Database, this db is call old record...
old_script = connection.getSourceConnection()
#script is new created db
new_script = connection.getDestinationConnection() 
"""
create a userOldId Method for a not a creted a duplicate record,
this method call a id and check,already exitis method is not create arecord again
use:- Go to Filter and apply a filter a option old_id= contains.
"""
def userOldId():
    oldIdName = 'x_old_id'
    object_id = new_script.execute('ir.model', 'search', [('model','=','sale.order')])
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

    old_ids = old_script.execute('sale.order', 'search', [])
    for i, old_id in enumerate(sorted(old_ids)):
        print ('\n\nStart:[%s]: %s' % (i, old_id))

        import_setdata_id = new_script.execute('sale.order', 'search',
                                            [('x_old_id','=',old_id)])

        if len(import_setdata_id) > 0:
            print('Exist:', import_setdata_id)
            continue

        old_v15 = old_script.execute('sale.order', 'read', old_id)[0]
        print("old_v15", old_v15)

        # Use For m2o
        # utm.campaign it define a relation field name
        old_v_campaign_id = old_v15['campaign_id'] and old_v15['campaign_id'][1] or ''
        new_v_campaign_id = new_script.execute('utm.campaign', 'search',
                                            [('name','=',old_v_campaign_id)])

        old_v_medium_id = old_v15['medium_id'] and old_v15['medium_id'][1] or ''
        new_v_medium_id = new_script.execute('utm.medium', 'search',
                                            [('name','=',old_v_medium_id)])

        old_v_source_id = old_v15['source_id'] and old_v15['source_id'][1] or ''
        new_v_source_id = new_script.execute('utm.source', 'search',
                                            [('name','=',old_v_source_id)])

        # use for inside a model of record sale_order and inside a sale_order_line
        sale_order_line = []
        print("sale_order_line",sale_order_line)
        if old_v15 ['order_line']:
            for department in old_v15['order_line']:
                sale_order_line_read = old_script.execute('sale.order.line', 'read', department)[0]    
                if sale_order_line_read['product_id'][0]:
                    data ={
                        'product_id':sale_order_line_read['product_id'][0],
                        'name':sale_order_line_read['name'],
                        'product_uom_qty':sale_order_line_read['product_uom_qty'],
                        'price_unit':sale_order_line_read['price_unit'],
                        'tax_id':sale_order_line_read['tax_id'],
                        'price_subtotal':sale_order_line_read['price_subtotal'],
                    }
                    sale_order_line.append((0,0,data))


        department = new_script.execute(
            'sale.order', 'create',
            {   
                'name':old_v15['name'],
                'partner_id': old_v15['partner_id'][0],
                'date_order': old_v15['date_order'],
                'order_line':sale_order_line,
                'user_id':old_v15['user_id'][0],
                'team_id':old_v15['team_id'][0],
                'require_signature':old_v15['require_signature'],
                'require_payment':old_v15['require_payment'],
                'client_order_ref':old_v15['client_order_ref'],
                'tag_ids':old_v15['tag_ids'],
                'commitment_date':old_v15['commitment_date'],
                'fiscal_position_id':old_v15['fiscal_position_id'],
                'origin':old_v15['origin'],
                'campaign_id':new_v_campaign_id and new_v_campaign_id[0] or False,
                'medium_id':new_v_medium_id and new_v_medium_id[0] or False,
                'source_id':new_v_source_id and new_v_source_id[0] or False,
                'x_old_id':old_id,
                'state':'draft',
            }
        )
        # Button Code 
        if old_v15.get('state') == 'sent':
            new_script.execute('sale.order','action_quotation_send',department)

        elif old_v15.get('state') == 'sale':
            new_script.execute('sale.order','action_confirm',department)

        elif old_v15.get('state') == 'done':
            new_script.execute('sale.order','action_done',department)

        elif old_v15.get('state') == 'cancel':
            new_script.execute('sale.order','action_cancel',department)

        print("Creation of record Successfullyyyyyyyyyy...\n End:[%s]: Created. Old(%s) New(%s)."
            % (i, old_id, department))

userOldId()
Migration()
print("Yayyyyyyyyyyy..!!! Script run successfullyyyyy...!!!!")