import connection
    
old_script = connection.getSourceConnection()
new_script = connection.getDestinationConnection()

def userOldId():
    oldIdName = 'x_old_id'
    object_id = new_script.execute('ir.model', 'search', [('model','=','hr.employee')])
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

    old_ids = old_script.execute('hr.employee', 'search', [])
    for i, old_id in enumerate(sorted(old_ids)):
        print ('\n\nStart:[%s]: %s' % (i, old_id))

        import_setdata_id = new_script.execute('hr.employee', 'search',
                                            [('x_old_id','=',old_id)])

        if len(import_setdata_id) > 0:
            print('Exist:', import_setdata_id)
            continue
        
        # in this script i have fetch one error, error is missing a one field. so i add a empty list, i have 
        #.....define a empty list [].

        old_v15 = old_script.execute('hr.employee', 'read', old_id, [])[0]
        print("old_v15", old_v15)

        # old_category_ids = old_v15['category_ids'] and old_v15['category_ids'][0] or ''
        # new_category_ids = new_script.execute('hr.employee.category','search',[('name','=',old_category_ids)])

        old_depatment_id = old_v15['department_id'] and old_v15['department_id'][1] or ''
        new_department_id = new_script.execute('hr.department','search',[('name','=',old_depatment_id)])

        old_parent_id = old_v15['parent_id'] and old_v15['parent_id'][1] or ''
        new_parent_id = new_script.execute('hr.employee','search',[('name','=',old_parent_id)])

        old_coach_id = old_v15['coach_id'] and old_v15['coach_id'][1] or ''
        new_coach_id = new_script.execute('hr.employee','search',[('name','=',old_coach_id)])

        old_address_id = old_v15['address_id'] and old_v15['address_id'][1] or ''
        new_address_id = new_script.execute('res.partner','search',[('name','=',old_address_id)])

        old_work_location_id = old_v15['work_location_id'] and old_v15['work_location_id'][1] or ''
        new_work_location_id = new_script.execute('hr.work.location','search',[('name','=',old_work_location_id)])

        old_resource_calendar_id = old_v15['resource_calendar_id'] and old_v15['resource_calendar_id'][1] or ''
        new_resource_calendar_id = new_script.execute('resource.calendar','search',[('name','=',old_resource_calendar_id)])

        old_address_home_id = old_v15['address_home_id'] and old_v15['address_home_id'][1] or ''
        new_address_home_id = new_script.execute('res.partner','search',[('name','=',old_address_home_id)])

        old_country_id = old_v15['country_id'] and old_v15['country_id'][1] or ''
        new_country_id = new_script.execute('res.country','search',[('name','=',old_country_id)])

        old_country_of_birth = old_v15['country_of_birth'] and old_v15['country_of_birth'][1] or ''
        new_country_of_birth = new_script.execute('res.country','search',[('name','=',old_country_of_birth)])

        old_user_id = old_v15['user_id'] and old_v15['user_id'][1] or ''
        new_user_id = new_script.execute('res.users','search',[('name','=',old_user_id)])

        old_contract_id = old_v15['contract_id'] and old_v15['contract_id'][1]or ''
        new_contract_id = new_script.execute('hr.contract','search',[('name','=',old_contract_id)])

        old_job_id = old_v15['job_id'] and old_v15['job_id'][1]or ''
        new_job_id = new_script.execute('hr.job','search',[('name','=',old_job_id)])

    
        department = new_script.execute(
            'hr.employee', 'create',
            {   
                'name':old_v15['name'],
                'job_title':old_v15['job_title'],
                'image_1920':old_v15['image_1920'],
                'category_ids': new_category_ids and new_category_ids[0]or False,
                'mobile_phone':old_v15['mobile_phone'],
                'work_phone':old_v15['work_phone'],
                'work_email':old_v15['work_email'],
                'department_id':new_department_id and new_department_id[0]or False,
                'parent_id':new_parent_id and new_parent_id[0]or False,
                'coach_id':new_coach_id and new_coach_id[0]or False,
                'address_id':new_address_id and new_address_id[0]or False,
                'work_location_id':new_work_location_id and new_work_location_id[0]or False,
                'resource_calendar_id':new_resource_calendar_id and new_resource_calendar_id[0]or False,
                'tz':old_v15['tz'],
                'address_home_id':new_address_home_id and new_address_home_id[0]or False,
                'private_email':old_v15['private_email'],
                'phone':old_v15['phone'],
                'lang':old_v15['lang'],
                'km_home_work':old_v15['km_home_work'],
                'marital':old_v15['marital'],
                'emergency_contact':old_v15['emergency_contact'],
                'emergency_phone':old_v15['emergency_phone'],
                'certificate':old_v15['certificate'],
                'study_field':old_v15['study_field'],
                'study_school':old_v15['study_school'],
                'country_id':new_country_id and new_country_id[0]or False,
                'identification_id':old_v15['identification_id'],
                'passport_id':old_v15['passport_id'],
                'gender':old_v15['gender'],
                'birthday':old_v15['birthday'],
                'place_of_birth':old_v15['place_of_birth'],
                'country_of_birth':new_country_of_birth and new_country_of_birth[0]or False,
                'children':old_v15['children'],
                'visa_no':old_v15['visa_no'],
                'permit_no':old_v15['permit_no'],
                'visa_expire':old_v15['visa_expire'],
                'work_permit_expiration_date':old_v15['work_permit_expiration_date'],
                'has_work_permit':old_v15['has_work_permit'],
                'employee_type':old_v15['employee_type'],
                'user_id':new_user_id and new_user_id[0]or False,
                'contract_id':new_contract_id and new_contract_id[0]or False,
                'job_id':new_job_id and new_job_id[0]or False,
                'pin':old_v15['pin'],
                'barcode':old_v15['barcode'],
                'pin':old_v15['pin'],
                'x_old_id':old_id,
            }
        )
        print("Creation of record Successfullyyyyyyyyyy...\n End:[%s]: Created. Old(%s) New(%s)."
              % (i, old_id, department))

userOldId()
Migration()
print("Yayyyyyyyyyyy..!!! Script run successfullyyyyy...!!!!")
