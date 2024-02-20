from django.urls import path
from api.views import EmployeeViewSetView,EmployeeModelViewSetView,TaskViewSetView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import ObtainAuthToken


router=DefaultRouter()
router.register("v1/employee",EmployeeViewSetView,basename="employee")
router.register("v2/employee",EmployeeModelViewSetView,basename="mempolyee")
router.register("v3/task",TaskViewSetView,basename="task")


urlpatterns=[
    path("v2/token/",ObtainAuthToken.as_view()),
    
] + router.urls