# 数据库
```
python3 manage.py makemigrations
python3 manage.py migrate
```

# 创建超级用户
`python3 manage.py createsuperuser` 

# 运行
`python3 manage.py runserver 127.0.0.1:8000`

# 填充数据
GET http://127.0.0.1:8000/admin

# 示例
GET http://127.0.0.1:8000/api/v1/host/?host_ip=172.25.10.10

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "machine_name": "ji11",
            "room_name": "机房",
            "cpu": 64,
            "memory": 128,
            "host_ip": "172.25.10.10",
            "idrac_ip": "172.25.3.10",
            "host_mode": "DELL630",
            "host_active": "有可用资源",
            "physicaldisk": [
                {
                    "disk_name": "datastore33",
                    "disk_space": "3T"
                }
            ]
        }
    ]
}
```