const uploadBtn = document.querySelector("#upload_button");

function upload() {
  let image = document.querySelector("#image_upload").files[0];
  // console.log(image)
  let song_title = document.querySelector("#song_title").value;
  let artist = document.querySelector("#artist").value;
  let formData = new FormData();
  formData.append("image_give", image);
  formData.append("song_title_give", song_title);
  formData.append("artist_give", artist);

  fetch("/upload", { method: "POST", body: formData })
    .then((response) => response.json())
    .then((data) => {
      alert(data["msg"]);
      window.location.reload();
    });
}

uploadBtn.addEventListener("click", upload);
