from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import Loja, User, db

class TodoController():
  def index():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    loja = Loja.query.filter_by(user_id=user_id).all()
    return render_template('index.html', loja=loja)

  def create():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    title = request.form.get('title')
    new_todo = Loja(title=title, complete=False, user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()
    flash('Todo criado com suceso', 'success')
    return redirect('/')
  
  def delete(id):
    if 'user_id' not in session:
        return redirect('/login')
    todo = Loja.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deletado com sucesso', 'success')
    return redirect('/')
  
  def complete(id):
    if 'user_id' not in session:
        return redirect('/login')
    todo = Loja.query.filter_by(id=id).first()
    Loja.complete = True
    db.session.commit()
    return redirect('/')
  
  def update(id):
    if 'user_id' not in session:
        return redirect('/login')
    title = request.form.get('title')
    todo = Loja.query.filter_by(id=id).first()
    Loja.title = title
    db.session.commit()
    return redirect('/')
  
class UserController():
  def login():
    return render_template('login.html')

  def signin():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('E-mail não encontrado', 'error')
        return redirect('/login')
    if not check_password_hash(user.password, password):
        flash('Senha incorreta', 'error')
        return redirect('/login')
    session['user_id'] = user.id
    flash('Bem vindo!', 'success')
    return redirect('/')
  
  def register():
    return render_template('register.html')
  
  def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        flash('E-mail já cadastrado', 'error')
        return redirect('/register')
    new_user = User(
        name=name,
        email=email,
        password=generate_password_hash(password, method='sha256')
    )
    db.session.add(new_user)
    db.session.commit()
    flash('Usuário criado com sucesso', 'success')
    return redirect('/login')
  
  def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
    return redirect('/login')