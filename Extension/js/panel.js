document.addEventListener('DOMContentLoaded', function () {
    var uploadProfile = document.getElementById('upload_profile');
    uploadProfile.addEventListener('click', function () {
        chrome.runtime.sendMessage({action: "upload-profile"});
        window.close();
    });
});