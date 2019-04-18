# header_obj_list = models.PhysicalMachine._meta.fields
def get_headers(header_fields_list):
    header_dic = {}
    for field in header_fields_list:
        header_dic[field.name] = field.verbose_name
    return header_dic
