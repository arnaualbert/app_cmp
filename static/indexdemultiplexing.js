document.addEventListener("DOMContentLoaded", function () {

    // select all the optional arguments
    var optionalArguments = document.querySelectorAll('#optional_arguments');
    // loop the array of all the optional arguments and hide them
    for (var i = 0; i < optionalArguments.length; i++) {
        var options = optionalArguments[i];
        options.style.display = "none";
    }

})

// when the button is clicked hide all the optional arguments if they are present or show all the optional arguments if they are not shown
function showHide() {
    var optionalArguments = document.querySelectorAll('#optional_arguments');
    for (var i = 0; i < optionalArguments.length; i++) {
        var options = optionalArguments[i];

        if (options.style.display === "none") {
            options.style.display = "block";
        } else {
            options.style.display = "none";
        }
    }
}

// clone the first form and add it to the div
function addForm() {
    var original = document.getElementById("form_demultiplex");
    var new_form = original.cloneNode(true);

    var where_form = document.getElementById("forms");
    where_form.appendChild(new_form);
}

// only fasta,gz files are allowed
var _validFileExtensions = ["fastq.gz"];    
function Validate(oForm) {
    var arrInputs = oForm.getElementsByTagName("input");
    for (var i = 0; i < arrInputs.length; i++) {
        var oInput = arrInputs[i];
        if (oInput.type == "file") {
            var sFileName = oInput.value;
            if (sFileName.length > 0) {
                var blnValid = false;
                for (var j = 0; j < _validFileExtensions.length; j++) {
                    var sCurExtension = _validFileExtensions[j];
                    if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                        blnValid = true;
                        break;
                    }
                }
                
                if (!blnValid) {
                    alert("Sorry, " + sFileName + " is invalid, allowed extensions are: " + _validFileExtensions.join(", "));
                    return false;
                }
            }
        }
    }
  
    return true;
}

function addFormReferenceOrganism() {
    var original = document.getElementById("reference_organism");
    var new_form = original.cloneNode(true);
    var where_form = document.getElementById("references_organisms");
    where_form.appendChild(new_form);
}
/////////////////// works
function batchmode() {
    var fasta0 = document.getElementById("fasta0");
    var fasta1 = document.getElementById("fasta1");
    var isactivated = document.getElementById("isactivated");
    if(fasta0.hasAttribute("directory")&&fasta1.hasAttribute("directory")){
    fasta0.removeAttribute("directory");
    fasta0.removeAttribute("webkitdirectory");
    fasta0.removeAttribute("mozdirectory");
    fasta0.removeAttribute("msdirectory");
    fasta0.removeAttribute("odirectory");
    fasta1.removeAttribute("directory");
    fasta1.removeAttribute("webkitdirectory");
    fasta1.removeAttribute("mozdirectory");
    fasta1.removeAttribute("msdirectory");
    fasta1.removeAttribute("odirectory");
    isactivated.innerHTML = 'Batch mode deactivated'    
  }else{
    fasta0.setAttribute("directory", "");
    fasta0.setAttribute("webkitdirectory", "");
    fasta0.setAttribute("mozdirectory", "");
    fasta0.setAttribute("msdirectory", "");
    fasta0.setAttribute("odirectory", "");
    fasta1.setAttribute("directory", "");
    fasta1.setAttribute("webkitdirectory", "");
    fasta1.setAttribute("mozdirectory", "");
    fasta1.setAttribute("msdirectory", "");
    fasta1.setAttribute("odirectory", "");
    isactivated.innerHTML = 'Batch mode activated'
  }

}




// get all the parameters and create the Demultiplex object , then add it to the array
function sendDemultiplexing() {
    var objects = [];

    var total_forms = document.querySelectorAll("#form_demultiplex");
    var fasta0 = document.querySelectorAll("#fasta0");
    var fasta1 = document.querySelectorAll("#fasta1");
    var output_dir = document.querySelectorAll("#output_dir");
    var refGenomes = document.querySelectorAll("#ref_genome");
    var organismName = document.querySelectorAll("#organism_name");
    var numberofthreads = document.querySelectorAll("#num_of_threads");
    var readsperchunk = document.querySelectorAll("#reads_per_chunk");
    var replacements = document.querySelectorAll("#replace");
    var skipRemovingTmpFilesFrom = document.querySelectorAll("#skip_removing_tmp_files");
    var witDB = document.querySelectorAll("#wit_db");
    var total_obj = total_forms.length;
    var organismNamearray = [];
    var referencesgenomesarray = [];
    for(let i = 0;i<refGenomes.length;i++){
        referencesgenomesarray.push(refGenomes[i].value);
    }
    for(let i = 0;i < organismName.length;i++){
        organismNamearray.push(organismName[i].value);    
    }


    for (let i = 0; i < total_obj; i++) {
        var demultiplex_params = new Demultiplex(fasta0[i].value, fasta1[i].value, output_dir[i].value, referencesgenomesarray, organismNamearray, numberofthreads[i].value, readsperchunk[i].value, replacements[i].value, skipRemovingTmpFilesFrom[i].value, witDB[i].value)
        objects.push(demultiplex_params);
            
    }
    console.log(objects);


}