import json
from webbrowser import get
from flask import Flask, render_template, request,flash,redirect,url_for,Response
import random
from werkzeug.utils import secure_filename
import os
import shutil
from pathlib import Path
# from flask import request

#UPLOAD_FOLDER = '/home/arnaualbert/Desktop/uiflask/uploads'
#ALLOWED_EXTENSIONS = {'*fasta.*','fastaq.gz','gz','fq.gz','*fq.*'}
module_name = __name__
app = Flask(__name__)
#root_path : Path = Path(app.root_path) 
#app.secret_key = "secret key"
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Get current path
path = os.getcwd()
# file Upload
DEMULTIPLEXING_FOLDER = os.path.join(path, 'demultiplexing')
FWD_FOLDER = os.path.join(path, 'demultiplexing/fwd')
RV_FOLDER = os.path.join(path, 'demultiplexing/rv')

#app.config['DEST_FOLDER'] = '/home/arnaualbert/Desktop/uiflask/uploads' #### last try
# if not os.path.isdir(UPLOAD_FOLDER):
#     os.mkdir(UPLOAD_FOLDER)

if not os.path.isdir(DEMULTIPLEXING_FOLDER):
    os.mkdir(DEMULTIPLEXING_FOLDER)

if not os.path.isdir(FWD_FOLDER):
    os.mkdir(FWD_FOLDER)

if not os.path.isdir(RV_FOLDER):
    os.mkdir(RV_FOLDER)

app.config['DEMULTIPLEXING_FOLDER'] = DEMULTIPLEXING_FOLDER
app.config['DEMULTIPLEXING_FWD_FOLDER'] = FWD_FOLDER
app.config['DEMULTIPLEXING_RV_FOLDER'] = RV_FOLDER

ALLOWED_EXTENSIONS = set(['*fasta.*','fastaq.gz','gz','fq.gz','*fq.*'])

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['UPLOAD_FOLDER'] = '/home/arnaualbert/Desktop/uiflask/uploads'
# app.config['ALLOWED_EXTENSIONS'] = set(['*fasta.*','fastaq.gz','gz','fq.gz','*fq.*'])

@app.route("/")
def index():
    return render_template('index.html')


# @app.route('/demultiplexing')
# def demuliplexing():
#     return render_template('demultiplexing.html')

#############################################################################################################################
################################################## DEMULTIPLEXING WORKS #####################################################
#############################################################################################################################

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/demultiplexing',methods=['GET', 'POST'])
def demultiplexing():
    ''' Demultiplexing 
        This function is used to demultiplex the fastq files.
        It takes all the parameters from the html form.
    '''
    # if request.method == 'GET':
    #     return render_template('demultiplexing.html')
    if request.method == 'POST':
        fastas_fwd = request.files.getlist("fastas_fwd")
        fastas_fwd_ls = []
        for f in fastas_fwd:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                # f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                f.save(os.path.join(app.config['DEMULTIPLEXING_FWD_FOLDER'], filename))
                # fastas_fwd_ls.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                fastas_fwd_ls.append(os.path.join(app.config['DEMULTIPLEXING_FWD_FOLDER'],filename))
        fastas_rv = request.files.getlist("fastas_rv")
        fastas_rv_ls = []
        for f in fastas_rv:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                # f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                f.save(os.path.join(app.config['DEMULTIPLEXING_RV_FOLDER'], filename))
                # fastas_rv_ls.append(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                fastas_rv_ls.append(os.path.join(app.config['DEMULTIPLEXING_RV_FOLDER'],filename))
        output_dir = request.form['output_dir']
        ref_genome = request.form['ref_genome']
        organism_name = request.form['organism_name']
        num_of_threads = request.form['num_of_threads']
        reads_per_chunk = request.form['reads_per_chunk']
        #replace = request.form['replace']
        skip_removing_tmp_files = request.form['skip_removing_tmp_files']
        wit_db = request.form['wit_db']
        params = {"fastas_fwd":fastas_fwd_ls,"fastas_rv":fastas_rv_ls,"output_dir":output_dir,"ref_genome":ref_genome,"organism_name":organism_name,"num_of_threads":num_of_threads,"reads_per_chunk":reads_per_chunk,"skip_removing_tmp_files":skip_removing_tmp_files,"wit_db":wit_db}
        print(params)
        #print(f'fastas_fwd: {fastas_fwd_ls}, fastas_rv: {fastas_rv_ls}, output_dir: {output_dir}, ref_genome: {ref_genome}, organism_name: {organism_name},num_of_threads: {num_of_threads}, reads_per_chunk: {reads_per_chunk}, replace: {replace},skip_removing_tmp_files: {skip_removing_tmp_files}, wit_db: {wit_db}')
        return redirect(url_for('demultiplexing'))
    return render_template('demultiplexing.html')

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

@app.route('/crossmaper')
def crossmaper():
    return render_template('crossmaper.html')

# @app.route('/crossmaper/dna')
# def crossmaperdna():
#     return render_template('crossmaperdna.html')
@app.route('/crossmaper/dna',methods=['GET','POST'])
def crossmaperdna():
    if request.method == 'GET':
        return render_template('crossmaperdna.html')
    if request.method == 'POST':
        output = request.get_json()
        result = json.dumps(output)
        result = json.loads(result)
        for res in result:
            print(res)
        # print(len(result))
        return redirect(url_for('crossmaperdna'))

# @app.route('/test',methods=['POST'])
# def test():
#     output = request.get_json()
#     result = json.dumps(output)
#     result = json.loads(result)
#     # print(result)
#     return result

@app.route('/crossmaper/rna')
def crossmaperrna():
    return render_template('crossmaperna.html')

##############################################################################################################
###############################################FUNCIONA#######################################################


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/pueba', methods=['GET', 'POST'])
# def upload_folder():
#     if request.method == 'POST':
#         folder = request.files.getlist("folder")
#         print(folder)
#         for f in folder:
#             if f and allowed_file(f.filename):
#                 filename = secure_filename(f.filename)
#                 f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return redirect(url_for('upload_folder'))
#     return '''
#     <!DOCTYPE html>
#     <html>
#       <head>
#         <title>Upload Folder</title>
#       </head>
#       <body>
#         <form action="/pueba" method="post" enctype="multipart/form-data">
#           <input type="file" name="folder" id="folder" directory="" webkitdirectory="" mozdirectory="" msdirectory="" odirectory="" />
#           <input type="submit" value="Upload Folder">
#         </form>
#       </body>
#     </html>
#     '''


##############################################################################################################
##############################################################################################################


############################################TEST FUNCIONA#####################################################
##############################################################################################################

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/pueba', methods=['GET', 'POST'])
# def upload_folder():
#     if request.method == 'POST':
#         folder = request.files.getlist("folder")
#         print(folder)
#         for f in folder:
#             print(f)
#             if f and allowed_file(f.filename):
#                 filename = secure_filename(f.filename)
#                 f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return redirect(url_for('upload_folder'))
#     return '''
#     <!DOCTYPE html>
#     <html>
#       <head>
#         <title>Upload Folder</title>
#       </head>
#       <body>
#         <form action="/pueba" method="post" enctype="multipart/form-data">
#           <input type="file" name="folder" id="folder" directory="" webkitdirectory="" mozdirectory="" msdirectory="" odirectory="" />
#           <input type="submit" value="Upload Folder">
#         </form>
#       </body>
#     </html>
#     '''

##############################################################################################################
##############################################################################################################


# def allowed_file(filename):
#     return True


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'GET':
#         return render_template('upload.html')
#     if request.method == 'POST':
#         files: str = request.form['fasta']
#         return f'you are uploading {files}'
#     return ''



# @app.route('/upload')
# def upload_file():
#     path = request.args.get('1','')
#     data = {'path':path}
#     print(search_files(path,'*fasta.*'))
#     # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     return render_template('upload.html',data=data)

# @app.route('/uploads')
# def upload_form():
#     return render_template('upload.html')

# @app.route('/uploads', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':

#         if 'files[]' not in request.files:
#             flash('No file part')
#             return redirect(request.url)

#         files = request.files.getlist('files[]')

#         for file in files:
#             if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#         flash('File(s) successfully uploaded')
#         return redirect('/uploads')

# @app.route("/send-data", methods=["POST"])
# def receive_data():
#     data = request.get_json()
#     print(data)
#     return json.dumps({ "message": "Data received successfully" })
# @app.route('/u')
# def main():
# 	return render_template("upload.html")


# @app.route('/upload', methods=['POST'])
# def upload():
# 	if request.method == 'POST':

# 		# Get the list of files from webpage
# 		files = request.files.getlist("file")

# 		# Iterate for each file in the files List, and Save them
# 		for file in files:
# 			file.save(file.filename)
# 		return "<h1>Files Uploaded Successfully.!</h1>"




# @app.route('/upload')
# def upload_file():
#    return render_template('upload.html')

# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file1():
#    if request.method == 'POST':
#       files = request.files.getlist("file")
#       for file in files:
#           file.save(secure_filename(file.filename))
#       return 'file uploaded successfully'


# @app.route('/copy_folder/<src>/<dest>')
# def copy_folder(src, dest):
#     src_path = os.path.abspath(src)
#     dest_path = os.path.abspath(dest)
#     try:
#         shutil.copytree(src_path, dest_path)
#         return "Folder copied successfully"
#     except Exception as e:
#         return "Error copying folder: " + str(e)


# @app.route('/batchmode')
# def batchmode():
#     return '''
#     <!doctype html>
#     <title>Upload a folder</title>
#     <h1>Upload a folder</h1>
#     <form action="upload_folder" method=post enctype=multipart/form-data>
#       <p><input type=file name=folder multiple>
#          <input type=submit value=Upload>
#     </form>
#     '''

# @app.route('/upload_folder', methods=['POST'])
# def upload_folder():
#     folder = request.files['folder']
#     if folder:
#         for file in folder:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return redirect(url_for('index'))
#     else:
#         return 'No folder was uploaded'


# @app.route('/batchmode', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file >
#       <input type=submit value=Upload>
#     </form>
#     '''


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def search_files(root_dir, extension):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(extension):
                print(os.path.join(root, file))


if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = '/home/arnaualbert/Desktop/uiflask/uploads'
    app.run(debug=True)
    #app.run(debug=True, port=5000)
    # app.run(host="127.0.0.1", port=8080, debug=True)