# -*- coding: utf-8 -*-
""" Migration Task """ 
import connection
    
old_script = connection.getSourceConnection()
new_script = connection.getDestinationConnection()

def userOldId():
    oldIdName = 'x_old_id'
    object_id = new_script.execute('ir.model', 'search', [('model','=','hr.contract')])
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

    old_ids = old_script.execute('hr.contract', 'search',['|',('active', '=', False), ('active', '=', True)])
    for i, old_id in enumerate(sorted(old_ids)):
        print ('\n\nStart:[%s]: %s' % (i, old_id))

        import_setdata_id = new_script.execute('hr.contract', 'search',
                                            [('x_old_id','=',old_id)])

        if len(import_setdata_id) > 0:
            print('Exist:', import_setdata_id)
            continue
        
        old_v15 = old_script.execute('hr.contract', 'read', old_id)[0]
        print("old_v15", old_v15)

        old_employee_id = old_v15['employee_id'] and old_v15['employee_id'][1] or ''
        new_employee_id = new_script.execute('hr.employee','search',[('name','=',old_employee_id)])
    
        old_resource_calendar_id = old_v15['resource_calendar_id'] and old_v15['resource_calendar_id'][1]or ''
        new_resource_calendar_id = new_script.execute('resource.calendar','search',[('name','=',old_resource_calendar_id)])

        old_structure_type_id = old_v15['structure_type_id'] and old_v15['structure_type_id'][1] or ''
        new_structure_type_id = new_script.execute('hr.payroll.structure.type','search',[('name','=',old_structure_type_id)])

        old_department_id = old_v15['department_id'] and old_v15['department_id'][1] or ''
        new_department_id = new_script.execute('hr.department','search',[('name','=',old_department_id)])

        old_job_id = old_v15['job_id'] and old_v15['job_id'][1] or ''
        new_job_id = new_script.execute('hr.job','search',[('name','=',old_job_id)])

        old_contract_type_id = old_v15['contract_type_id'] and old_v15['contract_type_id'][1] or ''
        new_contract_type_id = new_script.execute('hr.contract.type','search',[('name','=',old_contract_type_id)])

        old_hr_responsible_id = old_v15['hr_responsible_id'] and old_v15['hr_responsible_id'][1] or ''
        new_hr_responsible_id = new_script.execute('res.users','search',[('name','=',old_hr_responsible_id)])

        department = new_script.execute(
            'hr.contract', 'create',
            {   
                'name':old_v15['name'],
                'date_start':old_v15['date_start'],
                'date_end':old_v15['date_end'],
                'wage':old_v15['wage'],
                'state':old_v15['state'],
                'employee_id': new_employee_id and new_employee_id[0]or False,
                'structure_type_id': new_structure_type_id and new_structure_type_id[0]or False,
                'resource_calendar_id':new_department_id and new_resource_calendar_id[0]or False,
                'department_id': new_department_id and new_department_id[0]or False,
                'job_id': new_job_id and new_job_id[0]or False,
                'contract_type_id': new_contract_type_id and new_contract_type_id[0]or False,
                'hr_responsible_id': new_hr_responsible_id and new_hr_responsible_id[0]or False,
                'x_old_id':old_id,
            }
        )
        print("Creation of record Successfullyyyyyyyyyy...\n End:[%s]: Created. Old(%s) New(%s)."
              % (i, old_id, department))

userOldId()
Migration()
print("Yayyyyyyyyyyy..!!! Script run successfullyyyyy...!!!!")
