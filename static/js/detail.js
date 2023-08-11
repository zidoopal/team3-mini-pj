const postId = getPostId(); // 어디서든 postId를 가져올 수 있는 함수를 가정합니다.

// 서버로부터 게시글 데이터를 받아와 화면에 출력하는 함수
function fetchPostDetail() {
  fetch(`/api/detail/${postId}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("네트워크 에러");
      }
      return response.json();
    })
    .then((data) => {
      $("#postImage").attr("src", data.img_url);
      $("#createdAt p").text(data.createdAt);
      $("#createUser p").text(data.user);
      $("#artist p").text(` #${data.artist}` );
      $("#song_title p").text(` #${data.song_title}`);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// 서버로부터 데이터를 받아와 댓글을 출력하는 함수
function fetchComments() {
  fetch(`/detail/${postId}/comments`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("네크워크 에러");
      }
      return response.json();
    })
    .then((data) => {
      const commentContainer = $("#comment-container");
      // 기존 댓글 삭제
      commentContainer.empty();

      data.comments.forEach((comment) => {
        const commentHtml = `
          <div class="detail__comment">
            <div class="detail__comment_user-wrapper">
              <div class="detail__comment__profile">
                <img src="${comment.userProfileImage}" alt="User Profile">
              </div>
              <div class="detail__comment__user">
                <p>${comment.userName}</p>
              </div>
            </div>
            <div class="detail__comment__content">
              <p>${comment.content}</p>
            </div>
          </div>
        `;

        commentContainer.append(commentHtml);
      });
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function getPostId() {
  const path = window.location.pathname;
  const parts = path.split("/");

  if (parts.length > 2) {
    return parseInt(parts[2], 10);
  } else {
    return null;
  }
}

// 댓글 추가하는 코드
document.getElementById("comment-button").addEventListener("click", () => {
  const comment = document.getElementById("comment-input").value;

  if (!comment.trim()) {
    alert("댓글을 입력해주세요.");
    return;
  }

    // 로컬 스토리지에서 email, name, picture 가져오기
    const userEmail = localStorage.getItem('email');
    const userName = localStorage.getItem('name');
    const userPicture = localStorage.getItem('picture'); 
  
    const payload = {
      comment: comment,
      email: userEmail,
      name: userName,
      picture: userPicture
    };

    
  fetch(`/detail/${postId}/comment`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("댓글이 성공적으로 등록되었습니다.");
        document.getElementById("comment-input").value = "";
        window.location.reload();
      } else {
        alert(data.message || "댓글 등록에 실패했습니다.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("댓글 등록 중 오류가 발생했습니다.");
    });
});

// 페이지 로드 시 댓글 및 게시글 상세 내용 가져오기
document.addEventListener("DOMContentLoaded", function () {
  fetchComments();
  fetchPostDetail();
});
