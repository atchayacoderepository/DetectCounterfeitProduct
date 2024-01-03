from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from datetime import datetime
import mysql.connector
mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
charset="utf8",
database="product_bc"
)
@app.route('/login', methods=['GET', 'POST'])
def login():
msg=""
act = request.args.get('act')
if request.method=='POST':
uname=request.form['uname']
pwd=request.form['pass']
cursor = mydb.cursor()
cursor.execute('SELECT * FROM pr_manufacture WHERE uname = %s AND pass =
%s', (uname, pwd))
account = cursor.fetchone()
if account:
ff1=open("log.txt","w")
ff1.write(uname)
ff1.close()

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

54

session['username'] = uname
return redirect(url_for('product'))
else:
# Account doesnt exist or username/password incorrect
msg = 'Incorrect username/password!'

return render_template('index.html',msg=msg,act=act)

<form role="form" method="post" action="/login" class="form-horizontal">
<div class="form-group">
<div class="col-sm-12">

<input class="form-
control" name="uname" placeholder="Username" type="text" required>

</div>
</div>
<div class="form-group">
<div class="col-sm-12">

<input class="form-
control" name="pass" placeholder="Password" type="password" required>

</div>
</div>
<div class="row">
<div class="col-sm-10">
<button type="submit"

class="btn btn-light btn-radius btn-brd grd1">

Login
</button>

</div>
</div>
</form>

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

55

Add Product
@app.route('/product', methods=['GET', 'POST'])
def product():
msg=""
uname=""
if 'username' in session:
uname = session['username']
print(uname)
cursor = mydb.cursor()
ff1=open("log.txt","r")
company=ff1.read()
ff1.close()

cursor.execute('SELECT count(*) FROM pr_product where company=%s',(company, ))
cnpr = cursor.fetchone()[0]

cursor.execute('SELECT * FROM pr_product where company=%s order by id
desc',(company, ))
data = cursor.fetchall()

cursor.execute('SELECT * FROM pr_category')
catt = cursor.fetchall()
if request.method=='POST':
cat=request.form['category']
prd=request.form['product']
price=request.form['price']
description=request.form['description']
location=request.form['location']
mdate=request.form['mdate']
num_piece=request.form['num_piece']

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

56

num_start="1"
plen=len(num_piece)
numStr1 = num_start.zfill(plen)
numStr2 = num_piece.zfill(plen)

mycursor = mydb.cursor()
mycursor.execute("SELECT max(id)+1 FROM pr_product")
maxid = mycursor.fetchone()[0]
if maxid is None:
maxid=1

numStr = str(maxid)
numStr = numStr.zfill(4)
now = datetime.datetime.now()
rdate=now.strftime("%d-%m-%Y")
my=now.strftime("%y%m")

xn=randint(1000, 9999)
pcode="K"+numStr
code1=pcode+"P"+numStr1
code2=pcode+"P"+numStr
sql = "INSERT INTO
pr_product(id,category,product,company,price,description,location,mdate,pcode,rdate,num_p
iece,code1,code2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
val =
(maxid,cat,prd,company,price,description,location,mdate,pcode,rdate,num_piece,code1,code
2)
cursor.execute(sql, val)
mydb.commit()
print(cursor.rowcount, "Added Success")
result="sucess"

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

57

##BC##
sdata="PID:"+str(maxid)+", Product:"+prd+", Company:"+company+",
Manufacture:"+mdate+",KYP Code:"+code1+" to "+code2+", RegDate:"+rdate
result = hashlib.md5(sdata.encode())
key=result.hexdigest()

mycursor1 = mydb.cursor()
mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
maxid1 = mycursor1.fetchone()[0]
if maxid1 is None:
maxid1=1
pkey="00000000000000000000000000000000"
else:
mid=maxid1-1
cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
pp = cursor.fetchone()
pkey=pp[3]
sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype)
VALUES (%s, %s, %s, %s, %s,%s)"
val2 = (maxid1,maxid,pkey,key,sdata,'PID')
cursor.execute(sql2, val2)
mydb.commit()
##
if cursor.rowcount==1:
msg="success"
return redirect(url_for('product',msg=msg))
else:
msg="fail"
return redirect(url_for('product',msg=msg))
#msg='Already Exist'
return render_template('product.html',catt=catt,data=data,cnpr=cnpr)

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

58

Send Product to Distributor
@app.route('/prd_send', methods=['GET', 'POST'])
def prd_send():
msg=""
act=""
uname=""
if 'username' in session:
uname = session['username']
print(uname)
ff1=open("log.txt","r")
company=ff1.read()
ff1.close()

pid = request.args.get('pid')

now = datetime.datetime.now()
rdate=now.strftime("%d-%m-%Y")

cursor = mydb.cursor()

cursor.execute('SELECT * FROM pr_supplier where owner=%s',(company, ))
catt = cursor.fetchall()
# where status=0
cursor.execute('SELECT * FROM pr_product where id=%s',(pid, ))
dd1 = cursor.fetchone()
tot=dd1[21]
pcode=dd1[9]
tot1=str(tot)

if request.method=='POST':

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

59
num_prd=request.form['num_prd']
supp=request.form['supplier']
pid=request.form['pid']

num=int(num_prd)
cursor.execute('SELECT sum(num_prd) FROM pr_send where pid=%s',(pid, ))
sn1 = cursor.fetchone()[0]
if sn1 is None:
sn1=0
bal=tot-sn1

if bal>=num:

num_start=sn1+1
num_end=sn1+num
num_s=str(num_start)
num_e=str(num_end)
plen=len(tot1)
numStr1 = num_s.zfill(plen)
numStr2 = num_e.zfill(plen)
code1=pcode+"P"+numStr1
code2=pcode+"P"+numStr2

balance=tot-num_end

cursor.execute("SELECT max(id)+1 FROM pr_send")
maxid2 = cursor.fetchone()[0]
if maxid2 is None:
maxid2=1

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

60

sql3 = "INSERT INTO
pr_send(id,pid,num_prd,prd_from,prd_to,prd1,prd2,company,supplier,rdate) VALUES (%s,
%s, %s, %s, %s, %s, %s, %s, %s, %s)"
val3 = (maxid2,pid,num_prd,code1,code2,num_start,num_end,company,supp,rdate)
cursor.execute(sql3, val3)
mydb.commit()

cursor.execute('update pr_product set distribute=%s,balance=%s WHERE id = %s',
(num_end,balance, pid))
mydb.commit()
##BC##
sdata="PID:"+pid+", Distribute to:"+supp+", Company:"+company+",
Pcode:"+code1+"-"+code2+", RegDate:"+rdate
result = hashlib.md5(sdata.encode())
key=result.hexdigest()

mycursor1 = mydb.cursor()
mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
maxid1 = mycursor1.fetchone()[0]
if maxid1 is None:
maxid1=1
pkey="00000000000000000000000000000000"
else:
mid=maxid1-1
cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
pp = cursor.fetchone()
pkey=pp[3]
sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype)
VALUES (%s, %s, %s, %s, %s,%s)"
val2 = (maxid1,pid,pkey,key,sdata,'PID')
cursor.execute(sql2, val2)
mydb.commit()

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

61

####

act="1"
msg="Distributed Success"
return redirect(url_for('view_prd'))

else:
act="2"
msg="Product not available!"

return render_template('prd_send.html',catt=catt,act=act,msg=msg,pid=pid)

Retailer Approval
@app.route('/shop_req', methods=['GET', 'POST'])
def shop_req():
msg=""
act=""
sid=""
supplier=""
if 'username' in session:
supplier = session['username']

ff1=open("log.txt","r")
company=ff1.read()
ff1.close()
cursor = mydb.cursor()

###Retailer approval
cursor.execute('SELECT * FROM pr_shop where owner=%s', (company, ))
data = cursor.fetchall()

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

62

cursor.execute('SELECT * FROM pr_supplier where uname=%s',(supplier, ))
data1 = cursor.fetchone()

if request.method=='GET':
sid = request.args.get('sid')
if sid is None:
print("sid")
else:
cursor.execute('update pr_shop set status=1 WHERE id = %s', (sid, ))
mydb.commit()
return redirect(url_for('shop_req',act='1'))

return render_template('shop_req.html',msg=msg,data=data,data1=data1,act=act)

Sale Product
@app.route('/shop_sale', methods=['GET', 'POST'])
def shop_sale():
msg=""
act=""
kid=""
#supplier=""
#if 'username' in session:
# supplier = session['username']

ff1=open("log3.txt","r")
shop=ff1.read()
ff1.close()

now = datetime.datetime.now()
rdate=now.strftime("%d-%m-%Y")

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

63

pid = request.args.get('pid')
rid = request.args.get('rid')

cursor = mydb.cursor()

cursor.execute('SELECT * FROM pr_shop where uname=%s',(shop, ))
data1 = cursor.fetchone()
company=data1[1]
supplier=data1[2]

data=[]

cursor.execute('SELECT * FROM pr_product where id=%s',(pid, ))
data2 = cursor.fetchone()
pcode=data2[9]
tot=data2[21]
tot1=str(tot)
plen=len(tot1)

cursor.execute('SELECT * FROM pr_send2 where id=%s',(rid, ))
data11 = cursor.fetchone()

p1=data11[5]
p2=data11[6]
i=p1
s="0"
while i<p2:
dat=[]

num_start=i

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

64

num_s=str(num_start)
numStr1 = num_s.zfill(plen)
code1=pcode+"P"+numStr1

cursor.execute('SELECT count(*) FROM pr_sale where pcode=%s',(code1, ))
dt = cursor.fetchone()[0]
if dt>0:
s="1"
else:
s="0"

dat.append(i)
dat.append(code1)
dat.append(s)
data.append(dat)
i+=1

#######

if request.method=='GET':
act=request.args.get('act')
kid=request.args.get('kid')
pcode2=request.args.get('pcode2')
if act=="1":

cursor.execute("SELECT max(id)+1 FROM pr_sale")
maxid2 = cursor.fetchone()[0]
if maxid2 is None:
maxid2=1

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

65

sql3 = "INSERT INTO pr_sale(id,shop,pid,rid,kid,pcode,rdate) VALUES (%s, %s,
%s, %s, %s, %s, %s)"
val3 = (maxid2,shop,pid,rid,kid,pcode2,rdate)
cursor.execute(sql3, val3)

#cursor.execute('update pr_send2 set supplier=%s,status=1 WHERE id = %s',
(supplier, i))
#mydb.commit()
##BC##
sdata="PID:"+pid+",:Retailer"+shop+", Product:"+pcode2+", RegDate:"+rdate
result = hashlib.md5(sdata.encode())
key=result.hexdigest()

mycursor1 = mydb.cursor()
mycursor1.execute("SELECT max(id)+1 FROM pr_blockchain")
maxid1 = mycursor1.fetchone()[0]
if maxid1 is None:
maxid1=1
pkey="00000000000000000000000000000000"
else:
mid=maxid1-1
cursor.execute('SELECT * FROM pr_blockchain where id=%s',(mid, ))
pp = cursor.fetchone()
pkey=pp[3]
sql2 = "INSERT INTO pr_blockchain(id,block_id,pre_hash,hash_value,sdata,ptype)
VALUES (%s, %s, %s, %s, %s,%s)"
val2 = (maxid1,pid,pkey,key,sdata,'Sale')
cursor.execute(sql2, val2)
mydb.commit()
####

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

66

act="1"
msg="Request Sent"
return redirect(url_for('shop_sale',pid=pid,rid=rid))

return
render_template('shop_sale.html',msg=msg,data=data,data1=data1,data2=data2,pid=pid,rid=r
id)

Customer Search Product & Verification
if request.method=='POST':
pcode=request.form['pcode']
show="yes"

pp=pcode.split("P")
pcode2=pp[0]

cursor = mydb.cursor()
cursor.execute("SELECT count(*) FROM pr_product where pcode=%s",(pcode2, ))
cnt = cursor.fetchone()[0]
if cnt>0:
act="1"
cursor.execute("SELECT * FROM pr_product where pcode=%s",(pcode2, ))
dd = cursor.fetchone()
pid=dd[0]
company=dd[3]
cursor.execute('SELECT * FROM pr_blockchain where block_id=%s &&
ptype=%s',(pid, 'PID'))
data2 = cursor.fetchall()
'''for ss in data:
ss1=ss[4].split(",")
data1.append()'''

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

67
cursor.execute("SELECT * FROM pr_shop")
data3 = cursor.fetchall()
####Find Manufacture###
code=int(pp[1])
ms1="1"
cursor.execute("SELECT * FROM pr_manufacture where uname=%s",(company, ))
mdata = cursor.fetchone()

cursor.execute("SELECT * FROM pr_product where id=%s",(pid, ))
pdata = cursor.fetchone()

####Find Distributor###
cursor.execute("SELECT count(*) FROM pr_send where pid=%s && prd1<=%s &&
prd2>=%s",(pid, code,code))
dss1 = cursor.fetchone()[0]
if dss1>0:
ms2="1"
cursor.execute("SELECT * FROM pr_send where pid=%s && prd1<=%s &&
prd2>=%s",(pid, code,code))
dss2 = cursor.fetchone()
supplier=dss2[8]

cursor.execute("SELECT * FROM pr_supplier where uname=%s",(supplier, ))
sdata = cursor.fetchone()
else:
ms2="2"
print("none")
####Find Retailer###
cursor.execute("SELECT count(*) FROM pr_send2 where pid=%s && prd1<=%s
&& prd2>=%s",(pid, code,code))
dss2 = cursor.fetchone()[0]

Detect and Prevent Counterfeit Product for Offline and online Sales Using Blockchain Technology

68

if dss2>0:
ms3="1"
cursor.execute("SELECT * FROM pr_send2 where pid=%s && prd1<=%s &&
prd2>=%s",(pid, code,code))
dss2 = cursor.fetchone()
shop=dss2[12]

cursor.execute("SELECT * FROM pr_shop where uname=%s",(shop, ))
rdata = cursor.fetchone()
else:
ms3="2"
print("none")
####SOLD##
cursor.execute("SELECT count(*) FROM pr_sale where pcode=%s",(pcode, ))
scnt = cursor.fetchone()[0]
if scnt>0:
sact="1"
else:
sact=""
#####
else:
act="2"