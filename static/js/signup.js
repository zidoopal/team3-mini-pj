const signupBtn = document.querySelector("#signup-button");

const signup = () => {
    const email = $("#email").val();
    const password = $("#password").val();
    const confirmPassword = $("#confirmPassword").val();
    const nickname = $("#nickname").val();

    let formData = new FormData();
    formData.append("email_give", email);
    formData.append("password_give", password);
    formData.append("confirmPassword_give", confirmPassword);
    formData.append("nickname_give", nickname);


    fetch('/signup', { method: "POST", body: formData, }).then((res) => res.json()).then((data) => {
        alert(data['msg'])
        
        let error_html = ``
        // 이메일 입력 여부 검증
        if(data['msg'] == '이메일을 입력해주세요!'){
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-email').append(error_html)
            $('#signup-email').children('#email').addClass('input_validation_error')
        }
        // 이메일 유효성 검증
        else if (data['msg'] == '유효하지 않은 이메일 입니다!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-email').append(error_html)
            $('#signup-email').children('#email').addClass('input_validation_error')
        }
        // 이메일 중복 검증
        else if (data['msg'] == '이미 등록된 이메일 입니다!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-email').append(error_html)
            $('#signup-email').children('#email').addClass('input_validation_error')
        }
        // 비밀번호 입력 검증
        else if (data['msg'] == '비밀번호를 입력해주세요!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-password').append(error_html)
            $('#signup-password').children('#password').addClass('input_validation_error')
            $('#signup-password').children('#password').val('')
        }
        // 비밀번호 길이 검증
        else if (data['msg'] == '비밀번호는 5자리 이상 20자리 이하로 해주세요!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-password').append(error_html)
            $('#signup-password').children('#password').addClass('input_validation_error')
        }
        // 비밀번호 일치 여부 검증
        else if (data['msg'] == '비밀번호가 일치하지 않습니다!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-confirmPassword').append(error_html)
            $('#signup-confirmPassword').children('#confirmPassword').addClass('input_validation_error')
        }
        else if (data['msg'] == '닉네임을 입력해주세요!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-nickname').append(error_html)
            $('#signup-nickname').children('#nickname').addClass('input_validation_error')
        }
        // 닉네임 길이 검증
        else if (data['msg'] == '닉네임은 20자리 이하로 해주세요!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-nickname').append(error_html)
            $('#signup-nickname').children('#nickname').addClass('input_validation_error')
        }
        // 닉네임 중복 검증
        else if (data['msg'] == '이미 등록된 닉네임 입니다!') {
            error_html = `<div class="validation_error_msg">${data['msg']}</div>`
            $('.validation_error_msg').detach();
            $('input').removeClass('input_validation_error')
            $('#signup-nickname').append(error_html)
            $('#signup-nickname').children('#nickname').addClass('input_validation_error')
        }

        else if (data['msg'] == '회원가입이 완료되었습니다!') {
            
            window.location.href = "/login"
        }



    });
}

signupBtn.addEventListener("click", signup);