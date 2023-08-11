function checkLoginStatus() {
  const token = getCookie("AccessToken");
  if (token) {
    // 서버에 인증 요청을 보냄
    return fetch("/auth/verify", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok && response.status === 401) {
          throw new Error("Unauthorized");
        }
        return response.json();
      })
      .then((data) => {
        if (data.authenticated) {
          return true; // 로그인 상태
        } else {
          redirectUnauthenticatedUser();
          return false; // 로그아웃 상태
        }
      })
      .catch((error) => {
        console.error("인증 중 오류 발생:", error);
        redirectUnauthenticatedUser();
        return false; // 로그아웃 상태
      });
  } else {
    console.log("로그인되지 않은 유저");
    redirectUnauthenticatedUser();
    return false; // 로그아웃 상태
  }
}

// 인증되지 않은 유저가 접근했을 경우 실행되는 코드 또는 로그인이 필요한 기능
function redirectUnauthenticatedUser() {
  if (window.location.pathname === "/create-post") {

    alert("로그인이 필요한 기능입니다. 로그인 후 이용해주세요.");
    window.location.href = "/";
  } else {
      // document.querySelector("#nav-logout-button").style.display = "block";
      // document.querySelector("#nav-login-button").style.display = "none";
      // document.querySelector("#nav-signup-button").style.display = "block";
      // document.querySelector("#nav-mypage-button").style.display = "none";
    alert("올바르지 않은 접근입니다. 다시 로그인해주세요");
    deleteCookie("AccessToken");
    window.location.href = "/login";
  }
}

// 쿠키 가져오는 함수
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

// 올바르지 않은 토큰 또는 로그아웃 시 쿠키 제거하는 함수
function deleteCookie(name) {
  document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

// 현재 페이지의 경로를 확인해서 로그인 상태를 적용
if (
  window.location.pathname === "/create-post" ||
  window.location.pathname === "/" ||
  window.location.pathname === "/detail"
) {
  checkLoginStatus();
}
