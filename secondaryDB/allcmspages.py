
def all_cms_pages_list(all_cms_obj):
    all_cms = []
    for i in all_cms_obj:
        all_cms.append({
            'id': i.id,
            'title': i.title,
            'meta_title': i.meta_title,
            'sub_title': i.sub_title,
            'meta_keyword': i.meta_keyword,
            'slug': i.slug,
            'meta_description': i.meta_description,
            'username': i.userid.username,
            'short_description': i.short_description,
            'cms_file': i.cmsfile.url,
            'html_description': i.html_description,
            'create_date': i.createdate.strftime('%m/%d/%Y %H:%M:%S.%I'),
            'update_date': i.updatedate.strftime('%m/%d/%Y %H:%M:%S.%I'),
            'status': i.status
        })
    return all_cms


def cms_pages_data(cms_obj):
    return {
            'id': cms_obj.id,
            'title': cms_obj.title,
            'meta_title': cms_obj.meta_title,
            'sub_title': cms_obj.sub_title,
            'meta_keyword': cms_obj.meta_keyword,
            'slug': cms_obj.slug,
            'meta_description': cms_obj.meta_description,
            'username': cms_obj.userid.username,
            'short_description': cms_obj.short_description,
            'cms_file': cms_obj.cmsfile.url,
            'html_description': cms_obj.html_description,
            'create_date': cms_obj.createdate.strftime('%m/%d/%Y %H:%M:%S.%I'),
            'update_date': cms_obj.updatedate.strftime('%m/%d/%Y %H:%M:%S.%I'),
            'status': cms_obj.status
    }
