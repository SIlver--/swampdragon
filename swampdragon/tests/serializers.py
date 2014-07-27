from ..serializers.django_model_serializer import DjangoModelSerializer
from ..serializers.model_serializer import ModelSerializer

################################
# Old school serializers
################################


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = 'tests.Department'
        publish_fields = ['name', 'company_id', 'staff']
        update_fields = ['name']

    def serialize_staff(self, obj=None, serializer=None, ignore_fields=[]):
        return [StaffSerializer().serialize(s, ignore_fields=['departments']) for s in obj.staff.all()]


class StaffSerializer(ModelSerializer):
    documents = 'serializers.DocumentSerializer'

    class Meta:
        model = 'tests.Staff'
        publish_fields = ['name', 'department.company.id', 'documents']
        update_fields = ['name']
        documents_serializer = 'tests.DocumentSerializer'

    # def serialize_documents(self, obj=None, serializer=None):
    #     import ipdb;ipdb.set_trace()
    #     return [serializer.serialize(d, ignore_fields=['staff']) for d in obj.documents.all()]


class LogoSerializer(ModelSerializer):
    class Meta:
        model = 'tests.CompanyLogo'
        publish_fields = ['url']


class CompanySerializer(ModelSerializer):
    class Meta:
        model = 'tests.Company'
        publish_fields = ['name', 'age', 'departments', 'logo', 'custom_field']
        update_fields = ['name', 'age']
        departments_serializer = DepartmentSerializer
        logo_serializer = LogoSerializer

    def serialize_custom_field(self, obj=None, serializer=None, ignore_fields=[]):
        return 'custom field'


class DocumentSerializer(ModelSerializer):
    staff = StaffSerializer

    class Meta:
        model = 'tests.Document'
        publish_fields = ['name', 'content', 'staff']
        staff_serializer = StaffSerializer

    # def serialize_staff(self, obj=None, serializer=None, ignore_fields=[]):
    #     return [serializer.serialize(o, ignore_fields=['documents']) for o in obj.staff.all()]


################################
# New serializeres
################################
class FooSerializer(ModelSerializer):
    bars = 'tests.BarSerializer'

    class Meta:
        publish_fields = ('test_field_a', 'bars')
        update_fields = ('test_field_a', 'test_field_b', 'bars')
        model = 'tests.FooModel'


class BarSerializer(ModelSerializer):
    foo = FooSerializer

    class Meta:
        model = 'tests.BarModel'
        update_fields = ('number', 'foo')
        publish_fields = ('number', 'foo')


class BazSerializer(ModelSerializer):
    bar = BarSerializer

    class Meta:
        model = 'tests.BazModel'
        update_fields = ('name', 'bar')
        publish_fields = ('name', 'bar')


class QuxSerializer(ModelSerializer):
    foos = FooSerializer

    class Meta:
        model = 'tests.QuxModel'
        publish_fields = ('value', 'foos')
        update_fields = ('value', 'foos')
