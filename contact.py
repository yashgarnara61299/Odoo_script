# -*- coding: utf-8 -*-
""" Migration Task """ 
import connection

old_script = connection.getSourceConnection()
new_script = connection.getDestinationConnection()

def userOldId():
    oldIdName = 'x_old_id'
    object_id = new_script.execute('ir.model', 'search', [('model','=','res.partner')])
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
    old_ids = old_script.execute('res.partner', 'search',['|',('active', '=', False), ('active', '=', True)])
    for i, old_id in enumerate(sorted(old_ids)):
        print ('\n\nStart:[%s]: %s' % (i, old_id))

        import_setdata_id = new_script.execute('res.partner', 'search',
                                            [('x_old_id','=',old_id)])

        if len(import_setdata_id) > 0:
            print('Exist:', import_setdata_id)
            continue

        old_v15 = old_script.execute('res.partner', 'read', old_id)[0]
        print("old_v15", old_v15)

        old_category_id = old_v15['category_id'] and old_v15['category_id'][1] or ''
        new_category_id = new_script.execute('res.partner.category','search',[('name','=',old_category_id)])

        old_title = old_v15['title'] and old_v15['title'][1] or ''
        new_title = new_script.execute('res.partner.title','search',[('name','=',old_title)])

        old_country_id = old_v15['country_id'] and old_v15['country_id'][1] or ''
        new_country_id = new_script.execute('res.country','search',[('name','=',old_country_id)])

        old_state = old_v15['state_id'] and old_v15['state_id'][1] or ''
        new_state = new_script.execute('res.country.state','search',[('name','=',old_state)])

        old_user_id = old_v15['user_id'] and old_v15['user_id'][1] or ''
        new_user_id = new_script.execute('res.users','search',[('name','=',old_user_id)])

        old_team_id = old_v15['team_id'] and old_v15['team_id'][1] or ''
        new_team_id = new_script.execute('crm.team','search',[('name','=',old_team_id)])

        old_property_payment_term_id = old_v15['property_payment_term_id'] and old_v15['property_payment_term_id'][1] or ''
        new_property_payment_term_id = new_script.execute('account.payment.term','search',
                                            [('name','=',old_property_payment_term_id)])

        old_property_product_pricelist = old_v15['property_product_pricelist'] and old_v15['property_product_pricelist'][1] or ''
        new_property_product_pricelist = new_script.execute('product.pricelist','search',
                                            [('name','=',old_property_product_pricelist)])

        old_property_supplier_payment_term_id = old_v15['property_supplier_payment_term_id'] and old_v15['property_supplier_payment_term_id'][1] or ''
        new_property_supplier_payment_term_id = new_script.execute('account.payment.term','search',
                                            [('name','=',old_property_supplier_payment_term_id)])

        old_property_payment_method_id = old_v15['property_payment_method_id'] and old_v15['property_payment_method_id'][1] or ''
        new_property_payment_method_id = new_script.execute('account.payment.method','search',[('name','=',old_property_payment_method_id)])

        old_property_account_position_id = old_v15['property_account_position_id'] and old_v15['property_account_position_id'][1] or ''
        new_property_account_position_id = new_script.execute('account.fiscal.position','search',
                                            [('name','=',old_property_account_position_id)])

        old_industry_id = old_v15['industry_id'] and old_v15['industry_id'][1] or ''
        new_industry_id = new_script.execute('res.partner.industry','search',[('name','=',old_industry_id)])

        res_partner_line = []
        print("res_partner_line",res_partner_line)
        if old_v15['child_ids']:
            for department in old_v15['child_ids']:
                res_partner_line_read = old_script.execute('res.partner','read',department)[0]
                # if res_partner_line_read['name']:
                data={
                        'type' : res_partner_line_read['type'],
                        'name' : res_partner_line_read['name'],
                        'title' : new_title['title'] and new_title['title'][0] or False,
                        'function' : res_partner_line_read['function'],
                        'comment' : res_partner_line_read['comment'],
                        'email' : res_partner_line_read['email'],
                        'phone' : res_partner_line_read['phone'],
                        'mobile' : res_partner_line_read['mobile'],
                    }
                res_partner_line.append((0,0,data))

        invoice = []
        print("invoice",invoice)
        if old_v15['bank_ids']:
            for department in old_v15['bank_ids']:
                invoce_read = old_script.execute('res.partner','read',department)[0]
                # if invoce_read['bank_id'][0]:
                data={
                        'bank_ids':invoce_read['bank_ids'] and invoce_read['bank_ids'][0] or False,
                        'acc_number':invoce_read['acc_number'],
                    }
                invoice.append((0,0,data))

        department = new_script.execute(
            'res.partner', 'create',
            {   
                'sale_order_count':old_v15['sale_order_count'],
                'company_type':old_v15['company_type'],
                'name':old_v15['name'],
                'image_1920':old_v15['image_1920'],
                'vat':old_v15['vat'],
                'phone':old_v15['phone'],
                'mobile':old_v15['mobile'],
                'email':old_v15['email'],
                'website':old_v15['website'],
                'category_id':new_category_id and new_category_id[0] or False,
                'street':old_v15['street'],
                'street2':old_v15['street2'],
                'title': new_title and new_title[0] or False,
                'city':old_v15['city'],
                'state_id':new_state and new_state[0] or False,
                'zip':old_v15['zip'],
                'country_id':new_country_id and new_country_id[0] or False,
                'user_id': new_user_id and new_user_id[0] or False,
                'team_id': new_team_id and new_team_id[0] or False,
                'property_payment_term_id': new_property_payment_term_id and new_property_payment_term_id[0] or False,
                'property_product_pricelist': new_property_product_pricelist and new_property_product_pricelist[0] or False,
                'property_supplier_payment_term_id':new_property_supplier_payment_term_id and new_property_supplier_payment_term_id[0] or False,
                'property_payment_method_id':new_property_payment_method_id and new_property_payment_method_id[0] or False,        
                'property_account_position_id': new_property_account_position_id and new_property_account_position_id[0] or False,
                'ref':old_v15['ref'],
                'industry_id': new_industry_id and new_industry_id[0] or False,
                'res_partner_line_read':res_partner_line,
                'bank_ids':invoice,
                'x_old_id':old_id,
            }

        )
        print("Creation of record Successfullyyyyyyyyyy...\n End:[%s]: Created. Old(%s) New(%s)"
          % (i, old_id, department))

userOldId()
Migration()
print("Yayyyyyyyyyyy..!!! Script run successfullyyyyy...!!!!",Migration())
