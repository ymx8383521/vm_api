from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField,HyperlinkedRelatedField
from api import models
from rest_framework import exceptions


# class BaseSerializer(serializers.ModelSerializer):
#     headers = serializers.SerializerMethodField()
#     def get_headers(self,row):
#         header_obj_list=row._meta.fields
#         header=[]
#         for field in header_obj_list:
#             header.append({field.name:field.verbose_name})
#         return header


class PhysicalMachineSerializer(serializers.ModelSerializer):
    physicaldisk=serializers.SerializerMethodField()
    # 列表表头verbose_name
    # headers=serializers.SerializerMethodField()
    # 中文名称显示
    host_active=serializers.CharField(source='get_host_active_display')
    room_name=serializers.CharField(source='room_site.room_name')

    class Meta:
        model=models.PhysicalMachine
        # fields='__all__'
        fields=('id','machine_name','room_name','cpu','memory','host_ip','idrac_ip','host_mode','host_active','physicaldisk')
        # depth=1

    def get_physicaldisk(self,row):
        # print(row._meta.get_field('cpu').verbose_name)
        # 外键的反向查找
        disk_obj_list=row.physicaldisk_set.all()
        ret=[]
        for obj in disk_obj_list:
            ret.append({'disk_name':obj.disk_name,'disk_space':str(obj.disk_space)+'T'})
        return ret

    # def get_headers(self,row):
    #     header_obj_list=row._meta.fields
    #     header=[]
    #     for field in header_obj_list:
    #         header.append({field.name:field.verbose_name})
    #     return header


class VirtualMachineSerializer(serializers.ModelSerializer):
    # vm_audit=serializers.CharField(source='get_vm_audit_display',required=False)
    host_ip=serializers.CharField(source='host_machine.host_ip',required=False)
    datastore=serializers.CharField(source='vm_datastore.disk_name',required=False)
    room_name=serializers.CharField(source='host_machine.room_site.room_name',required=False)
    class Meta:
        model=models.VirtualMachine
        # fields='__all__'
        # depth=1
        fields=('id','vm_name','vm_cpu','vm_memory','vm_os','vm_disk','vm_ip','vm_gateway','vm_audit','vm_proposer','host_ip','room_name','datastore','vm_installed')
        read_only_fields=('vm_audit',)

    def validate_host_ip(self,value):
        host_machine_obj = models.PhysicalMachine.objects.filter(host_ip=value).first()
        if not host_machine_obj:
            raise exceptions.ValidationError('主机不存在')
        return value

    def validate_datastore(self,value):
        vm_datastore_obj = models.PhysicalDisk.objects.filter(disk_name=value).first()
        if not vm_datastore_obj:
            raise exceptions.ValidationError('磁盘不存在')
        return value

    # 对磁盘所在主机校验
    def validate(self, attrs):
        host_machine=attrs.get('host_machine')
        vm_datastore=attrs.get('vm_datastore')

        if host_machine and vm_datastore:
            host_ip=host_machine['host_ip']
            disk_name=vm_datastore['disk_name']
            host_machine_obj = models.PhysicalMachine.objects.filter(host_ip=host_ip).filter(physicaldisk__disk_name=disk_name).first()
            if not host_machine_obj:
                raise exceptions.ValidationError('主机的磁盘不匹配')
        return attrs

    # 只针对外键做重构
    def create(self, validated_data):
        host_machine=validated_data.pop('host_machine')
        host_ip=host_machine['host_ip']
        vm_datastore=validated_data.pop('vm_datastore')
        datastore_name=vm_datastore['disk_name']
        # get_vm_audit_display=validated_data.pop('get_vm_audit_display')
        # print(get_vm_audit_display)
        host_machine_obj=models.PhysicalMachine.objects.filter(host_ip=host_ip).first()
        vm_datastore_obj=models.PhysicalDisk.objects.filter(disk_name=datastore_name).first()
        # if get_vm_audit_display == '待审核':
        #     vm_audit=0
        # elif get_vm_audit_display == '审核通过':
        #     vm_audit=1
        # else:
        #     vm_audit=2
        return models.VirtualMachine.objects.create(host_machine=host_machine_obj,vm_datastore=vm_datastore_obj,**validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('host_machine'):
            host_machine = validated_data.pop('host_machine')
            host_ip = host_machine['host_ip']
            host_machine = models.PhysicalMachine.objects.filter(host_ip=host_ip).first()
            if host_machine: validated_data['host_machine']=host_machine

        if validated_data.get('vm_datastore'):
            vm_datastore = validated_data.pop('vm_datastore')
            datastore_name = vm_datastore['disk_name']
            vm_datastore= models.PhysicalDisk.objects.filter(disk_name=datastore_name).first()
            if vm_datastore: validated_data['vm_datastore']=vm_datastore

        # print(validated_data)
        instance.vm_name=validated_data.get('vm_name',instance.vm_name)
        instance.vm_cpu=validated_data.get('vm_cpu',instance.vm_cpu)
        instance.vm_memory=validated_data.get('vm_memory',instance.vm_memory)
        instance.vm_os=validated_data.get('vm_os',instance.vm_os)
        instance.vm_disk=validated_data.get('vm_disk',instance.vm_disk)
        instance.vm_ip=validated_data.get('vm_ip',instance.vm_ip)
        instance.vm_gateway=validated_data.get('vm_gateway',instance.vm_gateway)
        instance.vm_audit=validated_data.get('vm_audit',instance.vm_audit)
        instance.vm_installed=validated_data.get('vm_installed',instance.vm_installed)
        instance.vm_proposer=validated_data.get('vm_proposer',instance.vm_proposer)
        instance.host_machine=validated_data.get('host_machine',instance.host_machine)
        instance.vm_datastore=validated_data.get('vm_datastore',instance.vm_datastore)
        instance.save()

        return instance


class MachineRoomSerializer(serializers.ModelSerializer):
    host = serializers.SerializerMethodField()

    class Meta:
        model = models.MachineRoom
        # fields='__all__'
        fields=('id','room_name','host')
        depth=1

    def get_host(self,row):
        # print(row)
        # 外键的反向查找所有主机
        host_obj_list=row.physicalmachine_set.all()
        res=[]
        for obj in host_obj_list:
            res.append({'host_id':obj.id,'host_name':obj.machine_name,'host_ip':obj.host_ip,'idrac_ip':obj.idrac_ip})
        return res


