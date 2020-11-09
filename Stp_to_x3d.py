# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 14:11:59 2020

@author: DELL
"""
from urllib import request

from OCC.Display.WebGl import x3dom_renderer
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepTools import breptools_Read
from OCC.Extend.DataExchange import read_step_file


from OCC.Display.SimpleGui import init_display
from OCC.Core.TopoDS import topods_Edge
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.OCCViewer import rgb_color
from OCC.Core.AIS import AIS_ColoredShape
from random import random
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.Quantity import Quantity_Color,Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
import os,time
import socket
import webbrowser
import errno
from flask import Flask, redirect, url_for, request,send_from_directory
from flask import Flask, render_template
from werkzeug.utils import secure_filename

num_click=0

def get_available_port(port):
    """ sometimes, the python webserver is closed but the
    port is not made available for a further call. So let's find
    any available port to prevent such issue. This function:
    * takes a port number (an integer), above 1024
    * check if it is available
    * if not, take another one
    * returns the port numer
    """
    if not port > 1024:
        raise AssertionError("port number should be > 1024")
    # check this port is available
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            print("\nPort %i is already in use. Picking another one." % port)
            # take another one
            s.bind(("", 0))
            port = s.getsockname()[1]
            print("Using port number %i" % port)
        else:
            print("Can't bind to port %i." % port)
    s.close()
    return port
def Exchange_stp_3xd(file="aaa.stp",path="."):
    pass
    file=file
    global num_click
    num_click+=1
    try:
        os.mkdir(str(num_click))
    except:
        pass
    the_shape = read_step_file(file)
    path=str(num_click)
    my_renderer = x3dom_renderer.X3DomRenderer(path=path)
    my_renderer.DisplayShape(the_shape,export_edges=True,color=(random(), random(), random()))
    my_renderer.run()
    os.path.join(path, "index.html")
    path="."+"\\"+ path +"\\"+"index.html"
    print(path)

    with open(path,"r") as f:
          html=f.read()
          f.close()
    return html



from flask import Flask

app = Flask(__name__, static_folder='', static_url_path='')
app.config['UPLOAD_FOLDER'] = 'upload/'



def getlist(path=''):
    try:
        print(path)
        path=path.replace("/","\\")
        all_file_list=os.listdir(path)
        file_modify_time_list=[]
        file_size_list=[]
        image_list=[]
        file_list=[]
        
        
        for file in all_file_list:
            if "x3d" in file:
                pass
                mtime = os.path.getmtime(path+"\\"+file) #输出文件最近修改时间
                file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                file_modify_time_list.append(file_modify_time)#文件修改时间列表
                file_size=os.path.getsize(path+"\\"+file)#输出文件的大小
                file_size_list.append(file_size)#文件大小列表
                file_list.append(file)
            if "jpg" in file:
                pass
                image_list.append(file)
       
    
        json = {
            'code':0,
             'msg':'返回指定类型列表',
             'data':{
                'path': file_list,  #存所有文件列表
                'size':file_size_list, #存所有文件尺寸
                'img':image_list,   #存所有文件缩图
                'date':file_modify_time_list   #存所有文件修改日期
                  }
           
        }
        
    except:
       json = {
        'code':100,
         'msg':'暂无数据',     
    }
      
    return json

def getfolder(path="."):
    pass
    dirs_list=[]
    dirs_dict={}
    path=path.replace("/","\\")
    for root,dirs,files in os.walk(path):
        if dirs==[]:
            continue
        dirs_list.append(dirs)
    
    dirs_dict={"folder":dirs_list[0]}
    return dirs_dict
    
    


 #访问根路径  传入3d文件名参数 查看3d
@app.route('/view3d')  
def index():
   fileNmae=request.args['file']
   #url_for('static', filename=fileNmae)
   return render_template("index.html",file='/static/3d/'+fileNmae)


#返回访问文件夹目录文件列表
@app.route('/getlist', methods = ['GET'])  
def Retun_file_name_1():
    return getlist(r"./static/3d/"+ request.args['path']);

#返回访问文件夹目录文件列表
@app.route('/getfolder')  
def Retun_file_name_2():
    print("123A")
    return getfolder(r"./static/3d/")
    
 

#返回个人空间目录文件列表
@app.route('/get_personal', methods = ['GET'])  
def get_personal():
    return  getlist(r"./static/personal/"+request.args['wx_id']);
    
    

 #访问上传html
@app.route('/upload')  
def upload_file():
   return render_template('upload.html')


 #效验微信小程序业务域名
@app.route('/z8Z79JHC9s.txt')
def today():
    return  app.send_static_file('z8Z79JHC9s.txt')


 #登录成功创建个人空间
@app.route('/personal_create', methods = ['GET'])
def personal_create():
    try:
    #这里还需判断存在 
        os.mkdir('./static/personal/'+ request.args['wx_id'])  #创建个人空间文件夹
       
        json = {
            'code':0,
             'msg':'创建个人空间成功！',
             'data':{
                  }
           
        }
        
    except:
       json = {
        'code':100,
         'msg':'暂无数据',     
    }
      
    return json

  
    
    
    return json



#接收上传文件
@app.route('/uploader', methods = ['GET', 'POST']) 
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
      print(f.filename)
      path=".\\upload"+"\\"+f.filename
      try:
          result=Exchange_stp_3xd(file=path)
          #return 'file uploaded successfully'
          return result
      except:
          pass
      
        
      
@app.route('/<path:path>')
def send_x3d_content(path):
    global num_click
    x3d_path="."+"\\"+str(num_click)
    return send_from_directory(x3d_path, path)



if __name__ == '__main__':

    app.run("0.0.0.0",8080,threaded=True)