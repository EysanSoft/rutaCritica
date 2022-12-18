def queryAperturaMaterias(listaPeriodo,clave):
    consulta = f'''
                select mat.materiaid, mat.Nombre, mat.Periodo from d_materia mat
                left join d_planestudios plan on mat.PlanEstudiosID = plan.PlanEstudiosID
                where mat.Periodo in {str(tuple(listaPeriodo))} and plan.clave = {clave}
                '''
    return consulta

def queryDatosAlumno(matricula):
    consulta = f'''
                SELECT cal.Matricula, cal.materiaid, mat.Nombre, mat.periodo, cal.Final, cal.Aprobado FROM d_calificaciones cal 
                LEFT JOIN d_materia mat ON mat.MateriaID = cal.MateriaID 
                LEFT JOIN d_planestudios plan ON plan.PlanEstudiosID = mat.PlanEstudiosID 
                LEFT JOIN c_estatuscardex e ON e.EstatusCardexID = cal.EstatusCardexID 
                WHERE cal.Matricula = {matricula}
                '''
    return consulta

def queryListaMaterias(clave):
    consulta = f'''
                select mat.MateriaID, mat.Nombre, mat.Objetivo, mat.HorasSemana, mat.TotalHoras, mat.Periodo, mat.TipoPrerequisito from d_materia mat #mat.nombre
                left join d_planestudios plan on mat.PlanEstudiosID = plan.PlanEstudiosID
                where plan.clave = {clave}
                '''
    return consulta

def queryMateriaInfoByName(nombre,clave):
    consulta = f'''
                select mat.MateriaID, mat.Nombre, mat.Objetivo, mat.HorasSemana, mat.TotalHoras, mat.Periodo, mat.TipoPrerequisito from d_materia mat
                left join d_planestudios plan on mat.PlanEstudiosID = plan.PlanEstudiosID
                where mat.Nombre = '{nombre}' and plan.clave = {clave}
                '''
    return consulta

def findMatricula(matricula):
    consulta = f'''
                select distinct Matricula from d_calificaciones where Matricula = {matricula}
                '''
    return consulta