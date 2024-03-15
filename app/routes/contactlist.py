
from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import ContactList
from app.classes.forms import ContactListForm
from flask_login import login_required
import datetime as dt

#view all
@app.route('/contactList/list')
@app.route('/contactLists')
@login_required
def contactListList():
     contactLists = ContactList.objects()
     return render_template('contactLists.html',contactLists=contactLists)

#view 1
@app.route('/contactList/<contactListID>')
@login_required
def contactList(contactListID):
    thisContactList = ContactList.objects.get(id=contactListID)
    return render_template('contactList.html',contactList=thisContactList)

#delete
@app.route('/contactList/delete/<contactListID>')
@login_required
def contactListDelete(contactListID):
    deleteContactList = ContactList.objects.get(id=contactListID)
    if current_user == deleteContactList.author:
        deleteContactList.delete()   
        flash('The Contact was deleted.')
    else:  
        flash("You can't delete a contact you don't own.")
    contactLists = ContactList.objects()  
    return render_template('contactLists.html',contactLists=contactLists)

#create
@app.route('/contactList/new', methods=['GET', 'POST'])
@login_required
def contactListNew():
    form = ContactListForm()
    if form.validate_on_submit():
        newContactList = ContactList(
            fName = form.fName.data, 
            lName = form.lName.data,
            email = form.email.data,
            phone_num = form.phone_num.data,
            author = current_user.id,
            modify_date = dt.datetime.utcnow  
        )
        newContactList.save()
        return redirect(url_for('contactList',contactListID=newContactList.id))
    return render_template('contactListform.html',form=form)

#edit
@app.route('/contactList/edit/<contactListID>', methods=['GET', 'POST'])
@login_required
def contactListEdit(contactListID):
    editContactList = ContactList.objects.get(id=contactListID)
    if current_user != editContactList.author:
        flash("You can't edit a contact you don't own.")
        return redirect(url_for('contactList',contactListID=contactListID))
    form = ContactListForm()
    if form.validate_on_submit():
        editContactList.update(
            fName = form.fName.data, 
            lName = form.lName.data,
            email = form.email.data,
            phone_num = form.phone_num.data,
            modify_date = dt.datetime.utcnow
        )
        return redirect(url_for('contactList',contactListID=contactListID))
    form.fName.data = editContactList.fName
    form.lName.data = editContactList.lName
    form.email.data = editContactList.email
    form.phone_num.data = editContactList.phone_num
    return render_template('contactListform.html',form=form)
