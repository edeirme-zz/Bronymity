document.addEventListener('DOMContentLoaded', function () {
    var uploadProfile = document.getElementById('upload_profile');
    var reinitializeProfile = document.getElementById('reinitialize_profile');
    uploadProfile.addEventListener('click', function () {
        chrome.runtime.sendMessage({action: "upload-profile"});
        window.close();
    });
    reinitializeProfile.addEventListener('click', function () {
        chrome.runtime.sendMessage({action: "reinitialize-profile"});
        window.close();
    });
});