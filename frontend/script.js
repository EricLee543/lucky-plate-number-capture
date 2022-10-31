document
  .getElementById("cameraFileInput")
  .addEventListener("change", function () {
    document
      .getElementById("pictureFromCamera")
      .setAttribute("src", window.URL.createObjectURL(this.files[0]));
  });

document.getElementById("clear_btn").addEventListener("click", function () {
  document.getElementById("pictureFromCamera").setAttribute("src", "");
});

document.getElementById("submit_btn").addEventListener("click", function () {
  let fileList = document.getElementById('cameraFileInput').files
  let fd = new FormData() //文件传输一定要使用ForData对象
  fd.append('file', fileList[0])
  fd.append("name", "test")
  const request = new XMLHttpRequest();
  request.responseType = 'arraybuffer';
  request.onreadystatechange = function() {
    if (request.readyState == XMLHttpRequest.DONE) {
      // show the image from the server
      let blob = new Blob([request.response], {type: 'image/jpg'});
      let url = window.URL.createObjectURL(blob);
      document.getElementById("pictureFromCamera").setAttribute("src", url);
    }
}
  request.open("POST", "http://127.0.0.1:5000/post/image");
  request.send(fd);
});

// Upload the image to the server
