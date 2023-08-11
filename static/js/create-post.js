const uploadBtn = document.querySelector("#upload_button");

function upload() {
  let image = document.querySelector("#image_upload").files[0];
  let song_title = document.querySelector("#song_title").value;
  let artist = document.querySelector("#artist").value;
  console.log(image, song_title,artist)

  // 예외처리
  if(song_title && artist && image) {
    let formData = new FormData();
    formData.append("image_give", image);
    formData.append("song_title_give", song_title);
    formData.append("artist_give", artist);

    fetch("/upload", { method: "POST", body: formData })
      .then((response) => response.json())
      .then((data) => {
        alert(data["msg"]);
        window.location.href='/';
      });
  } else {
    alert('정보를 입력해주세요!')
  }
}

uploadBtn.addEventListener("click", upload);
