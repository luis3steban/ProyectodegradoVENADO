from django.http import JsonResponse
from django.shortcuts import redirect
from django.db import connection

def obtener_producto_max_produccion_mes():
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT 
                        pr.producto_id,
                        pc.nombre_producto,
                        SUBSTRING(pr.fecha_produccion_mensual, 1, 7) AS año_mes,
                        TRIM(TRAILING '0' FROM FORMAT(pr.cantidad_produccion, 2)) AS cantidad_produccion_mensual
                    FROM 
                        venadobdpredict.produccion_venado pr
                    JOIN 
                        venadobdpredict.productos_venado pc 
                        ON pr.producto_id = pc.id
                    WHERE
                        (SELECT COUNT(*) 
                        FROM venadobdpredict.produccion_venado pr2 
                        WHERE pr2.producto_id = pr.producto_id 
                        AND pr2.fecha_produccion_mensual >= pr.fecha_produccion_mensual) <= 1
                    ORDER BY 
                        pr.cantidad_produccion DESC LIMIT 1;
        """)
        resultado = cursor.fetchone()
    
    if resultado:
        producto_id = resultado[0]
        porcentaje_incremento = resultado[3]  
        return producto_id, porcentaje_incremento
    else:
        return None, None

def obtener_producto_max_produccion_anio():
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT 
                        pr.producto_id,
                        pc.nombre_producto,
                        SUBSTRING(pr.fecha_produccion_mensual, 1, 7) AS año_mes,
                        TRIM(TRAILING '0' FROM FORMAT(pr.cantidad_produccion, 2)) AS cantidad_produccion_anual
                    FROM 
                        venadobdpredict.produccion_venado pr
                    JOIN 
                        venadobdpredict.productos_venado pc 
                        ON pr.producto_id = pc.id
                    WHERE
                        SUBSTRING(pr.fecha_produccion_mensual, 1, 4) = '2020'
                    ORDER BY 
                        pr.cantidad_produccion DESC
                    LIMIT 1 ;
        """)
        resultado = cursor.fetchone()
    
    if resultado:
        producto_id = resultado[0]
        cantidad_produccion_mensual = resultado[3]  
        return producto_id, cantidad_produccion_mensual
    else:
        return None, None
def obtener_producto_disminucion():
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT 
                        producto_id,
                        nombre_producto,
                        año_mes,
                        cantidad_produccion_actual,
                        cantidad_produccion_anterior,
                        diferencia_produccion,
                        CASE 
                            WHEN cantidad_produccion_anterior = 0 THEN NULL
                            ELSE CAST(ROUND(ABS((diferencia_produccion / cantidad_produccion_anterior) * 100)) AS UNSIGNED) -- Redondear, convertir a positivo y a entero
                        END AS porcentaje_incremento
                    FROM (
                        SELECT 
                            pr.producto_id,
                            pc.nombre_producto,
                            SUBSTRING(pr.fecha_produccion_mensual, 1, 7) AS año_mes,
                            pr.cantidad_produccion AS cantidad_produccion_actual,
                            (
                                SELECT pr2.cantidad_produccion
                                FROM venadobdpredict.produccion_venado pr2
                                WHERE pr2.producto_id = pr.producto_id
                                ORDER BY pr2.fecha_produccion_mensual DESC
                                LIMIT 1 OFFSET 1
                            ) AS cantidad_produccion_anterior,
                            pr.cantidad_produccion - (
                                SELECT pr2.cantidad_produccion
                                FROM venadobdpredict.produccion_venado pr2
                                WHERE pr2.producto_id = pr.producto_id
                                ORDER BY pr2.fecha_produccion_mensual DESC
                                LIMIT 1 OFFSET 1
                            ) AS diferencia_produccion
                        FROM 
                            venadobdpredict.produccion_venado pr
                        JOIN 
                            venadobdpredict.productos_venado pc 
                            ON pr.producto_id = pc.id
                        WHERE
                            (
                                SELECT COUNT(*) 
                                FROM venadobdpredict.produccion_venado pr2 
                                WHERE pr2.producto_id = pr.producto_id 
                                AND pr2.fecha_produccion_mensual >= pr.fecha_produccion_mensual
                            ) <= 2
                    ) AS subquery
                    ORDER BY 
                        diferencia_produccion ASC LIMIT 1;
        """)
        resultado = cursor.fetchone()
    
    if resultado:
        producto_id = resultado[0]
        porcentaje_disminucion = resultado[6]  
        return producto_id, porcentaje_disminucion
    else:
        return None, None

def obtener_producto_incremento():
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT 
                        producto_id,
                        nombre_producto,
                        año_mes,
                        cantidad_produccion_actual,
                        cantidad_produccion_anterior,
                        diferencia_produccion,
                        CASE 
                            WHEN cantidad_produccion_anterior = 0 THEN NULL
                            ELSE CAST(ROUND((diferencia_produccion / cantidad_produccion_anterior) * 100) AS UNSIGNED)
                        END AS porcentaje_incremento
                    FROM (
                        SELECT 
                            pr.producto_id,
                            pc.nombre_producto,
                            SUBSTRING(pr.fecha_produccion_mensual, 1, 7) AS año_mes,
                            pr.cantidad_produccion AS cantidad_produccion_actual,
                            (
                                SELECT pr2.cantidad_produccion
                                FROM venadobdpredict.produccion_venado pr2
                                WHERE pr2.producto_id = pr.producto_id
                                ORDER BY pr2.fecha_produccion_mensual DESC
                                LIMIT 1 OFFSET 1
                            ) AS cantidad_produccion_anterior,
                            pr.cantidad_produccion - (
                                SELECT pr2.cantidad_produccion
                                FROM venadobdpredict.produccion_venado pr2
                                WHERE pr2.producto_id = pr.producto_id
                                ORDER BY pr2.fecha_produccion_mensual DESC
                                LIMIT 1 OFFSET 1
                            ) AS diferencia_produccion
                        FROM 
                            venadobdpredict.produccion_venado pr
                        JOIN 
                            venadobdpredict.productos_venado pc 
                            ON pr.producto_id = pc.id
                        WHERE
                            (
                                SELECT COUNT(*) 
                                FROM venadobdpredict.produccion_venado pr2 
                                WHERE pr2.producto_id = pr.producto_id 
                                AND pr2.fecha_produccion_mensual >= pr.fecha_produccion_mensual
                            ) <= 2
                    ) AS subquery
                    ORDER BY 
                        diferencia_produccion DESC LIMIT 1;
        """)
        resultado = cursor.fetchone()
    
    if resultado:
        producto_id = resultado[0]
        porcentaje_incremento = resultado[6] 
        return producto_id, porcentaje_incremento
    else:
        return None, None

