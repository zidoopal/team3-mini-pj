'use strict';

// 상세 페이지 이동
const DetailPageIcon = document.querySelector('#nav-mypage-button');

function myPageHandler() {
  // 상세 페이지 URL로 이동
  window.location.href = 'http://plipli.site/detail';
}

DetailPageIcon.addEventListener('click', myPageHandler);

// 회원가입 페이지 이동
const signUpIcon = document.querySelector('#nav-signup-button');

function signUpHandler() {
  // 회원가입 페이지 URL로 이동
  window.location.href = 'http://plipli.site/signup';
}

signUpIcon.addEventListener('click', signUpHandler);

// 로그아웃
const logOutIcon = document.querySelector('#nav-logout-button');

// 메인 페이지로 돌아가기
function logOutHandler() {
  // 메인 페이지 URL로 이동
  window.location.href = 'http://plipli.site/';
}

logOutIcon.addEventListener('click', logOutHandler);

// 로그인
const logInIcon = document.querySelector('#nav-login-button');

// 로그인 페이지로 가기
function logInHandler() {
  // 로그인 페이지 URL로 이동
  window.location.href = 'http://plipli.site/login';
}

logInIcon.addEventListener('click', logInHandler);
