document.addEventListener('DOMContentLoaded', function () {


    var status = localStorage['status'];
    if (status == undefined  || status === "deactivated") {
        radiobtn = document.getElementById("deactivated");
        radiobtn.checked = true;
    } else if (status === "activated"){
        radiobtn = document.getElementById("activated");
        radiobtn.checked = true;
    }
    
    var uploadProfile = document.getElementById('upload_profile');
    var reinitializeProfile = document.getElementById('reinitialize_profile');
    var startTests = document.getElementById('start_tests');
    var startBrowserprint = document.getElementById('start_browserprint');
    var submitBrowserprint = document.getElementById('submit_browserprint');
    var enablePlugin = document.getElementById('activated');
    var disablePlugin = document.getElementById('deactivated');
    var uploadTestResults = document.getElementById('upload_test_results');


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
    startBrowserprint.addEventListener('click', function () {
        chrome.runtime.sendMessage({action: "start-browserprint"});
        window.close();
    });
    submitBrowserprint.addEventListener('submit', function (e) {
        e.preventDefault();
        chrome.runtime.sendMessage({action: "submit-browserprint", source: document.getElementById('fname').value});
        window.close();         
    });
    enablePlugin.addEventListener('click', function (e) {
        chrome.runtime.sendMessage({action: "enable-plugin"});
        window.close();         
    });
    disablePlugin.addEventListener('click', function (e) {
        chrome.runtime.sendMessage({action: "disable-plugin"});
        window.close();         
    });
    uploadTestResults.addEventListener('click', function (e) {
        chrome.runtime.sendMessage({action: "upload-test-results"});
        window.close();         
    });
});