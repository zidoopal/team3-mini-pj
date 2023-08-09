function checkLoginStatus() {
  const token = getCookie("AccessToken");
  if (token) {
    // 서버에 인증 요청을 보냄
    fetch("/auth/verify", {
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
          // 인증 성공
          // document.querySelector(".logout-button").style.display = "block";
          // document.querySelector(".login-button").style.display = "none";
        } else {
          // 인증 실패
          // document.querySelector(".logout-button").style.display = "none";
          // document.querySelector(".login-button").style.display = "block";
        }
      })
      .catch((error) => {
        console.error("인증 실패:", error);
        if (error.message === "Unauthorized") {
          deleteCookie("AccessToken");
          window.location.href = "/login";
        } else {
          alert("인증 중 오류 발생");
        }
      });
  } else {
    // 토큰 없음, 로그아웃 상태
    console.log("로그인되지 않은 유저");
    // document.querySelector(".logout-button").style.display = "none";
    // document.querySelector(".login-button").style.display = "block";
  }
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function deleteCookie(name) {
  document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

// 현재 페이지의 경로를 확인해서 로그인 상태를 적용
if (
  window.location.pathname === "/create-post" ||
  window.location.pathname === "/"
) {
  checkLoginStatus();
}
