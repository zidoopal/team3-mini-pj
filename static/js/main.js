'use strict';

// 사진 불러오기
document.addEventListener('DOMContentLoaded', function () {
  listing();
});

function listing() {
  // rows 변수가 여기서 정의되어야 합니다.
  fetch('/upload')
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      let rows = data['result'];

      c;

      rows.forEach((a) => {
        let userName = a['user'];
        let img_url = a['img_url'];
        let artistName = a['artist'];
        let song_title = a['song_title'];
        // let date = a['']
        console.log(userName, img_url, artistName, song_title);
        let photoSection = document.querySelector('.photo-set');

        let photoSetHTML = `<div class="photo-set">
                                <div class="artist-photo">
                                  <img src="${img_url}" id="tag" />
                                </div>
                                <div class="photo-info">
                                  <p id="tag">${(artistName, song_title)}</p>
                                  <p id="date"><span id="userName">${userName}</span></p>
                                </div>
                              </div>
                            </div>`;

        photoSection.innerHTML += photoSetHTML;
      });
    });
}

// 상세 페이지로 이동
const artistPhoto = document.querySelector('.artist-photo');

function photoToDetailPage() {
  window.location.href = '/detail/<post_id>';
}
artistPhoto.addEventListener('click', photoToDetailPage);
