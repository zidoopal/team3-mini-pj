'use strict';

// 사진 불러오기
$(document).ready(function () {
  showPhoto();
});

function showPhoto() {
  fetch('/upload')
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      let rows = data['result'];

      $('.photo-section').empty();
      rows.forEach((a) => {
        let userName = a['user'];
        let img_url = a['img_url'];
        let artistName = a['artist'];
        let songTitle = a['song_title'];
        let date = a['createAT'];
        let photoSetHTML = `<div class="photo-set">
                                <div class="artist-photo">
                                  <img src="${img_url}" />
                                </div>
                                <div class="photo-info">
                                  <p id="artistName">#${artistName}<span id="song_title">#${songTitle}</span></p>
                                  <p id="date">${date}<span id="userName">${userName}</span></p>
                                </div>
                              </div>`;

        $('.photo-section').append(photoSetHTML);
      });
    });
}

// 상세 페이지로 이동
const artistPhoto = document.querySelector('.artist-photo');

function photoToDetailPage() {
  window.location.href = '/detail/post_id';
}
artistPhoto.addEventListener('click', photoToDetailPage);
