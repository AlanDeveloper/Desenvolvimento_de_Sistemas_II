# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, session
from ..models.departamento import departamento
from ..models.usuario import usuario
from .. import db
import hashlib

home_bp = Blueprint('us', __name__, url_prefix='/usuario', template_folder='templates')

@home_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST' and request.form['opt'] != '':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        resp = usuario(nome,email,senha)
        resp.idDepto = request.form['opt']
        
        usuario.adicionar(resp)
        return redirect('/usuario/listar')
    else:
        lista = departamento.listar()
        return render_template('usuario/form.html', lista=lista)

@home_bp.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        u = usuario.entrar(email, senha)

        if u == None:
            return render_template('usuario/login.html', info='Usuário não encontrado')
        else:
            session['logged_in'] = True
            session['nome'] = u.nome
            session['id'] = u.id
            return render_template('base.html')
    else:
        return render_template('usuario/login.html', info=None)

@home_bp.route('/sair', methods=['GET','POST'])
def sair():
    session['logged_in'] = False
    del session['nome']
    del session['id']
    
    return redirect('/')


@home_bp.route('/listar', methods=['GET'])
def listar():
    lista = usuario.listar()
    return render_template('usuario/list.html', lista=lista)

@home_bp.route('/deletar/<id>', methods=['GET', 'POST'])
def deletar(id):
    usuario.deletar(id)
    return redirect('/usuario/listar')

@home_bp.route('/atualizar/<id>', methods=['GET', 'POST'])
def atualizar(id):
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        resp = usuario(nome,email,senha)
        resp.id = id

        usuario.atualizar(resp)
        return redirect('/usuario/listar')
    else:
        u = usuario.buscar(id=id)
        return render_template('usuario/alt.html', u=u)