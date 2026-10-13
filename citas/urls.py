from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'citas'

urlpatterns = [
    # Vistas públicas
    path('', views.BienvenidaView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(
        template_name='citas/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.RegistroView.as_view(), name='registro'),

    # Vistas protegidas
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('perfil/', views.perfil, name='perfil'),

    path('medicos/', views.MedicoListView.as_view(), name='medico_list'),

    path('turnos/', views.TurnoListView.as_view(), name='turno_list'),
    path('turnos/nuevo/', views.TurnoCreateView.as_view(), name='turno_create'),
    path('turnos/<int:pk>/', views.TurnoDetailView.as_view(), name='turno_detail'),
    path('turnos/<int:pk>/estado/', views.TurnoEstadoUpdateView.as_view(), name='turno_estado'),
    path('turnos/<int:pk>/cancelar/', views.turno_cancelar, name='turno_cancelar'),

    path('pacientes/nuevo/', views.PacienteCreateView.as_view(), name='paciente_create'),

    path('api/horarios-disponibles/', views.horarios_disponibles, name='horarios_disponibles'),
]
