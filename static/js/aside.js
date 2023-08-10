'use strict';

// 홈 (main)으로 이동
const homeIcon = document.querySelector('#nav-main-button');

function homeHandler() {
  // 메인 페이지 URL로 이동
  window.location.href = 'http://plipli.site/';
}

homeIcon.addEventListener('click', homeHandler);

// 작성 페이지 이동
const writeIcon = document.querySelector('#nav-write-button');

function writeHandler() {
  // 작성 페이지 URL로 이동
  window.location.href = 'http://plipli.site/create-post';
}

writeIcon.addEventListener('click', writeHandler);
