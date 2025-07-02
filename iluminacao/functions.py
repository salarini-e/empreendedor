# import pandas as pd
# from django.db.models import Count, Avg
# from .models import OrdemDeServico

# def get_os_data_by_month(month, year):
#     # Filtra as OS pelo mês e ano fornecidos
#     os_data = OrdemDeServico.objects.filter(
#         dt_solicitacao__month=month,
#         dt_solicitacao__year=year
#     )

#     return os_data

# def get_os_stats(month, year):
#     os_data = get_os_data_by_month(month, year)

#     # Contagem de OS por bairro
#     os_by_bairro = os_data.values('bairro').annotate(total=Count('id'))

#     # Total de OS
#     total_os = os_data.count()

#     # Média de OS por bairro
#     avg_os = os_by_bairro.aggregate(avg=Avg('total'))

#     # Mediana de OS por bairro
#     median_os = os_by_bairro.aggregate(median=Median('total'))

#     # Pontos atendidos por bairro
#     points_by_bairro = os_data.values('bairro').annotate(total_points=Sum('pontos_atendidos'))

#     # Diferença entre OS abertas e fechadas
#     open_os = os_data.filter(status='0').count()
#     closed_os = os_data.filter(status='f').count()
#     difference = closed_os - open_os

#     return {
#         'os_by_bairro': os_by_bairro,
#         'total_os': total_os,
#         'avg_os': avg_os,
#         'median_os': median_os,
#         'points_by_bairro': points_by_bairro,
#         'difference': difference
#     }
