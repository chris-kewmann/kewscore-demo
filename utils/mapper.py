def map_residence_status(status):
    if status == 'OWNER':
        return 'HOME.OWNER'
    elif status == 'SHARED':
        return 'LIVING.WITH.PARENTS'
    elif status == 'RENT':
        return 'SQUATTER'
    elif status == 'TENANT':
        return 'TENANT'

    return 'OTHER'

def map_occupation(status):
    if status == 'PRIVATE SECTOR':
        return 'PEGAWAI SWASTA'
    elif status == 'GOVERMENT AGENCY':
        return 'PEJABAT/PENYELENGGARA NEGARA'
    elif status == 'HEALTH SECTOR':
        return 'DOKTER'
    elif status == 'ENTREPRENEUR':
        return 'WIRASWASTA'
    elif status == 'ENGINEERING':
        return 'ENGINEERING'
    elif status == 'MILITARY':
        return 'PENGAMANAN'

    return 'OTHER'

def map_user_mb(status):
    if status == 'EMPLOYEE':
        return 'Y'

    return 'N'