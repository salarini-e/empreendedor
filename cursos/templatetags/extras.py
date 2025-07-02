from django import template
from django.utils.safestring import mark_safe
from ..models import Turma, Turno
from django.db.models import Q
from datetime import date

register = template.Library()


@register.filter(is_safe=True)
def turmas(obj):
    turmas=Turma.objects.filter(Q(status='pre') | Q(status='acc'), curso=obj)
    response=''
    if len(turmas)>0:        
        for turma in turmas:
            if turma.idade_minima and turma.idade_maxima:
                faixa=f"{str(turma.idade_minima)} até {str(turma.idade_maxima)}"
            elif turma.idade_minima:
                faixa=f"{str(turma.idade_minima)}"
            elif turma.idade_minima:
                faixa=f"{str(turma.idade_maxima)}"
            else:
                faixa='Livre'
            
            horarios = ''
            for i in turma.turnos.all():
                horarios += f"<li class='px-2'>{i}</li>"
            
            response+=f"""
            <b class='my-2 p-0'>{str(turma)}</b>
            <ul class='my-2 p-0'><li>Horários:</li> {horarios}</ul> 
                Faixa Etária: {str(faixa)}
            """

    return mark_safe(response)

@register.filter(is_safe=True)
def turmas_input(obj):
    turmas=Turma.objects.filter(Q(status='pre') | Q(status='acc'), curso=obj)
    response=''
    if len(turmas)>0: 
        for turma in turmas:
            if turma.idade_minima and turma.idade_maxima:
                faixa=f"{str(turma.idade_minima)} até {str(turma.idade_maxima)}"
            elif turma.idade_minima:
                faixa=f"{str(turma.idade_minima)}"
            elif turma.idade_minima:
                faixa=f"{str(turma.idade_maxima)}"
            else:
                faixa='Livre'

            turnos = ''
            for turno in turma.turnos.all():
                turnos += f"""
                    <li>{turno.get_dia_semana_display()}, {turno.horario_inicio.strftime("%H:%M")} às {turno.horario_fim.strftime("%H:%M")}</li>
                """
                
            response+=f"""
            <div class="form-check mt-1 turma">
                                                        
                <input class="form-check-input" id="id_turmas_{str(turma.id)}" name="turmas" title="" type="checkbox" value="{str(turma.id)}">
                <label class="form-check-label" for="id_turmas_{str(turma.id)}">
                    {str(turma.curso.nome)} - {str(turma.local)} - Faixa Etária: {str(faixa)}
                    <ul>
                    {turnos}
                    </ul>
                </label>
            </div>
            """

    else:
        response='<i class="ps-4 text-danger">Não há turmas disponíveis.</i>'

    return mark_safe(response)



@register.filter(is_safe=True)
def idade(obj):    
    age = "N/A"
    if obj:
        birthDate=obj
        today = date.today() 
        age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
    
    return mark_safe(f'''<span class="px-3">{age}</span>''')

@register.filter(is_safe=True)
def bg_idade(obj):  
    if obj == None or isinstance(obj, str): 
        return 'N/A'
    
    today = date.today() 
    age = today.year - obj.year - ((today.month, today.day) < (obj.month, obj.day)) 
    if int(age)<int(18):
        return mark_safe(f'''<span class="bg-warning px-3">{age}</span>''')
    else:
        return mark_safe(f'''<span class=" px-3">{age}</span>''')