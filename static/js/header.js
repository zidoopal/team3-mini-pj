'use strict';

// 상세 페이지 이동
const DetailPageIcon = document.querySelector('.fa-user');

function myPageHandler() {
  if (true) {
    window.location.href = 'http://127.0.0.1:5501/templates/detail.html#';
  }
}

DetailPageIcon.addEventListener('click', myPageHandler);

// 로그아웃
const logOutIcon = document.querySelector('.fa-right-from-bracket');

// 로그인 페이지로 돌아가기
function logOutHandler() {
  if (true) {
    window.location.href = 'http://127.0.0.1:5501/templates/login.html';
  }
}

logOutIcon.addEventListener('click', logOutHandler);
