(function () {
    let fileUploaderReplace = document.getElementById('file-upload-replace');
    let fileInputUploaderReplace = document.getElementById('file-input-replace');
    let fileUploader = document.getElementById('file-uploader');
    let fileInputUploader = document.getElementById('file-input');
    let fileListDisplay = document.getElementById('file-list-display');
    let fileListDisplayRender =  document.getElementById("file-list-display-replace");
    let fileDownload = document.getElementById("file-downloader");
    let fileDownloadInput = document.getElementById("file-input-download");
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

    uploadFunction = function (evnt, replace){
        let originalText = evnt.submitter.textContent;

        evnt.preventDefault();
        evnt.submitter.disabled = true;
        evnt.submitter.textContent = "Processing";

        fileList.forEach(function (file) {
            sendFile(file, evnt.submitter, originalText, replace);
        });
    }

    fileUploaderReplace.addEventListener('submit', function (evnt) {
        uploadFunction(evnt, true);
    });

    fileUploader.addEventListener('submit', function (evnt) {
        uploadFunction(evnt, false);
    });

    fileInputUploader.addEventListener('change', function (evnt) {
        fileList = [];
        for (let i = 0; i < fileInputUploader.files.length; i++) {
            fileList.push(fileInputUploader.files[i]);
        }
        renderFileList(fileListDisplay);
    });

    fileInputUploaderReplace.addEventListener("change", function (evnt){
        fileList = [];
        for (let i = 0; i < fileInputUploaderReplace.files.length; i++) {
            fileList.push(fileInputUploaderReplace.files[i]);
        }
        renderFileList(fileListDisplayRender);
    });

    renderFileList = function (objRender) {
        objRender.innerHTML = '';
        fileList.forEach(function (file, index) {
            let fileDisplayEl = document.createElement('p');
            // fileDisplayEl.innerHTML = (index + 1) + ': ' + file.name;
            fileDisplayEl.innerHTML = file.name;
            objRender.appendChild(fileDisplayEl);
        });
    };

    setToken = function (request){
        let token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiM2IyMGE0ZjktNzAwNy00YzM4LTk0ZTMtNzE2ZTVkNGZjNjY5IiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNjE5MjM4MzQ2fQ.EKp-WMmcX21vIciIqnt5WMk-fSO5d9eoa86U2Mp28K0"
        request.setRequestHeader("Authorization", "Bearer " + token);


    };

    receiveFile = function (name_file, bt, originalText){
        let request = new XMLHttpRequest();

        request.open("GET", '/api/v1/file_download?file_name='+name_file);
        setToken(request);
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
                } else {
                    // Oh no! There has been an error with the request!
                    let json_resp = JSON.parse(request.responseText);
                    alert("Sorry, we're unable to process your request! Reason: " + json_resp.detail);
                }
                if (bt && originalText){
                    bt.textContent = originalText.trim();
                    bt.disabled = false;
                }
            }
        }
    };

    sendFile = function (file, bt, originalText, replace) {
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
        setToken(request);
        request.send(formData);

        // check state...
        request.onreadystatechange=function() {
            if(request.readyState === XMLHttpRequest.DONE) {
                console.log(request.responseText);
                if (request.status === 0 || (request.status >= 200 && request.status < 400)) {
                    // The request has been completed successfully
                    alert("Congratulations! Your file has been updated successfully!");
                } else {
                    // Oh no! There has been an error with the request!
                    let json_resp = JSON.parse(request.responseText);
                    alert("Sorry, we're unable to process your request! Reason: " + json_resp.detail);
                }
                if (bt && originalText){
                    bt.textContent = originalText.trim();
                    bt.disabled = false;
                }
            }
        }
    };
})();