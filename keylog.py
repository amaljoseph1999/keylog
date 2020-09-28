from flask import Flask,render_template,request, redirect,session
from DBConnection import Db
import datetime

app = Flask(__name__)
db=Db()
app.secret_key="abc"



@app.route('/')
def log_in():
    return render_template("login.html")

@app.route('/login',methods=['post'])
def login():
    userid = request.form['name']
    pw = request.form['passwd']
    qry = "select * from login where  name='"+userid+"' and passwd='"+pw+"'"
    res = db.selectOne(qry)
    if res==None:
         "<scirpt>alert('')</script>"
    else:
        print("success")
        tp=res['type']
        session['lid']=res['loginid']
        if tp=="admin":
            return redirect("/admin_home")
        elif tp=="employee":
            return redirect("/emp_home")
        elif tp == "department":
            return redirect("/dep_home")
        else:
            return "/"




@app.route('/admin_home')
def hello_world():
    return render_template("admin/admin_home.html")

@app.route('/add_dept')
def add_dept():
    return render_template("admin/dep_mgnt.html")

@app.route('/add_dept_post',methods=['post'])
def add_dept_post():
    dept=request.form['department']
    passwd = request.form['email']
    import random
    pwd=random.randint(00000,99999)
    qry2 = "insert into login(name,passwd,type) values('" + passwd + "','"+str(pwd)+"','department')"
    res1 = db.insert(qry2)
    qry="insert into dept values('"+str(res1)+"','"+dept+"','"+passwd+"')"
    res=db.insert(qry)
    return render_template("admin/dep_mgnt.html")

@app.route('/view_dept')
def view_dept():
    qry="select * from dept"
    res=db.select(qry)
    return render_template("admin/view_dep.html",data=res)


@app.route('/dept_dlt/<i>')
def dept_dlt(i):
    qry="delete from dept where dept_id='"+i+"'"
    res=db.delete(qry)
    return view_dept()


@app.route('/dep_edit/<i>')
def dep_edit(i):
    qry="select * from dept where dept_id='"+i+"'"
    res=db.selectOne(qry)
    return render_template("admin/dep_edit.html",data=res)


@app.route('/dept_editb',methods=['post'])
def dept_editb():
    deptname=request.form['dep_name']
    did=request.form['did']
    qry="update dept set name='"+deptname+"' where dept_id='"+str(did)+"'"
    res=db.update(qry)
    return view_dept()


@app.route('/add_work')
def add_work():
    qry = "select * from dept"
    res = db.select(qry)

    return render_template("admin/add_work.html",data=res)


@app.route('/add_work_post',methods=['post'])
def add_work_post():
    work=request.form['work']
    dep_id=request.form['dep']
    qry="insert into work (dep_id,w_work) values('"+dep_id+"','"+work+"')"
    res=db.insert(qry)
    return '<script>alert("Inserted")</script>'

@app.route('/edit_work1/<i>')
def edit_work(i):
    qry = "select * from work where workid='" + i + "'"
    res = db.selectOne(qry)
    return render_template("admin/edit_work1.html", data=res)

@app.route('/work_editb/<a>',methods=['post'])
def work_editb(a):
    type=request.form['worktype']
    work=request.form['work']

    qry="update work set w_type='"+type+"',w_work='"+work+"' where workid='"+a+"'"
    res=db.update(qry)
    return '<script>alert("updated")</script>'


@app.route('/work_dlt/<i>')
def work_dlt(i):
    qry="delete from work where workid='"+i+"'"
    res=db.delete(qry)
    return '<script>alert("Deleted")</script>',view_work()


@app.route('/view_work')
def view_work():
    qry = "select * from work inner join dept group by workid "
    res = db.select(qry)
    return render_template("admin/view_work.html", data=res)


@app.route('/add_emp')
def add_emp():
    db = Db()
    qry = "select * from dept"
    res = db.select(qry)
    return render_template("admin/add_emp.html",data=res)


@app.route('/add_emp_post',methods=['post'])
def add_emp_post():
    emp_name = request.form['names']
    emp_lastname = request.form['lastname']
    emp_post = request.form['posts']
    emp_house = request.form['house']
    emp_street = request.form['street']
    emp_place = request.form['place']
    emp_dis = request.form['dis']
    emp_pin = request.form['pin']
    emp_mob = request.form['mob']
    emp_gender = request.form['gender']
    emp_date = request.form['date1']
    emp_email = request.form['email1']
    dept = request.form['dept']
    photo=request.files['image1']
    data=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    photo.save("C:\\Users\\id\\PycharmProjects\\keylog\\static\\employee\\"+data+".jpg")
    path="static/employee/"+data+'.jpg'
    print(photo)
    qry2="insert into login(name,passwd,type) values('"+emp_email+"','emp','employee')"
    res1=db.insert(qry2)
    print(res1)
    qry = "insert into emp(emp_id,first_name,last_name,post,house,street,Place,district,pin_code,mob_no,email,gender,DOB,dept_id,photo,login_id) values('" + str(res1) + "','" + emp_name + "','"+emp_lastname+"','"+emp_post+"','"+emp_house+"','"+emp_street+"','"+emp_place+"','"+emp_dis+"','"+emp_pin+"','"+emp_mob+"','"+emp_email+"','"+emp_gender+"','"+emp_date+"','"+path+"','"+dept+"','"+str(res1)+"')"
    res = db.insert(qry)
    return '<script>alert("inserted")</script>'

@app.route('/view_emp')
def view_emp():
    db = Db()
    qry = "select * from emp"
    res = db.select(qry)
    return render_template("admin/view_emp.html", data=res)


@app.route('/edit_emp/<i>')
def edit_emp(i):
    qry = "select * from dept"
    res1 = db.select(qry)

    qry = "select * from emp where login_id='" + i + "'"
    res = db.selectOne(qry)
    return render_template("admin/edit_emp.html", i=res,data=res1)


@app.route('/edit_emp_post/<i>',methods=['post'])
def edit_emp_post(i):
    emp_name = request.form['name']
    emp_lastname = request.form['lastname']
    emp_post = request.form['post']
    emp_house = request.form['house']
    emp_street = request.form['street']
    emp_place = request.form['place']
    emp_dis = request.form['dis']
    emp_pin = request.form['pin']
    emp_mob = request.form['mob']
    emp_dept = request.form['dept']
    emp_gender = request.form['gender']
    # print(emp_gender)
    emp_date = request.form['date']
    emp_email = request.form['email']
    photo=request.files['image']
    ss=photo.filename
    if ss=='':
              qry = "update emp set first_name='" + emp_name + "',last_name='" + emp_lastname + "',post='" + emp_post + "',house='" + emp_house + "',street='" + emp_street + "',Place='" + emp_place + "',district='" + emp_dis + "',pin_code='" + emp_pin + "',mob_no='" + emp_mob + "',email='" + emp_email + "',gender='" + emp_gender + "',DOB='" + emp_date + "',dept_id='"+emp_dept+"' where emp_id='" + i + "'"
              res = db.update(qry)
    else:

         data=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
         photo.save("C:\\Users\\id\\PycharmProjects\\keylog\\static\\employee\\"+data+".jpg")
         path="static/employee/"+data+'.jpg'
         print(path)
         qry = "update emp set first_name='" + emp_name + "',last_name='" + emp_lastname + "',post='" + emp_post + "',house='" + emp_house + "',street='" + emp_street + "',Place='" + emp_place + "',district='" + emp_dis + "',pin_code='" + emp_pin + "',mob_no='" + emp_mob + "',email='" + emp_email + "',gender='" + emp_gender + "',DOB='" + emp_date + "',dept_id='"+emp_dept+"',photo='" + path + "' where login_id='" + i + "'"
         res=db.update(qry)
    return view_emp()



@app.route('/emp_dlt/<i>')
def emp_dlt(i):
    qry="delete from emp where login_id='"+i+"'"
    res=db.delete(qry)
    return view_emp()

@app.route('/view_comp')
def view_comp():
    qry = "select complaint.comp_id,complaint.emp_id,complaint.complaint1,complaint.cdate,emp.first_name,emp.photo,emp.last_name from emp inner join complaint  on complaint.emp_id=emp.login_id"
    res = db.select(qry)
    return render_template("admin/view_complaint.html",data=res)


@app.route('/reply/<i>')
def reply(i):
    return render_template("admin/reply_complaint.html",data=i)


@app.route('/reply1',methods=["post"])
def reply1():

    rp=request.form["textarea"]
    cid=request.form["cid"]
    qry = "update  complaint set  reply='"+rp+"',reply_date=now() where comp_id='"+cid+"' "
    res = db.update(qry)
    qry = "select complaint.comp_id,complaint.emp_id,complaint.complaint1,complaint.cdate,emp.first_name,emp.photo,emp.last_name from emp inner join complaint  on complaint.emp_id=emp.login_id"
    rs = db.select(qry)
    return render_template("admin/view_complaint.html", data=rs)


@app.route('/view_feedback')
def view_feedback():
    qry = "select emp.first_name,emp.last_name,emp.photo,feedback.* from feedback inner join emp on emp.login_id=feedback.userid"
    res = db.select(qry)
    return render_template("admin/view_feedback.html",data=res)


# ===============================================================================================
@app.route('/emp_home')
def emp_home():
    return render_template("employee/emp_home.html")


@app.route('/myprofile')
def myprofile():
    id = session['lid']
    qry = "select * from emp where emp_id='"+str(id)+"'"
    print(id)
    res = db.selectOne(qry)
    return render_template("employee/profile.html",i=res)

@app.route('/myprofile_post',methods=['post'])
def myprofile_post():
    att= request.form['radio']
    id = session['lid']
    if att=='in':
       qry="insert into attendance(emp_id,checkin,adate) values('"+str(id)+"',now(),curdate())"
       res=db.insert(qry)
    elif att=='out':
       qry1 = "select * from attendance where emp_id='"+str(id)+"' and adate=curdate()"
       d=db.select(qry1)
       if d==None:
           print("please checkIn")
       else:
           qry = "update  attendance set  checkout=now() where emp_id='"+str(id)+"' and adate=curdate()"
           res = db.insert(qry)
    else:
        return emp_home()

    return emp_home()

@app.route('/view_assign_work')
def view_assign_work():
    db=Db();
    id=session['lid']
    # print(str(id)+"=================")
    qry = "select * from workassign,work where workassign.emp_id='"+str(id)+"' AND work.workid=workassign.workid"
    res = db.select(qry)
    return render_template("employee/view_assign_work.html", data=res)


@app.route('/work_status')
def work_status():
    id = session['lid']
    qry = "select distinct work.workid as id,work.w_work as nm from work_status,work where work.workid=work_status.work_id and emp_id='" + str(id) + "'"
    res = db.select(qry)
    return render_template("employee/work_status.html",data=res)

@app.route('/work_status_post',methods=['post'])
def work_status_post():
    workid = request.form["work"]
    status = request.form["status"]
    qry="update work_status set status='"+workid+"',date=curdate() where work_id='"+workid+"'"
    res=db.update(qry)

    return '<script>alert("Send")</script>'

@app.route('/file_sharing')
def file_sharing():
    id = session['lid']
    qry="select * from emp where login_id = '"+str(id)+"'"
    res=db.selectOne(qry)
    # print(qry)
    dept=res['dept_id']
    # print(dept)
    qry1="select * from emp where dept_id='"+str(dept)+"' and login_id!='"+str(id)+"'"
    # print(qry1)
    res1=db.select(qry1)
    print(res1)
    return render_template("employee/file_sharing.html",data=res1)

@app.route('/view_attendance')
def view_attendance():
    id = session['lid']
    print(str(id)+"=================")
    qry = "select * from attendance where emp_id='"+str(id)+"'  "
    res = db.select(qry)
    return render_template("employee/view_attendance.html",data=res)

@app.route('/send_leave_request')
def send_leave_request():
     return render_template("employee/send_leave_request.html")

@app.route('/leave_request_post',methods=['post'])
def leave_request_post():
    dt=request.form['date']
    re = request.form['reason']
    id = session['lid']
    qry="insert into leave1(emp_id,ldate,lreason) values('"+str(id)+"','"+dt+"','"+re+"')"
    res=db.insert(qry)
    return render_template("employee/send_leave_request.html")

@app.route('/send_workfile/<i>')
def send_workfile(i):
    return render_template("employee/send_work.html",data=i)

@app.route('/send_work_post/<i>',methods=['post'])
def send_work_post(i):
    file=request.files['work']
    des = request.form['des']
    sts = request.form['sts']
    id = session['lid']
    data = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    file.save("C:\\Users\\id\\PycharmProjects\\keylog\\static\\employee\\" + data + file.filename)
    path = "static/employee/" + data + file.filename
    qry="insert into file(ffile,description,fdate,workid,emp_id) values('"+path+"','"+des+"',curdate(),'"+i+"','"+str(id)+"') "
    res=db.insert(qry)

    qry="insert into work_status values(null,'"+str(id)+"','"+i+"','"+sts+"',now()) "
    res=db.insert(qry)
    return render_template("employee/send_work.html")


@app.route('/share_files',methods=['post'])
def share_files():
    file=request.files['work']
    rid = request.form['employee']
    lid = session['lid']
    dat = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    file.save("C:\\Users\\id\\PycharmProjects\\keylog\\static\\file_shares\\" + dat + file.filename)
    path = "static/file_shares/" + dat + file.filename

    qry="insert into fileshare(ffile,send_id,rec_id,fdate) values('"+path+"','"+rid+"','"+str(lid)+"',curdate())"
    res=db.insert(qry)
    return render_template("employee/file_sharing.html")


@app.route('/view_revfile')
def view_revfile():
    id = session['lid']
    qry = "select * from fileshare,emp where emp_id=send_id and rec_id='"+str(id)+"'"
    res = db.select(qry)
    return render_template("employee/view_rev.html",data=res)

@app.route('/view_sendfile')
def view_sendfile():
    id = session['lid']
    qry = "select * from fileshare,emp where emp_id=send_id and send_id='"+str(id)+"'"
    res = db.select(qry)
    return render_template("employee/view_send.html",data=res)


@app.route('/view_leave_request')
def view_leave_request():
    id = session['lid']
    print(str(id) + "=================")
    qry = "select * from leave1 where emp_id='" + str(id) + "'  "
    res = db.select(qry)
    return render_template("employee/view_leave.html",data=res)

@app.route('/send_complaint')
def send_complaint():
    return render_template("employee/send_complaint.html")

@app.route('/send_comp_post',methods=['post'])
def send_comp_post():
    id = session['lid']
    com=request.form['complaint']
    qry="insert into complaint (emp_id,complaint1,cdate) values('"+str(id)+"','"+com+"',curdate())"
    res=db.insert(qry)
    return '<script>alert("Send")</script>'

@app.route('/view_comp1')
def view_comp1():
    id = session['lid']
    print(str(id) + "=================")
    qry = "select * from complaint where emp_id='"+str(id)+"'  "
    res = db.select(qry)
    return render_template("employee/view_complaints.html",data=res)


@app.route('/send_feedback/<a>')
def send_feedback(a):
    return render_template("employee/send_feedback.html",data=a)


@app.route('/send_feedback_post/<i>',methods=['post'])
def send_feedback_post(i):
    db=Db()
    feedback=request.form['feedback']
    # date=datetime.datetime.now()
    id=session['lid']
    qry="insert into feedback(ftype,fdate,userid,workid) values('"+feedback+"',curdate(),'"+str(id)+"','"+i+"')"
    res=db.insert(qry)
    return '<script>alert("Send")</script>'


@app.route('/emp_edit_work')
def emp_edit_work():
    return render_template("employee/edit_work.html")





##-----------------------------------------------------------------------------------------

@app.route('/dep_home')
def dep_home():
    return render_template("department/view_dep_profile.html")


@app.route('/dep_assign_work')
def dep_assign_work():
    lid = session['lid']
    qry = "select * from work where dep_id='"+str(lid)+"'"
    res = db.select(qry)
    print(lid)
    return render_template("department/dep_assign_work.html",data=res)


@app.route('/dep_status')
def dep_status():
    return render_template("department/dep_status.html")


@app.route('/leave_status')
def leave_status():
    lid = session['lid']
    qry = "select * from leave1,emp where leave1.emp_id=emp.emp_id and emp.dept_id="'+str(lid)+'""
    res = db.select(qry)
    return render_template("department/leave_status.html",data=qry)

@app.route('/date')
def date():
    lid=session['lid']

    qry=db.select('select * from attendance,emp where attendance.emp_id=emp.emp_id and emp.dept_id="'+str(lid)+'" order by adate')
    print(qry)
    return render_template('department/date.html',data=qry)


@app.route('/view_emp_attend',methods=['post'])
def view_emp_attend():
    lid = session['lid']
    adate=request.form['date']
    qry = db.select('select * from attendance,emp where attendance.emp_id=emp.emp_id and adate="'+adate+'"and emp.dept_id="'+str(lid)+'" order by adate')
    return render_template("department/date.html",data=qry)

@app.route('/work_assign/<n>')
def work_assign(n):
    lid = session['lid']
    work_id=n;
    print(work_id)
    qry = "select * from emp where dept_id='"+str(lid)+"'"
    res = db.select(qry)
    return render_template("department/emp_display.html",data=res,wid=n)

@app.route('/work_assiqn_post/<id>',methods=['post'])
def work_assiqn_post(id):
    emp_id=request.form['emp']
    qry="insert into workassign(workid,emp_id,date) values('"+id+"','"+emp_id+"',curdate())"
    res=db.insert(qry)
    return '<script>alert("Success")</script>'


@app.route('/work_view')
def work_view():
    lid=session['lid']
    print(str(lid))
    qry=db.select('select * from workassign,emp where  workassign.emp_id=emp.login_id and emp.dept_id="'+str(lid)+'"  order by workassign.assign_id' )
    print('mmmm',qry)
    return render_template('department/view_work.html',data1=qry)

@app.route('/view_work_emp',methods=['post'])
def view_work_emp():
    lid = session['lid']
    empid=request.form['emp']
    qry = db.select('select * from workassign,emp,work,file where workassign.workid=work.workid and workassign.emp_id=emp.login_id and workassign.emp_id=5 group by workassign.assign_id')
    return render_template("department/view_work.html",data=qry)


# @app.route('/dep_assign_work')
# def dep_assign_work():
#     return render_template("department/assign_work.html")



if __name__ == '__main__':
    app.run(debug=True)
