# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import datetime
import re

class Biblioteca(models.Model):
    _name = 'biblioteca.biblioteca'
    _description = 'Modulo para el manejo de bibliotecas'

    nombre = fields.Char(required=True)
    tipo_documento = fields.Selection([
        ('c', 'Cédula'),
        ('r', 'RUC'),
        ('p', 'Pasaporte')
    ], required=True)
    ruc = fields.Char(string="RUC")
    cedula = fields.Char(string="Cédula")
    pasaporte = fields.Char(string="Pasaporte")
    direccion = fields.Char()
    telefono = fields.Char()
    fecha = fields.Datetime(string="Fecha creación", default=lambda self: datetime.datetime.now())

    @api.onchange("cedula")
    def onchange_cedula(self):
        if self.cedula and not self.validar_cedula(self.cedula):
            raise UserError("Cédula inválida")

    @api.onchange("ruc")
    def onchange_ruc(self):
        if self.ruc and not self.validar_ruc(self.ruc):
            raise UserError("RUC inválido")
        
    @api.onchange("telefono")
    def onchange_telefono(self):
        if self.telefono and not self.validar_telefono(self.telefono):
            raise UserError("Teléfono inválido")

    def validar_cedula(self, ced):
        if len(ced) != 10:
            return False
        
        valores = [int(ced[x]) * (2 - x % 2) for x in range(9)]
        resultado = sum(map(lambda x: x > 9 and x - 9 or x, valores))
        verificador = 10 - int(str(resultado)[-1]) if int(str(resultado)[-1]) != 0 else 0
        
        return int(ced[9]) == verificador

    def validar_ruc(self, ruc):
        if len(ruc) != 13:
            return False

        ban = 0
        verificador = 0
        tipo = int(ruc[2])
        
        if tipo <= 5:
            aux = 2
            for valor in ruc[:9]:
                verificador += int(valor) * aux
                aux = 1 if aux == 2 else 2
                ban += 1
        elif tipo == 9:
            aux = 4
            aux2 = 7
            for valor in ruc[:9]:
                verificador += int(valor) * aux if aux > 1 else int(valor) * aux2
                aux = aux - 1 if aux > 1 else aux
                aux2 = aux2 - 1 if aux2 > 1 else aux2
                ban += 1
        elif tipo == 6:
            aux = 3
            aux2 = 7
            for valor in ruc[:7]:
                verificador += int(valor) * aux if aux > 1 else int(valor) * aux2
                aux = aux - 1 if aux > 1 else aux
                aux2 = aux2 - 1 if aux2 > 1 else aux2
                ban += 1

        if tipo <= 5:
            verificador = verificador % 10
            if verificador != 0:
                verificador = 10 - verificador
            return verificador == int(ruc[9])
        elif tipo == 9 or tipo == 6:
            verificador = verificador % 11
            if verificador != 0:
                verificador = 11 - verificador
            return (tipo == 9 and verificador == int(ruc[9])) or (tipo == 6 and verificador == int(ruc[8]))

        return False

    def validar_telefono(self, telefono):
        # Verifica que el teléfono tenga exactamente 10 dígitos y solo contenga números
        if re.match(r'^\d{10}$', telefono):
            # Verifica si comienza con un prefijo específico, por ejemplo, 09 para Ecuador
            return telefono.startswith('09')
        return False
        

class Personas(models.Model):
    _name = 'biblioteca.personas'
    _description = 'Manejo de personal y clientes para la biblioteca'

    nombre = fields.Char()
    ci = fields.Char()
    telefono = fields.Char()
    direccion = fields.Char()
    sexo = fields.Selection([('m', 'Masculino'),('f', 'Femenino')])
    edad = fields.Integer()
    tipo = fields.Selection([('e', 'Empleado'), ('c','Cliente')])
    biblioteca_id = fields.Many2one('biblioteca.biblioteca')

class Categoria(models.Model):
    _name = 'biblioteca.categoria'

    nombre = fields.Char()
    restriccion = fields.Char()

class Tipo(models.Model):
    _name = 'biblioteca.tipo'
    _description = ''

    nombre = fields.Char()
    descripcion = fields.Text()

class Libros(models.Model):
    _name = 'biblioteca.libros'
    _description = ''

    autor = fields.Char()
    nombre = fields.Char()
    isbn = fields.Char()
    aniopublicacion = fields.Char()
    cantidad = fields.Integer()
    biblioteca_id = fields.Many2one('biblioteca.biblioteca')
    categoria_id = fields.Many2one('biblioteca.categoria')
    tipo_id = fields.Many2one('biblioteca.tipo')

class Prestamo(models.Model):
    _name = 'biblioteca.prestamo'
    _description = ''

    fecha_prestamo = fields.Datetime()
    tiempo = fields.Float()
    retraso = fields.Integer()
    cliente_id = fields.Many2one('biblioteca.personas')	
    empleado_id = fields.Many2one('biblioteca.personas')
    detalle_ids = fields.One2many('biblioteca.detalleprestamos','prestamo_id')


class DetallePrestamos(models.Model):
    _name = 'biblioteca.detalleprestamos'
    _description = ''

    libro_id = fields.Many2one('biblioteca.libros')
    prestamo_id = fields.Many2one('biblioteca.prestamos')


