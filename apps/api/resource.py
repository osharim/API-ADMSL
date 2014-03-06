from django.db.models import Q
from tastypie import fields
from apps.core.models import *
from tastypie.exceptions import BadRequest
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource , ALL , ALL_WITH_RELATIONS
from django.contrib.auth.models import User
from django.db.models import Q


#************************************************************************************************************
#*********************************************Sucursal Inventario  ******************************************
#************************************************************************************************************


class SucursalInventarioResource(ModelResource):

	class Meta:
		queryset = SucursalInventario.objects.all()
		resource_name = 'SucursalInventario'
		authorization= Authorization()




#************************************************************************************************************
#*********************************************Cliente Facturacion *******************************************
#************************************************************************************************************


class ClienteFacturacionResource(ModelResource):

	class Meta:
		queryset = ClienteFacturacion.objects.all()
		resource_name = 'clientefacturacion'
		authorization= Authorization()

#************************************************************************************************************
#*********************************************SUCURSAL ******************************************************
#************************************************************************************************************

class SucursalResource(ModelResource):

	class Meta:
		queryset = Sucursal.objects.all()
		resource_name = 'sucursal'
		authorization= Authorization()


#************************************************************************************************************
#*********************************************   Cliente ****************************************************
#************************************************************************************************************


class ClienteResource(ModelResource):

	#cliente_facturacion = fields.ForeignKey(ClienteFacturacionResource , 'cliente_facturacion'    , full = True , null = True )
	sucursal = fields.ForeignKey(SucursalResource , 'Sucursal'    , full = True , null = True )
	class Meta:
		queryset = ClienteDatos.objects.all()
		resource_name = 'cliente'
		authorization= Authorization()


#************************************************************************************************************
#*********************************************   Logged ****************************************************
#************************************************************************************************************



class LogeedResource(ModelResource):

	class Meta:
		queryset = Logged.objects.all()

#************************************************************************************************************
#*********************************************   Login ****************************************************
#************************************************************************************************************


class LoginResource(ModelResource):


	class Meta:
		excludes = ["password", "email" , "id" , "nombre" , "resource_uri" , "tel_cel"]
		queryset = Usuario.objects.all().distinct()
		allowed_methods = ['get' ]		
		resource_name = 'login'
		limit = 1

		filtering = {  }



	def dehydrate(self , bundle ):

		del bundle.data["resource_uri"]
		get_email= bundle.request.GET.get("email") or False
		get_password = unicode(bundle.request.GET.get("password"))

		user_exist = Usuario.objects.filter( Q(email = get_email ) , Q(password = get_password))

		if user_exist:
			
			bundle.data["loggin"] = True
			bundle.data["message"] = "201"
		else:

			bundle.data["loggin"] = False
			bundle.data["message"] = "Email o password incorrecto"
			del bundle.data["rol"]

		return bundle
	
	def alter_list_data_to_serialize(self, request, data):

		del data["meta"]
		return data
	

#************************************************************************************************************
#*********************************************   Usuario ****************************************************
#************************************************************************************************************



class UsuarioResource(ModelResource):

	"""
	Usuario - Datos del usuario
	"""

	nombre = fields.CharField(attribute='nombre')
	rol = fields.CharField(attribute='rol')
	logged = fields.ForeignKey(LogeedResource, 'Logged'    , full = True , null = True )

	class Meta:
		allowed_methods = ['get', 'post' , 'delete' , "put"]		
		#excludes = ["password"]
		queryset = Usuario.objects.all().distinct()
		resource_name = 'usuario'
		authorization= Authorization()

		filtering = {
		}


	def dehydrate(self , bundle ):

		keyword = User.objects.make_random_password()
		bundle.data["loggin"] = keyword
		del bundle.data["logged"]

		

		return bundle


	def obj_create(self , bundle , request = None , ):
		print bundle.obj

		keyword = User.objects.make_random_password()
		last_loggin = Logged.objects.create( session_key = keyword , access = True )
		bundle.obj.logged  = last_loggin

		print bundle.obj.__dict__

		bundle = self.full_hydrate(bundle)
		bundle.obj.save()


		print bundle.obj.__dict__



		#Usuario.objects.update(pk = bundle.obj ).set(logged = last_loggin )


		return bundle





