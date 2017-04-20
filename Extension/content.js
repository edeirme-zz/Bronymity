var allowInjection = true;
if (window.frameElement != null && window.frameElement.sandbox != null) {
    allowInjection = false;
    for (var i = 0; i < window.frameElement.sandbox.length; i++) {
        var val = window.frameElement.sandbox[i];
        if (val == 'allow-scripts') {
            allowInjection = true;
        }
    }
}

function main(r, g, b, a, scriptId) {
    var scriptNode = document.getElementById(scriptId);
    function overrideCanvasProto(root) {
        function overrideCanvasInternal(name, old) {
            Object.defineProperty(root.prototype, name,
                {
                    value: function () {
                        var width = this.width;
                        var height = this.height;
                        var context = this.getContext("2d");
                        var imageData = context.getImageData(0, 0, width, height);
                        for (var i = 0; i < height; i++) {
                            for (var j = 0; j < width; j++) {
                                var index = ((i * (width * 4)) + (j * 4));
                                imageData.data[index + 0] = imageData.data[index + 0] + r;
                                imageData.data[index + 1] = imageData.data[index + 1] + g;
                                imageData.data[index + 2] = imageData.data[index + 2] + b;
                                imageData.data[index + 3] = imageData.data[index + 3] + a;
                            }
                        }
                        context.putImageData(imageData, 0, 0);
                        return old.apply(this, arguments);
                    }
                }
            );
        }
        //looks wrong

        // function overriderWebGLInternal(name, old) {
        //     Object.defineProperty(root.prototype, name,
        //         {
        //             value: function () {
        //                 //Initialize webgl
        //                 var context = this.getContext("webgl");
                        
        //                 return old.apply(this, arguments);
        //             }
        //         }
        //     );
        // }

        overrideCanvasInternal("toDataURL", root.prototype.toDataURL);
        overrideCanvasInternal("toBlob", root.prototype.toBlob);
        //overrideCanvasInternal("mozGetAsFile", root.prototype.mozGetAsFile);
        //looks wrongs
        // overriderWebGLInternal("UNMASKED_VENDOR_WEBGL", 
        //     root.prototype.getExtension("WEBGL_debug_renderer_info").UNMASKED_VENDOR_WEBGL);
        // overriderWebGLInternal("UNMASKED_RENDERER_WEBGL", 
        //     root.prototype.getExtension("WEBGL_debug_renderer_info").UNMASKED_RENDERER_WEBGL);
    }
    function overrideCanvaRendProto(root) {
        var getImageData = root.prototype.getImageData;
        Object.defineProperty(root.prototype, "getImageData",
            {
                value: function () {
                    var imageData = getImageData.apply(this, arguments);
                    var height = imageData.height;
                    var width = imageData.width;
                    //console.log("getImageData " + width + " " + height);
                    for (var i = 0; i < height; i++) {
                        for (var j = 0; j < width; j++) {
                            var index = ((i * (width * 4)) + (j * 4));
                            imageData.data[index + 0] = imageData.data[index + 0] + r;
                            imageData.data[index + 1] = imageData.data[index + 1] + g;
                            imageData.data[index + 2] = imageData.data[index + 2] + b;
                            imageData.data[index + 3] = imageData.data[index + 3] + a;
                        }
                    }
                    return imageData;
                }
            }
        );
    }
    function overrideWebGLRendProto(root) {
        // What should we override? getExtension?
        var unmasked_vendor_webgl = root.prototype.getExtension("WEBGL_debug_renderer_info").UNMASKED_VENDOR_WEBGL
        Object.defineProperty(root.prototype.getExtension("WEBGL_debug_renderer_info"), "UNMASKED_VENDOR_WEBGL",
            {
                value: function () {                    
                    return 37446;
                }
            }
        );
        var unmasked_renderer_webgl = root.prototype.getExtension("WEBGL_debug_renderer_info").UNMASKED_RENDERER_WEBGL
        Object.defineProperty(root.prototype.getExtension("WEBGL_debug_renderer_info"), "UNMASKED_RENDERER_WEBGL",
            {
                value: function () {                    
                    return 37445;
                }
            }
        );
    }
    function inject(element) {
        if (element.tagName.toUpperCase() === "IFRAME" && element.contentWindow) {
            try {
                var hasAccess = element.contentWindow.HTMLCanvasElement;
            } catch (e) {
                console.log("can't access " + e);
                return;
            }
            overrideCanvasProto(element.contentWindow.HTMLCanvasElement);
            overrideCanvaRendProto(element.contentWindow.CanvasRenderingContext2D);
            // let's try this one
            // overrideCanvaRendProto(element.contentWindow.WebGLRenderingContext);
            // overrideDocumentProto(element.contentWindow.Document);
        }
    }
    function overrideDocumentProto(root) {
        function doOverrideDocumentProto(old, name) {
            Object.defineProperty(root.prototype, name,
                {
                    value: function () {
                        var element = old.apply(this, arguments);
                        //console.log(name+ " everridden call"+element);
                        if (element == null) {
                            return null;
                        }
                        if (Object.prototype.toString.call(element) === '[object HTMLCollection]' ||
                            Object.prototype.toString.call(element) === '[object NodeList]') {
                            for (var i = 0; i < element.length; ++i) {
                                var el = element[i];
                                //console.log("elements list inject " + name);
                                inject(el);
                            }
                        } else {
                            //console.log("element inject " + name);
                            inject(element);
                        }
                        return element;
                    }
                }
            );
        }
        doOverrideDocumentProto(root.prototype.createElement, "createElement");
        doOverrideDocumentProto(root.prototype.createElementNS, "createElementNS");
        doOverrideDocumentProto(root.prototype.getElementById, "getElementById");
        doOverrideDocumentProto(root.prototype.getElementsByName, "getElementsByName");
        doOverrideDocumentProto(root.prototype.getElementsByClassName, "getElementsByClassName");
        doOverrideDocumentProto(root.prototype.getElementsByTagName, "getElementsByTagName");
        doOverrideDocumentProto(root.prototype.getElementsByTagNameNS, "getElementsByTagNameNS");
    }

    overrideCanvasProto(HTMLCanvasElement);
    overrideCanvaRendProto(CanvasRenderingContext2D);
    overrideCanvaRendProto(WebGLRenderingContext);
    overrideDocumentProto(Document);
    scriptNode.parentNode.removeChild(scriptNode);
}
var script = document.createElement('script');
script.id = getRandomString();
script.type = "text/javascript";
if (allowInjection) {
    var newChild = document.createTextNode('try{(' + main + ')(' + r + ',' + g + ',' + b + ',' + a + ',"' + script.id + '");} catch (e) {console.error(e);}');
    script.appendChild(newChild);
    var node = (document.documentElement || document.head || document.body);
    if (typeof node[docId] === 'undefined') {
        node.insertBefore(script, node.firstChild);
        node[docId] = getRandomString();
    }
}
function getRandomString() {
    var text = "";
    var charset = "abcdefghijklmnopqrstuvwxyz";
    for (var i = 0; i < 5; i++)
        text += charset.charAt(Math.floor(Math.random() * charset.length));
    return text;
}