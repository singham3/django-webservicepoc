

def all_email_hook_data(email_hoo_obj):
    all_email_hook_list = []
    for i in email_hoo_obj:
        all_email_hook_list.append({
            'title': i.title,
            'hook': i.hook,
            'description': i.description,
            'status': i.status,
            'created_at': i.createdat.strftime('%m/%d/%Y %H:%M:%S.%I'),
            'updated_at': i.updatedat.strftime('%m/%d/%Y %H:%M:%S.%I'),
            'username': i.userid.username
        })
    return all_email_hook_list
