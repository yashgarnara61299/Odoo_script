# -*- coding: utf-8 -*-
""" Migration Task """ 
import connection

old_script = connection.getSourceConnection()
new_script = connection.getDestinationConnection()

def userOldId():
    oldIdName = 'x_old_id'
    object_id = new_script.execute('ir.model', 'search', [('model','=','product.template')])
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
        print('Created - Old Id:', field_id)
    else:
        print ('Field: %s, already exist.' % oldIdName)

def Migration():

    old_ids = old_script.execute('product.template', 'search', [])
    for i, old_id in enumerate(sorted(old_ids)):
        print ('\n\nStart:[%s]: %s' % (i, old_id))

        import_setdata_id = new_script.execute('product.template', 'search',
                                            [('x_old_id','=',old_id)])
        if len(import_setdata_id) > 0:
            print('Exist:', import_setdata_id)
            continue

        old_v15 = old_script.execute('product.template', 'read',old_id)[0]
        print("old_v15", old_v15)

        old_taxes_id = old_v15['taxes_id'] and old_v15['taxes_id'][1] or ''
        new_taxes_id = new_script.execute('account.tax','search',[('name','=',old_taxes_id)])

        # old_categ_id = old_v15['categ_id'] and old_v15['categ_id'][1] or ''
        # new_categ_id = new_script.execute('product.category','search',[('name','=',old_categ_id)])

        # old_attributes_id = old_v15['attribute_id'] and old_v15['attribute_id'][1] or ''
        # new_attributes_id = new_script.execute('product.attribute','search',[('name','=',old_attributes_id)])

        attributes_variant= []
        print("attributes_variant",attributes_variant)
        if old_v15['attribute_line_ids']:
            for department in old_v15['attribute_line_ids']:
                attributes_variants=old_script.execute('product.template','read',department)[0]
                if attributes_variants['attribute_id'][0]:
                    data ={
                            'value_ids':attributes_variants['value_ids'][0],
                    }
                    attributes_variant.append((0,0,data))


        department = new_script.execute(
            'product.template', 'create',
            {   
                'name':old_v15['name'],
                'priority':old_v15['priority'],
                'image_1920':old_v15['image_1920'],
                'sale_ok':old_v15['sale_ok'],
                'purchase_ok':old_v15['purchase_ok'],
                'detailed_type': old_v15['detailed_type'],
                'invoice_policy':old_v15['invoice_policy'],
                'list_price':old_v15['list_price'],
                'taxes_id': new_taxes_id and new_taxes_id[0] or False, 
                'standard_price':old_v15['standard_price'],
                # 'categ_id': new_categ_id and new_categ_id[0] or False,
                'default_code':old_v15['default_code'],
                'barcode':old_v15['barcode'],
                # 'attribute_id':new_attributes_id and new_attributes_id[0] or False,
                'attribute_line_ids':attributes_variant,
                'x_old_id':old_id,
            }
        )
        print("Creation of record Successfullyyyyyyyyyy...\n End:[%s]: Created. Old(%s) New(%s)."
              % (i, old_id, department))
userOldId()
Migration()
print("Products script Successfullyyyyyyyyyy....",Migration())