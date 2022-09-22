"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, isFileId, isLocalFile
from rockeet.File import read



def showImage(fileId):
    displayImageHtml(getImageFromRessource(fileId))


def showFaces(fileId, faces: Response, title: str = "Face Detection", scale: float = 1):
    img, w, h = getImageFromRessource(fileId, scale)

    displayImageHtml(img, title, w, h, faces.result)


def showIdentifiedFaces(fileId, identification: Response, title: str = "Faces Identified", scale: float = 1):
    img, w, h = getImageFromRessource(fileId, scale)

    def addLabelKey(x):
        x["label"] = "".join(map(lambda y: f"<p style='margin:0'>Name: {y['name']} ({y['range'][0]*100:.0f}-{y['range'][1]*100:.0f}%)</p>", x["similarities"]))
        return x

    displayImageHtml(img, title, w, h, map(addLabelKey, list(identification)))


def displayImageHtml(image, title, width, height, boxes: list = []):
    labelStyle = '"position:absolute;top:2px;left:2px;background:#000;color:#fff;font-family:Trebuchet MS;font-size:12px;margin:0;padding:3px 7px;"'
    content = f"""
        <html>
            <head>
                <style>
                </style>
            </head>
            <body style="margin:0">
                <div id="scale-container" style="transform-origin: top left; transform:scale(1)">
                    <img src="data:image/jpeg;base64,{image}" />
                    {
                        "".join(
                            list(
                                map(
                                    lambda x: f"<div style='border:2px solid #fff;width:{x['w']};height:{x['h']};position:absolute;left:{x['x']};top:{x['y']}'>{'<div style=' + labelStyle + '>' + x['label'] + '</div>' if 'label' in x else ''}</div>",
                                    boxes
                                )
                            )
                        )
                    }
                </div>

                <div style="position: fixed; left: 10px; bottom: 10px; display: flex; justify-content: space-between; align-items: center; ">
                    <input type="range" min="0.01" max="2.00" value="1.00" step="0.01" id="scale" />
                    <p id="scale-value" style="margin-left: 20px; background: #000; color: #fff; padding: 3px 7px; font-family: Trebuchet MS">Scale: 1.00</p>
                </div>

                <script>
                    document.querySelector("#scale").addEventListener("input", ev => {{
                        document.querySelector("#scale-container").style.transform = `scale(${{ ev.currentTarget.value }})`;
                        document.querySelector("#scale-value").innerHTML = `Scale: ${{ev.currentTarget.value}}`;
                    }})
                </script>
            </body>
        </html>
        """

    displayHtml(content, title, width, height)


def displayHtml(content, title, width: int = 900, height: int = 500):
    import sys, platform, ctypes
    from tempfile import NamedTemporaryFile
    from cefpython3 import cefpython as cef

    file = NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".html", delete=False)
    file.write(content)
    file.flush()

    try:
        sys.excepthook = cef.ExceptHook
        cef.Initialize()

        window_info = cef.WindowInfo()
        parent_handle = 0
        window_info.SetAsChild(parent_handle, [0, 0, width, height])
        browser = cef.CreateBrowserSync(url=file.name, window_info=window_info, window_title=title)
        if platform.system() == "Windows":
            window_handle = browser.GetOuterWindowHandle()
            insert_after_handle = 0
            # X and Y parameters are ignored by setting the SWP_NOMOVE flag
            SWP_NOMOVE = 0x0002
            # noinspection PyUnresolvedReferences
            ctypes.windll.user32.SetWindowPos(window_handle, insert_after_handle, 0, 0, width, height, SWP_NOMOVE)

        cef.MessageLoop()
        del browser
        cef.Shutdown()
    except Exception:
        pass


def getFileFromRessource(ressource):
    import numpy, cv2

    if isinstance(ressource, Response):
        ressource = ressource.unpack("fileId")["fileId"]

    assert isFileId(ressource) or isLocalFile(ressource), f"invalid fileId or local file: {ressource}"

    if isFileId(ressource):
        file = read(ressource)
        file = numpy.frombuffer(file, dtype=numpy.uint8)
        file = cv2.imdecode(file, flags=1)
    else:
        file = cv2.imread(ressource)
    
    return file


def getImageFromRessource(ressource, scale: float = 1):
    import cv2, base64
    file = getFileFromRessource(ressource)
    iw = int(file.shape[1] * scale)
    ih = int(file.shape[0] * scale)
    file = cv2.resize(file, (iw, ih))
    _, buffer = cv2.imencode('.jpg', file)
    img = base64.b64encode(buffer).decode("utf-8")
    return img, iw, ih

