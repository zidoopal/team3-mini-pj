'use strict';

const homeIcon = document.querySelector('#nav-main-button');
const writeIcon = document.querySelector('#nav-write-button');

// 홈 (main)으로 이동
function homeHandler() {
  window.location.href = '/';
}
homeIcon.addEventListener('click', homeHandler);

// 작성 페이지 이동
function writeHandler() {
  window.location.href = '/create-post';
}
writeIcon.addEventListener('click', writeHandler);
