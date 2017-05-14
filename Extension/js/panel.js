document.addEventListener('DOMContentLoaded', function () {
    var uploadProfile = document.getElementById('upload_profile');
    var reinitializeProfile = document.getElementById('reinitialize_profile');
    var startTests = document.getElementById('start_tests');
    uploadProfile.addEventListener('click', function () {
        chrome.runtime.sendMessage({action: "upload-profile"});
        window.close();
    });
    reinitializeProfile.addEventListener('click', function () {
        chrome.runtime.sendMessage({action: "reinitialize-profile"});
        window.close();
    });
    startTests.addEventListener('click', function () {
        chrome.runtime.sendMessage({action: "start-tests"});
        window.close();
    });
});