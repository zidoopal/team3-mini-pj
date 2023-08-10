'use strict';

// 홈 으로 이동
const homeIcon = document.querySelector('.fa-house');

function homeHandler() {
  if (true) {
    window.location.href = 'http://127.0.0.1:5501/templates/index.html';
  }
}
homeIcon.addEventListener('click', homeHandler);

// 작성 페이지 이동
const writeIcon = document.querySelector('.fa-pen');

function writeHandler() {
  if (true) {
    window.location.href = 'http://127.0.0.1:5501/templates/createPost.html';
  }
}

writeIcon.addEventListener('click', writeHandler);
