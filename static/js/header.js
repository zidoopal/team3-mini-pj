'use strict';

// 상세 페이지 이동
const myPageIcon = document.querySelector('#nav-mypage-button');
const signUpIcon = document.querySelector('#nav-signup-button');
const logOutIcon = document.querySelector('#nav-logout-button');
const logInIcon = document.querySelector('#nav-login-button');

// // 마이페이지
// function myPageHandler() {
//   // 마이페이지 구현 X ?
//   window.location.href = '';
// }
// myPageIcon.addEventListener('click', myPageHandler);

// 회원가입 페이지 이동
function signUpHandler() {
  window.location.href = '/signup';
}
signUpIcon.addEventListener('click', signUpHandler);

// 로그아웃
// 메인 페이지로 돌아가기
function logOutHandler() {
  window.location.href = '/';
}
logOutIcon.addEventListener('click', logOutHandler);

// 로그인 페이지로 가기
function logInHandler() {
  window.location.href = '/login';
}
logInIcon.addEventListener('click', logInHandler);
