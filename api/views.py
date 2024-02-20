from rest_framework import viewsets
from api.serializers import EmployeeSerializer,TaskSerializer
from rest_framework.response import Response
from api.models import Employees,Tasks
from rest_framework.decorators import action
from rest_framework import authentication,permissions
# Create your views here.


class EmployeeViewSetView(viewsets.ViewSet):

    def create(self,request,*args,**kwargs):
        serialize=EmployeeSerializer(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(data=serialize.data)
        else:
            return Response(data=serialize.errors)
        
    def list(self,request,*args,**kwargs):
        qs=Employees.objects.all()
        serialize=EmployeeSerializer(qs,many=True)
        return Response(data=serialize.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        serialize=EmployeeSerializer(qs)
        return Response(data=serialize.data)
    

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        employee_object=Employees.objects.get(id=id)
        serialize=EmployeeSerializer(data=request.data,instance=employee_object)
        if serialize.is_valid():
            serialize.save()
            return Response(data=serialize.data)
        else:
            return Response(data=serialize.errors)
        
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Employees.objects.get(id=id).delete()
        return Response(data={"message":"data deleted successfully"})
    

class EmployeeModelViewSetView(viewsets.ModelViewSet):

    permission_classes=[permissions.IsAdminUser]
    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]

    serializer_class=EmployeeSerializer
    model=Employees
    queryset=Employees.objects.all()

    def list(self, request, *args, **kwargs):
        qs=Employees.objects.all()
        if "department"in request.query_params:
            value=request.query_params.get("department")
            qs=qs.filter(department=value)
        serializer=EmployeeSerializer(qs,many=True)
        return Response(data=serializer.data)
    

    
    #localhost:8000/api/v2/employees/departments/
    @action(methods=["get"],detail=False)
    def departments(self,request,*args,**kwargs):
        qs=Employees.objects.all().values_list("department",flat=True).distinct()
        return Response(data=qs)
    

    #localhost:8000/api/v2/employee/{id}/add_task/
    @action(methods=["post"],detail=True)
    def add_task(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        employee_object=Employees.objects.get(id=id)
        serializer=TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=employee_object)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

# list all task of a specified employee/
#  localhost:8000/api/v2/employee/{id}/task/
    # method=get
    
    @action(methods=["get"],detail=True)
    def task(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Tasks.objects.filter(employee__id=id)
        serializer=TaskSerializer(qs,many=True)
        return Response(data=serializer.data)
    

class TaskViewSetView(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.TokenAuthentication]
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        task_object=Tasks.objects.get(id=id)
        serializer=TaskSerializer(data=request.data,instance=task_object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Tasks.objects.get(id=id)
        serializer=TaskSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Tasks.objects.get(id=id).delete()
        return Response(data={"message":"deleted.."})
    
