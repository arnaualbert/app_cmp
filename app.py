import json
from webbrowser import get
from flask import Flask, render_template, request,flash,redirect,url_for,Response
import random
from werkzeug.utils import secure_filename
import os
import shutil
from pathlib import Path
# from flask import request

module_name = __name__
app = Flask(__name__)

# Get current path
path = os.getcwd()
# file Upload
DEMULTIPLEXING_FOLDER = os.path.join(path, 'demultiplexing')
FWD_FOLDER = os.path.join(path, 'demultiplexing/fwd')
RV_FOLDER = os.path.join(path, 'demultiplexing/rv')

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


@app.route("/")
def index():
    return render_template('index.html')


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
                f.save(os.path.join(app.config['DEMULTIPLEXING_FWD_FOLDER'], filename))
                fastas_fwd_ls.append(os.path.join(app.config['DEMULTIPLEXING_FWD_FOLDER'],filename))
        fastas_rv = request.files.getlist("fastas_rv")
        fastas_rv_ls = []
        for f in fastas_rv:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['DEMULTIPLEXING_RV_FOLDER'], filename))
                fastas_rv_ls.append(os.path.join(app.config['DEMULTIPLEXING_RV_FOLDER'],filename))
        output_dir = request.form['output_dir']
        ref_genome = request.form['ref_genome']
        organism_name = request.form['organism_name']
        num_of_threads = request.form['num_of_threads']
        reads_per_chunk = request.form['reads_per_chunk']
        #replace = request.form['replace']
        skip_removing_tmp_files = request.form['skip_removing_tmp_files']
        wit_db = request.form['wit_db']
        # params = {"fastas_fwd":fastas_fwd_ls,"fastas_rv":fastas_rv_ls,"output_dir":output_dir,"ref_genome":ref_genome,"organism_name":organism_name,"num_of_threads":num_of_threads,"reads_per_chunk":reads_per_chunk,"skip_removing_tmp_files":skip_removing_tmp_files,"wit_db":wit_db}
        params = {"--fastq1":fastas_fwd_ls,"--fastq2":fastas_rv_ls,"--outdir":output_dir,"--refGenomes":ref_genome,"--sampleNames":organism_name,"--trheads":num_of_threads,"--nreads_per_chunk":reads_per_chunk,"--skip_removing_tmp_files":skip_removing_tmp_files,"--wit_db":wit_db}
        print(params)
        print(type(params))
        #for rout in fastas_fwd_ls:
        fastas_fs_ls_string = " ".join(fastas_fwd_ls)
        fastas_rv_ls_string = " ".join(fastas_rv_ls)
        command = f' --fastq1 {fastas_fs_ls_string} --fastq2 {fastas_rv_ls_string} --outdir {output_dir} --refGenomes {ref_genome} --sampleNames {organism_name} --trheads {num_of_threads} --nreads_per_chunk {reads_per_chunk} --skip_removing_tmp_files {skip_removing_tmp_files} --wit_db {wit_db}'
        print(command)
        print(type(command))
        #print(f'fastas_fwd: {fastas_fwd_ls}, fastas_rv: {fastas_rv_ls}, output_dir: {output_dir}, ref_genome: {ref_genome}, organism_name: {organism_name},num_of_threads: {num_of_threads}, reads_per_chunk: {reads_per_chunk}, replace: {replace},skip_removing_tmp_files: {skip_removing_tmp_files}, wit_db: {wit_db}')
        return redirect(url_for('demultiplexing'))
    return render_template('demultiplexing.html')

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

@app.route('/crossmaper')
def crossmaper():
    return render_template('crossmaper.html')

@app.route('/crossmaper/dna',methods=['GET','POST'])
def crossmaperdna():
    if request.method == 'GET':
        return render_template('crossmaperdna.html')
    if request.method == 'POST':
        output = request.get_json()
        # print(output)
        for i in output:
            # print(type(i))
            # print(i)
            i = json.loads(i)
            # print(type(i))
            numofreads = i['numberOfReads']
            print(f'number of reads: {numofreads}')
        # print(type(output))
        # for result in output:
        #     result = json.dumps(output)
        #     print(result)
        #     print(type(result))
        # result = json.dumps(output)
        # result = json.loads(result)
        # print(result)
        # print(len(result))
        # print(type(result[0]))
        # print(result['numberOfReads'])
        # for res in result:
        #     print(res)
            #print(res['numberOfReads'])
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


def search_files(root_dir, extension):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(extension):
                print(os.path.join(root, file))


if __name__ == "__main__":
    #app.config['UPLOAD_FOLDER'] = '/home/arnaualbert/Desktop/uiflask/uploads'
    app.run(debug=True)
    #app.run(debug=True, port=5000)
    # app.run(host="127.0.0.1", port=8080, debug=True)