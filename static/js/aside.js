'use strict';

// 홈 (main)으로 이동
const homeIcon = document.querySelector('#nav-main-button');

function homeHandler() {
  if (true) {
    window.location.href = 'http://plipli.site/';
  }
}
homeIcon.addEventListener('click', homeHandler);

// 작성 페이지 이동
const writeIcon = document.querySelector('#nav-write-button');

function writeHandler() {
  if (true) {
    // 작성 도메인 아직??
    window.location.href = 'http://plipli.site/create-post';
  }
}

writeIcon.addEventListener('click', writeHandler);
