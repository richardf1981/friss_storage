(function () {
    let fileUploaderReplace = document.getElementById('file-upload-replace');
    let fileInputUploaderReplace = document.getElementById('file-input-replace');
    let fileUploader = document.getElementById('file-uploader');
    let fileInputUploader = document.getElementById('file-input');
    let fileListDisplay = document.getElementById('file-list-display');
    let fileListDisplayRender =  document.getElementById("file-list-display-replace");
    let fileDownload = document.getElementById("file-downloader");
    let fileDownloadInput = document.getElementById("file-input-download");
    let fileListDisplayAll = document.getElementById("file-list-all");
    let btUploadSubmit = document.getElementById("file-submit-upload");
    let btUploadSubmitReplace = document.getElementById("file-submit-upload-replace");
    let fileList = [];

    fileDownload.addEventListener('submit', function (evnt) {
        evnt.preventDefault();
        let originalText = evnt.submitter.textContent;

        evnt.preventDefault();
        evnt.submitter.disabled = true;
        evnt.submitter.textContent = "Processing";

        // file...
        let file_name = fileDownloadInput.value;

        receiveFile(file_name, evnt.submitter, originalText);
    });

    fileUploaderReplace.addEventListener('submit', function (evnt) {
        uploadFunction(evnt, true);
    });

    fileUploader.addEventListener('submit', function (evnt) {
        uploadFunction(evnt, false);
    });

    fileInputUploader.addEventListener('change', function (evnt) {
        fileList = [];
        btUploadSubmit.disabled = true;

        for (let i = 0; i < fileInputUploader.files.length; i++) {
            fileList.push(fileInputUploader.files[i]);
            btUploadSubmit.disabled = false;
        }
        renderFileList(fileListDisplay);
    });

    fileInputUploaderReplace.addEventListener("change", function (evnt){
        fileList = [];
        btUploadSubmitReplace.disabled = true;

        for (let i = 0; i < fileInputUploaderReplace.files.length; i++) {
            btUploadSubmitReplace.disabled = false;
            fileList.push(fileInputUploaderReplace.files[i]);
        }
        renderFileList(fileListDisplayRender);
    });

     window.addEventListener("load", function() {
        // your code here
        listFiles();
    }, false);

    let renderFileList = function (objRender) {
        objRender.innerHTML = '';
        fileList.forEach(function (file, index) {
            let fileDisplayEl = document.createElement('p');
            fileDisplayEl.innerHTML = file.name;
            objRender.appendChild(fileDisplayEl);
        });
    };

    let renderFileListFiles = function (objRender, list) {
        objRender.innerHTML = '';
        list.forEach(function (file, index) {
            let fileDisplayEl = document.createElement('p');
            fileDisplayEl.innerHTML = "<a href='#'>" + file.file_name + "</a>";
            objRender.appendChild(fileDisplayEl);

            fileDisplayEl.addEventListener("click", function(e) {
                e.preventDefault();
                fileDownloadInput.value = e.target.innerHTML;
            });
        });
    };

    let uploadFunction = function (evnt, replace){
        let originalText = evnt.submitter.textContent;

        evnt.preventDefault();
        evnt.submitter.disabled = true;
        evnt.submitter.textContent = "Processing";

        fileList.forEach(function (file) {
            sendFile(file, evnt.submitter, originalText, replace);
        });
    };

    let getToken = function (request){
        return new Promise(resolve => {
            setTimeout(() => {
                let request_token = new XMLHttpRequest();
                let params = {};

                request_token.open("POST", '/login');
                request_token.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
                request_token.send('&username=' + USER_NAME + '&password=' + PASSWORD);
                request_token.onreadystatechange=function() {
                    if (request_token.readyState === XMLHttpRequest.DONE) {
                        if (request_token.status === 0 || (request_token.status >= 200 && request_token.status < 400)) {
                            let json_resp = JSON.parse(request_token.responseText);
                            resolve(json_resp.access_token);
                        } else {
                            // Oh no! There has been an error with the request!
                            let json_resp = JSON.parse(request_token.responseText);
                            alert("Sorry, we're unable to process your request! Reason: " + json_resp.detail);
                        }
                    }
                }
            }, 2000);
        });
    };

    let handleError = function (response){
        // Oh no! There has been an error with the request!
        try {
            let json_resp = JSON.parse(response.responseText);
            alert("Sorry, we're unable to process your request! Reason: " + json_resp.detail);
        }catch (e){
            alert("Sorry, we're unable to process your request!");
        }
    }

    let listFiles = async function () {
        let request = new XMLHttpRequest();
        // let full_url = location.protocol + '//' +
        //    location.hostname+(location.port ? ':'+location.port: '') + "/api/v1/filelist";
        let full_url = "/api/v1/filelist";

        request.open("GET", full_url);
        const token = await getToken();
        request.setRequestHeader('Authorization', 'Bearer ' + token);
        request.responseType = "json";
        request.send();

        // check state...
        request.onreadystatechange = function () {
            if (request.readyState === XMLHttpRequest.DONE) {
                if (request.status === 0 || (request.status >= 200 && request.status < 400)) {
                    renderFileListFiles(fileListDisplayAll, request.response);
                } else {
                    // handleError(request);
                    console.log("Unable to load list file");
                }
            }
        }
    };

    let receiveFile = async function (name_file, bt, originalText){
        let request = new XMLHttpRequest();

        request.open("GET", '/api/v1/file_download/'+name_file);
        const token = await getToken();
        request.setRequestHeader('Authorization', 'Bearer ' + token);
        request.responseType = 'arraybuffer';
        request.send();

        // check state...
        request.onreadystatechange=function() {
            if(request.readyState === XMLHttpRequest.DONE) {
                if (request.status === 0 || (request.status >= 200 && request.status < 400)) {
                    let contentType = request.getResponseHeader("content-type");
                    let disposition = request.getResponseHeader("content-disposition");
                    let index1 = 0;
                    let index2 = 0;
                    let file_name;

                    index1 = disposition.indexOf("filename");
                    file_name = disposition.substring(index1);
                    index2 = file_name.indexOf('"');
                    file_name = file_name.substring(index2);
                    file_name = file_name.replaceAll('"', "");

                    // The request has been completed successfully
                    // Create a binary string from the returned data, then encode it as a data URL.
                    let blob = new Blob([this.response], {type: contentType});
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    // the filename you want
                    a.download = file_name;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                }else if (request.status === 404){
                    let resp_temp = {}
                    resp_temp.responseText = '{"detail": "' + request.statusText + '"}';
                    handleError(resp_temp);
                } else {
                    handleError(request);
                }
                if (bt && originalText){
                    bt.textContent = originalText.trim();
                    bt.disabled = false;
                }
            }
        }
    };

    let sendFile = async function (file, bt, originalText, replace) {
        let formData = new FormData();
        let request = new XMLHttpRequest();

        formData.set('file', file);
        let method = ""

        if (!replace) {
            method= "POST";
        }else{
            method = "PUT";
        }

        request.open(method, '/api/v1/file_upload');
        const token = await getToken();
        request.setRequestHeader('Authorization', 'Bearer ' + token);
        request.send(formData);

        // check state...
        request.onreadystatechange=function() {
            if(request.readyState === XMLHttpRequest.DONE) {
                console.log(request.responseText);
                if (request.status === 0 || (request.status >= 200 && request.status < 400)) {
                    // The request has been completed successfully
                    alert("Congratulations! Your file has been updated successfully!");
                    listFiles();
                } else {
                    handleError(request);
                }
                if (bt && originalText){
                    bt.textContent = originalText.trim();
                    bt.disabled = false;
                }
            }
        }
    };
})();